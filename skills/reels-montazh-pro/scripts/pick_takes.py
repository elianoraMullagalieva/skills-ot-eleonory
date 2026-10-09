#!/usr/bin/env python3
"""Оценка дублей: какой дубль каждой фразы лучший.

Критерии (чем выше балл, тем лучше):
  • разборчивость — средняя и минимальная вероятность слов whisper (p): каша/проглоченные окончания → низкое p;
  • шипение — доля ВЧ-энергии 6–12 кГц в речи (свист «с/ш», шум петлички) относительно других дублей;
  • паузы внутри дубля, слова-паразиты («погнали», «ещё раз», «угу»), повторы слов.

  python3 pick_takes.py запись.MOV                       → группы похожих фраз и лучший дубль в каждой
  python3 pick_takes.py запись.MOV --script сценарий.txt --reel Ролик1 --plan plan.json
        → для каждой строки сценария найдёт все дубли, выберет лучший и запишет черновик плана для cut.py
Нужен запись.words.json (transcribe.py). Строки сценария — по одной фразе на строку."""
import argparse, json, os, sys
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_audio, words_from_json, norm

FILL = {'погнали', 'угу', 'ага', 'блин', 'стоп', 'заново', 'эм', 'э', 'ммм', 'мм', 'дубль'}


def hf_ratio(a, sr, t0, t1):
    import numpy as np
    x = a[int(t0 * sr):int(t1 * sr)]
    if len(x) < sr * 0.1:
        return 0.0
    n = 2048
    fr = np.fft.rfftfreq(n, 1 / sr)
    hi = (fr >= 6000) & (fr <= 12000)
    tot = (fr >= 100) & (fr <= 12000)
    eh = et = 0.0
    for i in range(0, len(x) - n, n // 2):
        s = np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n))) ** 2
        eh += s[hi].sum()
        et += s[tot].sum()
    return float(eh / et) if et else 0.0


def utterances(words, gap=0.7):
    """Делим речь на фразы: пауза > gap или конец предложения."""
    out, cur = [], []
    for i, w in enumerate(words):
        if cur and (w['start'] - cur[-1]['end'] > gap):
            out.append(cur)
            cur = []
        cur.append(w)
        if w['word'].rstrip().endswith(('.', '!', '?', '…')):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def score(ws, a, sr, hf_ref=None):
    import numpy as np
    p = [w['probability'] for w in ws]
    gaps = [ws[i + 1]['start'] - ws[i]['end'] for i in range(len(ws) - 1)]
    hf = hf_ratio(a, sr, ws[0]['start'], ws[-1]['end'])
    fill = sum(1 for w in ws if norm(w['word'])[:1] and norm(w['word'])[0] in FILL)
    rep = sum(1 for i in range(1, len(ws)) if norm(ws[i]['word']) == norm(ws[i - 1]['word']))
    long_gap = max(gaps) if gaps else 0
    s = 100 * float(np.mean(p)) + 30 * min(p) - 20 * fill - 10 * rep - 15 * max(0, long_gap - 0.4)
    if hf_ref:
        s -= 40 * max(0, hf / hf_ref - 1)       # шипит сильнее медианы — штраф
    return {'score': round(s, 1), 'p_mean': round(float(np.mean(p)), 3), 'p_min': round(min(p), 3),
            'hf': round(hf, 4), 'pause': round(long_gap, 2), 'fillers': fill, 'repeats': rep,
            'start': ws[0]['start'], 'last_start': ws[-1]['start'], 'end': ws[-1]['end'],
            'text': ' '.join(w['word'] for w in ws)}


def strip_fillers(ws):
    while ws and norm(ws[0]['word'])[:1] and norm(ws[0]['word'])[0] in FILL:
        ws = ws[1:]
    while ws and norm(ws[-1]['word'])[:1] and norm(ws[-1]['word'])[0] in FILL:
        ws = ws[:-1]
    return ws


def find_takes(words, line, min_ratio=0.6):
    """Все места, где произнесена строка сценария (скользящее окно по словам)."""
    tgt = norm(line)
    L = len(tgt)
    if not L:
        return []
    nw = [(norm(w['word']) or [''])[0] for w in words]
    cands = []
    for i in range(len(words)):
        for l in (L - 1, L, L + 1):
            if l < 1 or i + l > len(words):
                continue
            r = SequenceMatcher(None, tgt, nw[i:i + l]).ratio()
            if r >= min_ratio:
                cands.append((r, i, i + l))
    cands.sort(reverse=True)
    taken, res = set(), []
    for r, i, j in cands:
        if any(k in taken for k in range(i, j)):
            continue
        taken.update(range(i, j))
        res.append((r, i, j))
    return sorted(res, key=lambda x: x[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('media')
    ap.add_argument('--words', help='words.json (по умолчанию <файл>.words.json)')
    ap.add_argument('--script', help='сценарий: по фразе на строку')
    ap.add_argument('--plan', help='записать/дополнить черновик плана cut.py')
    ap.add_argument('--reel', default='Ролик1', help='имя ролика в плане')
    ap.add_argument('--gap', type=float, default=0.7, help='пауза, которая делит фразы (без --script)')
    ap.add_argument('--min-ratio', type=float, default=0.6)
    a = ap.parse_args()
    wj = a.words or os.path.splitext(a.media)[0] + '.words.json'
    if not os.path.exists(wj):
        sys.exit(f'Нет {wj}. Сначала: python3 transcribe.py "{a.media}"')
    words = words_from_json(wj)
    sr = 32000
    audio = load_audio(a.media, sr)
    import numpy as np

    if a.script:
        lines = [l.strip() for l in open(a.script, encoding='utf-8') if l.strip() and not l.startswith('#')]
        groups = []
        for line in lines:
            tk = [(r, strip_fillers(words[i:j])) for r, i, j in find_takes(words, line, a.min_ratio)]
            groups.append((line, [(r, ws) for r, ws in tk if ws]))
    else:
        utt = [strip_fillers(u) for u in utterances(words, a.gap)]
        utt = [u for u in utt if len(u) >= 2]
        groups = []
        for u in utt:
            t = norm(' '.join(w['word'] for w in u))
            for g in groups:
                if SequenceMatcher(None, t, norm(g[0])).ratio() > 0.6:
                    g[1].append((1.0, u))
                    break
            else:
                groups.append([' '.join(w['word'] for w in u), [(1.0, u)]])

    all_hf = [hf_ratio(audio, sr, ws[0]['start'], ws[-1]['end']) for _, tk in groups for _, ws in tk]
    hf_ref = float(np.median(all_hf)) if all_hf else None
    plan_items, report = [], []
    for line, tk in groups:
        if not tk:
            print(f'\n✗ «{line}» — не нашла в записи (переформулировано? проверь transcript.txt)')
            continue
        sc = [dict(score(ws, audio, sr, hf_ref), match=round(r, 2)) for r, ws in tk]
        for s in sc:
            s['score'] = round(s['score'] + 150 * (s['match'] - 1), 1)  # дубль с другим текстом (пропущено слово) — заметно ниже
        best = max(sc, key=lambda s: s['score'])
        print(f'\n«{line[:80]}» — дублей: {len(sc)}')
        for s in sc:
            mark = '★' if s is best else ' '
            print(f" {mark} {s['start']:8.2f}  балл {s['score']:6.1f}  p̄={s['p_mean']:.2f} pmin={s['p_min']:.2f} "
                  f"ВЧ={s['hf']:.4f} пауза={s['pause']:.2f}{' паразиты' if s['fillers'] else ''}"
                  f"{' повтор' if s['repeats'] else ''}  {s['text'][:70]}")
        plan_items.append([round(best['start'], 2), round(best['last_start'], 2), line if a.script else best['text']])
        report.append({'line': line, 'takes': sc})
    if a.plan:
        plan = json.load(open(a.plan, encoding='utf-8')) if os.path.exists(a.plan) else {
            'source': os.path.relpath(os.path.abspath(a.media), os.path.dirname(os.path.abspath(a.plan))),
            'words': os.path.relpath(os.path.abspath(wj), os.path.dirname(os.path.abspath(a.plan))),
            'split_pauses': 0.5, 'reels': {}, 'ovr': {}}
        plan['reels'][a.reel] = plan_items
        json.dump(plan, open(a.plan, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'\nчерновик плана → {a.plan} (ролик «{a.reel}», {len(plan_items)} кусков). Дальше: python3 cut.py {a.plan}')
    json.dump(report, open(os.path.splitext(wj)[0].replace('.words', '') + '.takes.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
