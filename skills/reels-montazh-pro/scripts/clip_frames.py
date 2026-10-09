#!/usr/bin/env python3
"""Запись экрана → пронумерованные кадры jpg для вставки в графику (покадрово, точный синхрон).

  python3 clip_frames.py запись.mp4 frames/copy --from 1.2 --to 19.05 --width 1760
        → frames/copy/f_001.jpg … (30 к/с); печатает, сколько кадров и какой секунде записи соответствует кадр 1

В сцене: setFrame(img,'frames/copy',k) где k = 1 + round((сек_записи − from)·30);
сек_записи берётся из timeMap([[сек_исходника, сек_записи], …]) — кусочно-линейная привязка записи к словам.
--width: ширина кадра. Бери 2× от ширины окна в сцене (рендер наложения идёт с --scale 2), не больше исходной."""
import argparse, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import probe, need


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video')
    ap.add_argument('out_dir')
    ap.add_argument('--from', dest='t0', type=float, default=0)
    ap.add_argument('--to', dest='t1', type=float)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--width', type=int, default=1760)
    ap.add_argument('--crop', help='w:h:x:y — обрезать рамки/панели записи')
    ap.add_argument('--quality', type=int, default=3, help='2 — лучше, 5 — легче')
    a = ap.parse_args()
    need('ffmpeg')
    info = probe(a.video)
    src_w = int(a.crop.split(':')[0]) if a.crop else info['width']
    w = min(a.width, src_w)                       # не растягиваем выше исходника
    if w < a.width:
        print(f'⚠ запись уже {src_w}px — беру {w}px (растягивать нельзя)')
    os.makedirs(a.out_dir, exist_ok=True)
    vf = (f'crop={a.crop},' if a.crop else '') + f'fps={a.fps},scale={w}:-2:flags=lanczos'
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(a.t0)] + (['-t', f'{a.t1 - a.t0:.3f}'] if a.t1 else []) + \
          ['-i', a.video, '-vf', vf, '-q:v', str(a.quality), '-start_number', '1', os.path.join(a.out_dir, 'f_%03d.jpg')]
    subprocess.run(cmd, check=True)
    n = len([f for f in os.listdir(a.out_dir) if f.startswith('f_') and f.endswith('.jpg')])
    print(f'✓ {n} кадров → {a.out_dir}; кадр 1 = {a.t0:.2f} с записи, кадр k = {a.t0:.2f} + (k−1)/{a.fps} с')


if __name__ == '__main__':
    main()
