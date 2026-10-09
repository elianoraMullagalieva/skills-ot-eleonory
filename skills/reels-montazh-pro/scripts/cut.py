#!/usr/bin/env python3
"""Нарезка длинной записи с дублями в чистые ролики по плану (резы по словам + доводка по тишине).

  python3 cut.py plan.json                      → таблица резов + проверки (паузы, «погнали», повторы)
  python3 cut.py plan.json --render             → out/<ролик>.mp4 для всех роликов плана
  python3 cut.py plan.json --render --reel Ролик1 --codec h264   (8 бит для CapCut; исходник должен быть SDR)
  python3 cut.py plan.json --render --preview   → быстрые превью 1080p
  python3 cut.py plan.json --plans-js ../grafika/plans.js   → куски для движка графики (+ СЛОВА_ПО_КУСКАМ.md)
  python3 cut.py plan.json --verify             → расшифровать готовые ролики и проверить, что фразы целые
                                                  (+ out/<ролик>.words.json — слова готового ролика)

plan.json (пути — относительно plan.json):
{
  "source": "IMG_3061_SDR.mov",            // или "sources": [{"file":"A.mov","offset":0},{"file":"B.mov","offset":1000}]
  "words": "IMG_3061.words.json",          // по умолчанию <исходник>.words.json (сделай transcribe.py)
  "split_pauses": 0.5,                     // резать паузы длиннее N с внутри куска (0 = не резать)
  "reels": {
    "Ролик1": [[62.6, 63.9, "Обалденное обновление Figma."], …]   // [сек ПЕРВОГО слова, сек НАЧАЛА ПОСЛЕДНЕГО слова, текст]
  },
  "ovr": {"76.6": 76.40}                   // ручная точка начала куска: {сек_первого_слова: сек_реза}
}"""
import argparse, json, math, os, subprocess, sys
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (probe, load_audio, words_from_json, video_codec_args, color_args, color_bsf, hwdec, nice_fps, need, norm)

FILLERS = {'погнали', 'угу', 'ага', 'блин', 'стоп', 'заново', 'эм', 'э', 'ммм', 'мм', 'кхм', 'дубль'}
HOP = 0.01   # шаг RMS 10 мс


class Source:
    def __init__(self, base, d):
        self.file = os.path.join(base, d['file'])
        if not os.path.exists(self.file):
            sys.exit(f'Нет исходника: {self.file}')
        self.offset = float(d.get('offset', 0))
        wj = d.get('words') or os.path.splitext(self.file)[0] + '.words.json'
        wj = os.path.join(base, wj)
        if not os.path.exists(wj):
            sys.exit(f'Нет расшифровки {wj}. Сначала: python3 transcribe.py "{self.file}"')
        self.words = words_from_json(wj, self.offset)
        self.info = probe(self.file)
        self.cache = os.path.join(base, '_cache')
        self._rms = None

    @property
    def rms(self):
        if self._rms is None:
            import numpy as np
            a = load_audio(self.file, 16000, self.cache)
            hop = int(16000 * HOP)
            self._rms = np.sqrt(np.convolve(a ** 2, np.ones(hop * 2) / (hop * 2), 'same')[::hop])
            floor = np.percentile(self._rms, 20)
            self.thr = max(floor * 3, 0.006)          # «тишина» = ниже 3× фона, но не ниже 0.006
        return self._rms

    def covers(self, t):
        return self.offset <= t < self.offset + self.info['duration'] + 0.5


class Plan:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.base = os.path.dirname(self.path)
        d = json.load(open(path, encoding='utf-8'))
        self.d = d
        srcs = d.get('sources') or [{'file': d['source'], 'words': d.get('words'), 'offset': 0}]
        self.sources = [Source(self.base, s) for s in srcs]
        self.words = sorted([w for s in self.sources for w in s.words], key=lambda w: w['start'])
        self.reels = d['reels']
        self.ovr = {float(k): float(v) for k, v in d.get('ovr', {}).items()}
        self.split = float(d.get('split_pauses', 0.5))
        info = self.sources[0].info
        self.fps = nice_fps(d['fps']) if d.get('fps') else nice_fps(info['fps'])
        self.out_dir = os.path.join(self.base, d.get('out_dir', 'out'))

    def src(self, t):
        for s in self.sources:
            if s.covers(t):
                return s
        sys.exit(f'Секунда {t} не попадает ни в один исходник')

    def near(self, t):
        return min(range(len(self.words)), key=lambda i: abs(self.words[i]['start'] - t))

    # ---------- один кусок: от первого слова до НАЧАЛА последнего ----------
    def seg(self, s, e):
        import numpy as np
        S = self.src(s)
        rms, thr, off = S.rms, S.thr, S.offset
        W = self.words
        i0, i1 = self.near(s), self.near(e)       # e = НАЧАЛО последнего слова: так не съедаем окончание
        w0, w1 = W[i0], W[i1]
        pe = W[i0 - 1]['end'] if i0 > 0 else off
        ns = W[i1 + 1]['start'] if i1 + 1 < len(W) else w1['end'] + 1
        R = lambda t: int(round((t - off) / HOP))
        # начало: последний тихий момент перед первым звуком слова
        lo = max(pe + 0.03, w0['start'] - 0.5)
        hi = w0['start'] + 0.08
        iw, ilo = R(w0['start']), max(0, R(lo))
        loud = lambda i: 0 <= i and i + 3 <= len(rms) and bool(np.all(rms[i:i + 3] >= thr))
        if 0 <= iw and iw + 3 <= len(rms) and np.all(rms[iw:iw + 3] < thr):
            # whisper поставил начало слова в тишину (часто — раньше реального звука): ищем первый звук после
            j = next((i for i in range(iw, min(len(rms) - 3, iw + 60)) if loud(i)), iw)
        else:
            quiet = [i for i in range(ilo, min(len(rms), R(hi))) if rms[i] < thr]
            j = quiet[-1] + 1 if quiet else ilo
        # тихие первые звуки («У-станавливаем»): короткий звук сразу перед найденным началом — тоже часть слова
        while True:
            k = j - 1
            while k > max(ilo, j - 16) and rms[k] < thr:      # пауза до 0.15 с
                k -= 1
            if k <= ilo or rms[k] < thr or j - k > 15:
                break
            st = k
            while st > ilo and rms[st - 1] >= thr:
                st -= 1
            if k - st + 1 < 3 or st <= ilo:
                break
            j = st
        cin = j * HOP + off - 0.08                    # 80 мс «воздуха» перед первым звуком
        cin = max(cin, pe + 0.02)
        # конец: тишину ищем от КОНЦА последнего слова — первые 80 мс тишины подряд + 0.1 с хвост
        lo2 = w1['end'] + 0.02
        hi2 = min(ns - 0.03, w1['end'] + 0.6)
        cout = hi2
        for i in range(R(lo2), R(hi2) - 8):
            if i + 8 <= len(rms) and np.all(rms[i:i + 8] < thr):
                cout = i * HOP + off + 0.10
                break
        cout = min(cout, ns - 0.02)
        cin = self.ovr.get(round(s, 2), self.ovr.get(s, cin))
        return round(cin, 3), round(cout, 3)

    def inner_pauses(self, s, e):
        """Паузы внутри «одного» дубля по тишине (RMS): [(k, длина)] — пауза между словом k и k+1.
        Тишину ищем по звуку, а слово после паузы — по положению тишины (whisper часто ставит начало слова раньше)."""
        if not self.split:
            return []
        S = self.src(s)
        rms, thr, off = S.rms, S.thr, S.offset
        W = self.words
        i0, i1 = self.near(s), self.near(e)
        if i1 <= i0:
            return []
        a, b = W[i0]['start'] + 0.12, W[i1]['end'] - 0.05
        runs, st = [], None
        for i in range(int((a - off) / HOP), int((b - off) / HOP) + 1):
            q = 0 <= i < len(rms) and rms[i] < thr
            if q and st is None:
                st = i
            if (not q or i == int((b - off) / HOP)) and st is not None:
                if (i - st) * HOP >= self.split:
                    runs.append((st * HOP + off, (i - st) * HOP))
                st = None
        res = []
        for r0, d in runs:
            kb = next((k for k in range(i0 + 1, i1 + 1) if W[k]['start'] >= r0 - 0.05), None)
            if kb is not None and (not res or res[-1][0] != kb - 1):
                res.append((kb - 1, d))
        return res

    def pieces(self, reel):
        """Куски ролика: с автоделением по паузам и без микроперекрытий на стыках."""
        out = []
        for item in self.reels[reel]:
            s, e, txt = item[0], item[1], (item[2] if len(item) > 2 else '')
            bounds = [(s, e)]
            for k, _ in self.inner_pauses(s, e):
                last_s, last_e = bounds.pop()
                bounds += [(last_s, self.words[k]['start']), (self.words[k + 1]['start'], last_e)]
            for j, (a, b) in enumerate(bounds):
                ci, co = self.seg(a, b)
                out.append([ci, co, txt if len(bounds) == 1 else f'{txt} [{j + 1}/{len(bounds)}]', a, b])
        for i in range(1, len(out)):           # стык соседних кусков: убрать микроповтор
            if out[i - 1][0] < out[i][0] < out[i - 1][1]:
                out[i][0] = out[i - 1][1]
        return out

    def check(self, reel):
        warn = []
        W = self.words
        for item in self.reels[reel]:
            s, e = item[0], item[1]
            i0, i1 = self.near(s), self.near(e)
            if abs(W[i0]['start'] - s) > 0.25:
                warn.append(f'{s}: рядом нет начала слова (ближайшее «{W[i0]["word"]}»@{W[i0]["start"]:.2f})')
            if abs(W[i1]['start'] - e) > 0.25:
                warn.append(f'{e}: вторая цифра — НАЧАЛО последнего слова; ближайшее «{W[i1]["word"]}»@{W[i1]["start"]:.2f}')
            seg = W[i0:i1 + 1]
            for k, w in enumerate(seg):
                n = norm(w['word'])
                if n and n[0] in FILLERS:
                    warn.append(f'{s}: в куске слово-паразит «{w["word"]}»@{w["start"]:.2f}')
                if k and norm(seg[k - 1]['word']) == n and n:
                    warn.append(f'{s}: повтор «{w["word"]}»@{w["start"]:.2f} — оговорка?')
                if k and norm(seg[k - 1]['word']) == ['еще'] and n == ['раз']:
                    warn.append(f'{s}: «ещё раз»@{w["start"]:.2f} — служебная фраза дубля')
            for k, d in self.inner_pauses(s, e):
                warn.append(f'{s}: пауза {d:.2f} с после «{W[k]["word"]}»@{W[k]["start"]:.2f} — режу на два куска')
            if seg and seg[-1]['probability'] < 0.4:
                warn.append(f'{s}: последнее слово «{seg[-1]["word"]}» неразборчиво (p={seg[-1]["probability"]:.2f}) — проверь окончание или возьми другой дубль')
        return warn

    # ---------- рендер ----------
    def render(self, reel, codec='auto', preview=False, out=None, force=False, bitrate=None):
        need('ffmpeg')
        ps = self.pieces(reel)
        info = self.sources[0].info
        if codec == 'auto':
            codec = 'hevc10' if info['hdr'] else 'h264'
        if preview:
            codec = 'preview'
        if info['hdr'] and codec in ('h264', 'preview') and not force:
            if preview:
                print('⚠ исходник HDR: превью будет с блёклым цветом (это только превью).')
            else:
                sys.exit('Исходник HDR (HLG/Dolby Vision). Для CapCut сначала переведи его в SDR: '
                         'python3 to_sdr.py исходник.MOV — и поставь SDR-файл в "source" плана. '
                         '(10-бит HEVC CapCut иногда открывает как «файл повреждён».)')
        F = self.fps
        W0, H0 = info['width'], info['height']
        os.makedirs(self.out_dir, exist_ok=True)
        out = out or os.path.join(self.out_dir, f'{reel}{"_preview" if preview else ""}.mp4')
        cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y']
        for ci, co, *_ in ps:
            S = self.src(ci)
            cmd += hwdec() + ['-ss', f'{ci - S.offset:.3f}', '-t', f'{co - ci:.3f}', '-i', S.file]
        fc = []
        for i, (ci, co, *_r) in enumerate(ps):
            d = co - ci
            S = self.src(ci)
            vf = f'fps={F},setpts=PTS-STARTPTS'
            if (S.info['width'], S.info['height']) != (W0, H0):
                print(f'⚠ {os.path.basename(S.file)} другого размера — привожу к {W0}×{H0}')
                vf += f',scale={W0}:{H0}:force_original_aspect_ratio=decrease,pad={W0}:{H0}:(ow-iw)/2:(oh-ih)/2'
            if preview and H0 > 1920:
                vf += ',scale=-2:1920'           # превью: только уменьшаем, никогда не растягиваем
            fc.append(f'[{i}:v:0]{vf}[v{i}]')
            fc.append(f'[{i}:a:0]aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:d=0.012,'
                      f'afade=t=out:st={max(0, d - 0.015):.3f}:d=0.015[a{i}]')
        n = len(ps)
        fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][a]')
        cmd += ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]']
        vc = video_codec_args(codec, bitrate)
        ci_ = info if codec != 'preview' else {'hdr': False}
        cmd += vc + color_args(ci_) + color_bsf(vc, ci_)
        cmd += ['-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', out]
        subprocess.run(cmd, check=True)
        tot = sum(co - ci for ci, co, *_ in ps)
        print(f'✓ {reel}: {n} кусков, {tot:.1f} с → {out}')
        return out

    # ---------- куски для движка графики ----------
    def plans_js(self, path):
        F = float(self.fps)
        out, names, md = {}, {}, ['# Слова по кускам (секунды ИСХОДНИКА)\n']
        for k, reel in enumerate(self.reels, 1):
            ps = self.pieces(reel)
            # длительность = целое число кадров, как у ffmpeg -ss/-t → синхрон графики до кадра
            out[str(k)] = [[round(a, 3), round(a + math.ceil((b - a) * F - 1e-6) / F, 4)] for a, b, *_ in ps]
            names[str(k)] = reel
            md.append(f'\n## Ролик {k} — {reel}\n')
            for a, b in out[str(k)]:
                ws = ' '.join(f"{w['word']}@{w['start']:.2f}" for w in self.words if a - 0.05 <= w['start'] < b)
                md.append(f'- кусок [{a}, {b}]: {ws}')
        js = ('/* куски исходника для каждого ролика: [начало, конец] в секундах ИСХОДНИКА (сгенерировано cut.py) */\n'
              f'const PLANS={json.dumps(out)};\nconst REEL_NAMES={json.dumps(names, ensure_ascii=False)};\n')
        open(path, 'w', encoding='utf-8').write(js)
        mdp = os.path.join(os.path.dirname(os.path.abspath(path)), 'СЛОВА_ПО_КУСКАМ.md')
        open(mdp, 'w', encoding='utf-8').write('\n'.join(md) + '\n')
        print('plans.js →', path, '| слова по кускам →', mdp)
        print({names[k]: round(sum(b - a for a, b in v), 2) for k, v in out.items()})

    # ---------- проверка готового ролика повторной расшифровкой ----------
    def verify(self, reel, file=None, lang='ru'):
        from transcribe import transcribe
        file = file or os.path.join(self.out_dir, f'{reel}.mp4')
        if not os.path.exists(file):
            sys.exit(f'Нет {file} — сначала --render')
        segs = transcribe(file, lang)
        wj = os.path.splitext(file)[0] + '.words.json'      # пригодится montage.py для "at_word"
        json.dump(segs, open(wj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        got = [w for s in segs for w in s['words']]
        ps, off, bad = self.pieces(reel), 0.0, 0
        print(f'\n== проверка {os.path.basename(file)}')
        for ci, co, txt, a, b in ps:
            d = co - ci
            ws = [w for w in got if off - 0.05 <= w['start'] < off + d - 0.02]
            want = [w['word'] for w in self.words if a - 0.05 <= w['start'] <= b + 0.05]
            r = SequenceMatcher(None, norm(' '.join(want)), norm(' '.join(w['word'] for w in ws))).ratio()
            notes = []
            if r < 0.8:
                notes.append(f'совпадение {r:.0%}')
            if ws and ws[-1]['end'] > off + d - 0.02:
                notes.append(f'последнее слово «{ws[-1]["word"]}» упирается в рез — окончание обрезано?')
            if ws and ws[-1]['probability'] < 0.4:
                notes.append(f'«{ws[-1]["word"]}» неразборчиво (p={ws[-1]["probability"]:.2f})')
            if want and ws and norm(want[-1]) != norm(ws[-1]['word']):
                notes.append(f'ждали в конце «{want[-1]}», слышно «{ws[-1]["word"]}»')
            for w in ws:
                if norm(w['word'])[:1] and norm(w['word'])[0] in FILLERS:
                    notes.append(f'паразит «{w["word"]}»')
            bad += bool(notes)
            print(f'{"⚠" if notes else "✓"} {off:6.2f}–{off + d:6.2f}  {" ".join(w["word"] for w in ws)[:90]}'
                  + (f'\n     → {"; ".join(notes)}' if notes else ''))
            off += d
        print(f'итого: {len(ps) - bad} из {len(ps)} кусков чистые')
        return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plan')
    ap.add_argument('--reel', action='append', help='только этот ролик (можно несколько раз)')
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--preview', action='store_true', help='быстрое превью 1080p H.264')
    ap.add_argument('--codec', default='auto', choices=['auto', 'h264', 'hevc10'],
                    help='auto: HDR-исходник → HEVC 10 бит HDR, SDR → H.264 8 бит (для CapCut)')
    ap.add_argument('--bitrate', help='например 60M')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--plans-js', help='записать plans.js для движка графики')
    ap.add_argument('--verify', action='store_true', help='расшифровать готовые ролики и проверить фразы')
    ap.add_argument('--lang', default='ru')
    a = ap.parse_args()
    P = Plan(a.plan)
    reels = a.reel or list(P.reels)
    for r in reels:
        if r not in P.reels:
            sys.exit(f'Нет ролика «{r}». Есть: {", ".join(P.reels)}')
        print(f'== {r}')
        tot = 0
        for ci, co, txt, *_ in P.pieces(r):
            tot += co - ci
            print(f'{ci:9.2f} → {co:9.2f}  ({co - ci:5.2f} с)  {txt}')
        print(f'   итого {tot:.1f} с')
        for w in P.check(r):
            print('   ⚠', w)
    if a.plans_js:
        P.plans_js(a.plans_js)
    if a.render or a.preview:
        for r in reels:
            P.render(r, a.codec, a.preview, force=a.force, bitrate=a.bitrate)
    if a.verify:
        bad = sum(P.verify(r, lang=a.lang) for r in reels)
        sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
