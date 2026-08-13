#!/usr/bin/env python3
# Запись HTML-анимации в mp4 через playwright video (реальное время = точный синхрон).
# Вертикаль 1080x1920. Фон берётся из HTML (для альфы делаем чёрным).
import sys, asyncio, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

async def record(html, out, duration_ms):
    out_dir = Path(out).parent / ("_vid_tmp_" + Path(out).stem)
    out_dir.mkdir(exist_ok=True, parents=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(
            viewport={"width":1080,"height":1920}, device_scale_factor=1,
            record_video_dir=str(out_dir), record_video_size={"width":1080,"height":1920},
        )
        pg = await ctx.new_page()
        await pg.goto(f"file://{Path(html).resolve()}?qa=1")
        await pg.wait_for_load_state("domcontentloaded")
        await pg.add_style_tag(content=".panel{display:none!important}")
        await pg.wait_for_timeout(250)
        await pg.evaluate("startAnimation()")
        await pg.wait_for_timeout(duration_ms)
        await ctx.close(); await b.close()
    webm = sorted(out_dir.glob("*.webm"), key=lambda f:f.stat().st_mtime, reverse=True)[0]
    subprocess.run(["ffmpeg","-y","-i",str(webm),
        "-c:v","libx264","-pix_fmt","yuv420p","-crf","16","-preset","fast",
        "-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,crop=1080:1920",
        "-an", str(out)], check=True)
    print("ГОТОВО:", out)

if __name__ == "__main__":
    html=sys.argv[sys.argv.index("--html")+1]; out=sys.argv[sys.argv.index("--out")+1]
    dur=float(sys.argv[sys.argv.index("--duration")+1])
    asyncio.run(record(html, out, int(dur*1000)))
