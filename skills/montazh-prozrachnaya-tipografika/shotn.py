#!/usr/bin/env python3
"""Быстрые снимки сцен HTML-монтажа без рендера видео + контактный лист.

Запуск:
    python3 shotn.py --html путь/к/ролику.html 0 2.5 5 7.8
    python3 shotn.py --html ролик.html --out-dir ./shots 0 3 6

Для каждого времени (в секундах) включает сцену из массива CUES, активную
в этот момент, ждёт 1.5 с и делает скриншот 1080x1920. В конце собирает
контактный лист nsheet.png.

Требует: python3 -m pip install --user playwright pillow
         python3 -m playwright install chromium
"""
import argparse
import pathlib

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(description="Снимки сцен HTML-монтажа по таймкодам")
    ap.add_argument("--html", required=True, type=pathlib.Path, help="HTML-файл ролика (с массивом CUES)")
    ap.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path("."), help="куда сохранить снимки")
    ap.add_argument("times", nargs="+", type=float, help="таймкоды в секундах")
    args = ap.parse_args()

    html = args.html.resolve()
    if not html.exists():
        raise SystemExit(f"Не найден HTML: {html}")
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    url = html.as_uri()

    shots = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for t in args.times:
            pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            pg.goto(url + "?qa=1")
            pg.evaluate(f"""()=>{{document.querySelectorAll('.scene').forEach(s=>s.style.opacity=0);
              const c=CUES.filter(c=>c[0]<={t});if(!c.length)return;c[c.length-1][1]();}}""")
            pg.wait_for_timeout(1500)
            f = out_dir / f"n_{t}.png"
            pg.screenshot(path=str(f))
            shots.append((t, f))
            pg.close()
        b.close()

    cols = min(5, len(shots))
    rows = (len(shots) + cols - 1) // cols
    tw = 250
    ims = [Image.open(s[1]) for s in shots]
    th = int(tw * ims[0].height / ims[0].width)
    sheet = Image.new("RGB", (cols * tw, rows * (th + 24)), "#222")
    d = ImageDraw.Draw(sheet)
    for i, ((t, _), im) in enumerate(zip(shots, ims)):
        x = (i % cols) * tw
        y = (i // cols) * (th + 24)
        sheet.paste(im.resize((tw, th)), (x, y + 24))
        d.text((x + 4, y + 6), f"{t}s", fill="white")
    sheet_path = out_dir / "nsheet.png"
    sheet.save(sheet_path)
    print("ok:", sheet_path)


if __name__ == "__main__":
    main()
