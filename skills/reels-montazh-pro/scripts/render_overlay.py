#!/usr/bin/env python3
"""Покадровый рендер HTML-графики в mp4: кадр = render(t), снимается по одному → синхрон до кадра, без пропусков.

  python3 render_overlay.py --html grafika.html --reel 1 --out Наложение_ролик1.mp4 --scale 2
  python3 render_overlay.py --html grafika.html --reel 2 --start 10 --end 13 --out test.mp4   (кусок для проверки)
  python3 render_overlay.py --html grafika.html --reel 1 --audio out/Ролик1.mp4             (+ версия со звуком)

HTML должен выставить window.render(t) и window.DURATION; размер кадра = #stage.
--scale 2: холст 1080×648 → видео 2160×1296 (для 4K-монтажа). --query: любые параметры страницы (a=1&b=2)."""
import argparse, asyncio, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import need


async def run(a):
    from playwright.async_api import async_playwright
    html = Path(a.html).resolve()
    q = 'render=1' + (f'&reel={a.reel}' if a.reel else '') + (f'&{a.query}' if a.query else '')
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=a.scale)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        await pg.goto(html.as_uri() + '?' + q)
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_timeout(300)
        w, h, dur = await pg.evaluate('[stage.offsetWidth,stage.offsetHeight,window.DURATION]')
        await pg.set_viewport_size({'width': w, 'height': h})
        end = min(a.end, dur) if a.end is not None else dur
        n = int(round((end - a.start) * a.fps))
        W, H = int(round(w * a.scale)), int(round(h * a.scale))
        print(f'{w}×{h} ×{a.scale} → {W}×{H}, {end - a.start:.2f} с, {n} кадров')
        ff = subprocess.Popen(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-f', 'image2pipe', '-framerate', str(a.fps), '-i', '-',
                               '-vf', f'scale={W}:{H}:flags=lanczos', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', str(a.crf),
                               '-preset', 'slow', '-tune', 'animation',
                               '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', a.out],
                              stdin=subprocess.PIPE)
        for i in range(n):
            await pg.evaluate(f'render({a.start + i / a.fps})')   # render может вернуть Promise (ждём кадры записей экрана)
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=97))
            if i % 300 == 0:
                print(f'  {i}/{n}')
        await br.close()
        ff.stdin.close()
        ff.wait()
        if errs:
            print('⚠ JS-ошибки:', *errs[:5], sep='\n  ')
    if a.audio:
        o = a.out.replace('.mp4', '_so_zvukom.mp4')
        subprocess.run(['ffmpeg', '-nostdin', '-y', '-v', 'error', '-ss', str(a.start), '-i', a.audio, '-i', a.out,
                        '-map', '1:v', '-map', '0:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', o], check=True)
        print('со звуком:', o)
    print('✓', a.out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--html', required=True)
    ap.add_argument('--out', default='grafika.mp4')
    ap.add_argument('--reel', help='номер ролика из plans.js')
    ap.add_argument('--start', type=float, default=0)
    ap.add_argument('--end', type=float)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--scale', type=float, default=1, help='2 = вдвое больше пикселей (резкость для 4K)')
    ap.add_argument('--crf', type=int, default=14)
    ap.add_argument('--query', default='')
    ap.add_argument('--audio', help='ролик с голосом — сделает *_so_zvukom.mp4 для проверки синхрона')
    a = ap.parse_args()
    need('ffmpeg')
    try:
        import playwright  # noqa
    except ImportError:
        sys.exit('Нет playwright: pip install playwright && python3 -m playwright install chromium')
    asyncio.run(run(a))


if __name__ == '__main__':
    main()
