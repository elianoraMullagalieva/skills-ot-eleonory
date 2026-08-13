#!/usr/bin/env python3
"""
Запись HTML-анимации в видео 1080x1920 mp4 (для Reels).

Запуск:
    python3 record.py                       # запись 60 сек
    python3 record.py --duration 45         # своя длительность в секундах
    python3 record.py --html ./other.html   # другой HTML
    python3 record.py --out ./final.mp4     # своё имя выходного файла

Требует:
    pip3 install playwright
    playwright install chromium
    ffmpeg (brew install ffmpeg)
"""
import argparse
import asyncio
import subprocess
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def record(html: Path, out: Path, duration_ms: int):
    out_dir = out.parent / "_record_tmp"
    out_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=1,
            record_video_dir=str(out_dir),
            record_video_size={"width": 1080, "height": 1920},
        )
        page = await context.new_page()
        url = f"file://{html.resolve()}?qa=1"
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")
        await page.add_style_tag(
            content=".progress, .controls { display: none !important; }"
        )
        await page.wait_for_timeout(300)
        await page.evaluate("window.startAnimation()")
        print(f"Запись {duration_ms // 1000} сек...")
        await page.wait_for_timeout(duration_ms)
        await context.close()
        await browser.close()

    webms = sorted(out_dir.glob("*.webm"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not webms:
        print("Ошибка: .webm не создался", file=sys.stderr)
        sys.exit(1)
    webm = webms[0]

    print("Конвертация в mp4...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(webm),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "18", "-preset", "fast",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,"
                   "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
            "-an",
            str(out),
        ],
        check=True,
    )
    webm.unlink()
    try:
        out_dir.rmdir()
    except OSError:
        pass

    print(f"\nГотово: {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, default=Path("index.html"))
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--duration", type=int, default=60, help="длительность записи в секундах")
    args = ap.parse_args()

    html = args.html.resolve()
    if not html.exists():
        print(f"Не найден: {html}", file=sys.stderr)
        sys.exit(1)

    out = args.out
    if out is None:
        out = html.parent / "_out" / (html.stem + ".mp4")
    out = out.resolve()
    out.parent.mkdir(exist_ok=True, parents=True)

    asyncio.run(record(html, out, args.duration * 1000))


if __name__ == "__main__":
    main()
