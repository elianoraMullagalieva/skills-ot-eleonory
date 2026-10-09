#!/usr/bin/env python3
"""Детектор мельтешения: находит смены кадра (резкая разница соседних кадров) и места, где смены идут
чаще, чем раз в 0.9 с — зритель не успевает прочитать. Работает и для графики, и для готового монтажа.

  python3 flicker_check.py Наложение_ролик1.mp4 [--min-gap 0.9] [--thresh 8] [--crop 0:0:1080:648]

Выводит: список смен, «быстрые смены < 0.9 с» с таймкодами и плотность смен по секундам.
Что делать с находками: объединить соседние сцены, сдвинуть смену на следующее слово, оставить одну
акцентную деталь в кадре; смены — не чаще ~1.2 с (кроме намеренного «удара» на хуке)."""
import argparse, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import probe, need


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video')
    ap.add_argument('--min-gap', type=float, default=0.9, help='смены ближе этого — мельтешение')
    ap.add_argument('--thresh', type=float, default=8, help='порог «смены кадра»: средняя разница яркости 0–255 (6 — чувствительнее, 12 — только полные смены сцены)')
    ap.add_argument('--crop', help='смотреть только область w:h:x:y (напр. только графику над головой)')
    ap.add_argument('--fps', type=int, default=30)
    a = ap.parse_args()
    need('ffmpeg')
    import numpy as np
    W, H = 160, 0
    info = probe(a.video)
    ar = (info['height'] / info['width']) if not a.crop else int(a.crop.split(':')[1]) / int(a.crop.split(':')[0])
    H = max(2, int(round(W * ar / 2)) * 2)
    vf = (f'crop={a.crop},' if a.crop else '') + f'fps={a.fps},scale={W}:{H},format=gray'
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', a.video, '-vf', vf, '-f', 'rawvideo', '-'],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W).astype(np.int16)
    diff = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    cuts = []
    for i, d in enumerate(diff):
        t = (i + 1) / a.fps
        if d >= a.thresh and (not cuts or t - cuts[-1][0] > 2 / a.fps):   # пик, а не хвост одной смены
            cuts.append((t, float(d)))
    dur = len(fr) / a.fps
    print(f'{os.path.basename(a.video)}: {dur:.1f} с, смен кадра: {len(cuts)} (в среднем раз в {dur / max(1, len(cuts)):.2f} с)')
    fast = [(cuts[i - 1][0], cuts[i][0]) for i in range(1, len(cuts)) if cuts[i][0] - cuts[i - 1][0] < a.min_gap]
    if fast:
        print(f'\n⚠ быстрые смены < {a.min_gap} с: {len(fast)}')
        for t0, t1 in fast:
            print(f'   {t0:7.2f} → {t1:7.2f}  ({t1 - t0:.2f} с)')
    else:
        print(f'✓ быстрых смен (< {a.min_gap} с) нет')
    per = np.zeros(int(dur) + 1, dtype=int)
    for t, _ in cuts:
        per[min(int(t), len(per) - 1)] += 1
    busy = [f'{s}с:{n}' for s, n in enumerate(per) if n >= 2]
    if busy:
        print('секунды с 2+ сменами:', ' '.join(busy))
    print('\nвсе смены:', ' '.join(f'{t:.2f}' for t, _ in cuts))
    sys.exit(1 if fast else 0)


if __name__ == '__main__':
    main()
