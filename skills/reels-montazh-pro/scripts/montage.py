#!/usr/bin/env python3
"""Финальная сборка «как в CapCut» одним ffmpeg: графика сверху, ты снизу (сдвиг/кроп), громкости, вставки на слове.

  python3 montage.py montage.json                      → итоговый mp4 (путь в "out")
  python3 montage.py montage.json --frame 12.5         → один кадр png для проверки раскладки
  python3 montage.py montage.json --compare экспорт_из_CapCut.mp4 --times 1,10,30
        → разница кадров с экспортом автора (средняя < 2% и худшая клетка < 6% — совпало)

montage.json (пути — относительно файла; слои рисуются по порядку, последний сверху):
{
  "out": "Итог_Ролик1_4K.mp4",
  "canvas": [2160, 3840], "fps": 60, "background": "black",
  "words": "out/Ролик1.words.json",            // для "at_word" (расшифровка ГОТОВОГО ролика)
  "layers": [
    {"name": "я",       "file": "out/Ролик1.mp4", "main": true,
     "crop": {"x": 0, "y": 742, "w": 2160, "h": 1914}, "pos": [0, 1926], "volume": 2.6},
    {"name": "графика", "file": "Наложение_ролик1.mp4",
     "crop": {"x": 0, "y": 31, "w": 2160, "h": 1926}, "pos": [0, 0], "volume": 0.26},
    {"name": "вставка", "file": "запись_экрана.mp4", "src_start": 76.07, "dur": 5.0,
     "at_word": "сайтов",                       // или "at": 46.1 (сек ролика), или {"word": "сайтов", "n": 2}
     "crop": {"x": 258, "y": 133, "w": 3018, "h": 1748}, "size": [2080, 1204], "pos": [40, 674], "volume": 0}
  ],
  "limiter": 0.95, "codec": "h264", "bitrate": "80M"
}
Параметры раскладки можно снять из проекта CapCut: python3 capcut_layout.py draft_info.json --out montage.json"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import probe, need, video_codec_args, color_bsf, words_from_json, norm


def load(path):
    c = json.load(open(path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(path))
    for L in c['layers']:
        L['file'] = os.path.join(base, L['file'])
        if not os.path.exists(L['file']):
            sys.exit(f'нет файла слоя «{L.get("name")}»: {L["file"]}')
        L['info'] = probe(L['file'])
    c['out'] = os.path.join(base, c.get('out', 'montage_out.mp4'))
    if c.get('words'):
        c['words'] = os.path.join(base, c['words'])
    return c


def word_time(c, spec):
    if isinstance(spec, str):
        spec = {'word': spec, 'n': 1}
    if not c.get('words') or not os.path.exists(c['words']):
        sys.exit('для at_word нужна расшифровка готового ролика: "words": "…words.json" (transcribe.py ролик.mp4)')
    ws = words_from_json(c['words'])
    target = norm(spec['word'])
    hits = [w for w in ws if norm(w['word'])[:len(target)] == target or norm(w['word']) == target]
    n = spec.get('n', 1)
    if len(hits) < n:
        sys.exit(f'слово «{spec["word"]}» (№{n}) не найдено в {c["words"]}')
    t = hits[n - 1]['start'] + spec.get('shift', 0)
    print(f'  вставка на слове «{hits[n - 1]["word"]}» → {t:.2f} с')
    return t


def build(c, audio=True):
    W, H = c['canvas']
    fps = c.get('fps', 60)
    main = next((L for L in c['layers'] if L.get('main')), c['layers'][0])
    dur = c.get('duration') or main.get('dur') or main['info']['duration']
    ins, fc, au = [], [f"color=c={c.get('background', 'black')}:s={W}x{H}:r={fps}:d={dur:.3f}[b0]"], []
    cur = 'b0'
    for i, L in enumerate(c['layers']):
        if 'src_start' in L or 'dur' in L:
            ins += ['-ss', str(L.get('src_start', 0))] + (['-t', str(L['dur'])] if 'dur' in L else [])
        ins += ['-i', L['file']]
        at = L.get('at', 0)
        if 'at_word' in L:
            at = word_time(c, L['at_word'])
        L['_at'] = at
        cw, ch = L['info']['width'], L['info']['height']
        chain = []
        if L.get('crop'):
            k = L['crop']
            chain.append(f"crop={k['w']}:{k['h']}:{k['x']}:{k['y']}")
            cw, ch = k['w'], k['h']
        if L.get('size') or L.get('scale', 1) != 1:
            tw, th = L['size'] if L.get('size') else (round(cw * L['scale'] / 2) * 2, round(ch * L['scale'] / 2) * 2)
            if tw > cw * 1.001 or th > ch * 1.001:
                print(f'⚠ слой «{L.get("name", i)}» растягивается ×{tw / cw:.2f} выше исходного размера — будет мыло. '
                      f'Лучше отрендерить его крупнее (render_overlay.py --scale 2).')
            chain.append(f'scale={tw}:{th}:flags=lanczos')
        chain += [f'fps={fps}', f'setpts=PTS-STARTPTS+{at:.3f}/TB']
        fc.append(f'[{i}:v]' + ','.join(chain) + f'[l{i}]')
        x, y = L.get('pos', [0, 0])
        fc.append(f'[{cur}][l{i}]overlay={x}:{y}:eof_action=pass[b{i + 1}]')
        cur = f'b{i + 1}'
        vol = L.get('volume', 1 if L is main else 0)
        if audio and vol and L['info']['has_audio']:
            ms = int(at * 1000)
            fc.append(f'[{i}:a]asetpts=PTS-STARTPTS,aresample=48000,adelay={ms}|{ms},volume={vol}[a{i}]')
            au.append(f'[a{i}]')
    fc.append(f'[{cur}]null[vout]')
    if au:
        fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.3f}[a_bg]")
        fc.append('[a_bg]' + ''.join(au) + f"amix=inputs={len(au) + 1}:normalize=0:duration=first,"
                  f"alimiter=limit={c.get('limiter', 0.95)}[aout]")
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[vout]']
    return cmd, bool(au), dur


def frame_gray(path, t, w=540):
    import numpy as np
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', str(t), '-i', path, '-frames:v', '1',
                        '-vf', f'scale={w}:-2,format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.uint8)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('config')
    ap.add_argument('--frame', type=float, help='отрендерить один кадр (png) на этой секунде')
    ap.add_argument('--compare', help='экспорт автора из CapCut для сверки')
    ap.add_argument('--times', default='1,5,10')
    ap.add_argument('--out')
    a = ap.parse_args()
    need('ffmpeg')
    c = load(a.config)
    if a.out:
        c['out'] = a.out
    cmd, has_a, dur = build(c, audio=a.frame is None and not a.compare)
    if a.frame is not None or a.compare:
        times = [a.frame] if a.frame is not None else [float(x) for x in a.times.split(',')]
        import numpy as np
        for t in times:
            png = os.path.splitext(c['out'])[0] + f'_кадр_{t:g}.png'
            subprocess.run(cmd + ['-ss', str(t), '-frames:v', '1', png], check=True)
            print('кадр →', png)
            if a.compare:
                A, B = frame_gray(png, 0).astype(int), frame_gray(a.compare, t).astype(int)
                if A.shape != B.shape:
                    print(f'  {t:g} с: разные пропорции кадров — сравнение невозможно')
                    continue
                D = np.abs(A - B).reshape(-1, 540)
                d = D.mean() / 255 * 100
                h = D.shape[0] // 30 * 30
                blk = D[:h].reshape(h // 30, 30, 18, 30).mean(axis=(1, 3)) / 255 * 100   # клетки 30×30
                worst = blk.max()
                ok = d < 2 and worst < 6
                print(f'  {t:g} с: разница {d:.1f}% (худшая клетка {worst:.0f}%) '
                      f'{"✓ совпадает" if ok else "⚠ раскладка/время отличаются — смотри кадр"}')
        return
    cmd += (['-map', '[aout]', '-c:a', 'aac', '-b:a', '320k'] if has_a else [])
    vc = video_codec_args(c.get('codec', 'h264'), c.get('bitrate', '80M'))
    cmd += vc + color_bsf(vc)
    cmd += ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', '-t', f'{dur:.3f}', c['out']]
    subprocess.run(cmd, check=True)
    print(f'✓ {c["out"]} ({dur:.1f} с, {c["canvas"][0]}×{c["canvas"][1]})')


if __name__ == '__main__':
    main()
