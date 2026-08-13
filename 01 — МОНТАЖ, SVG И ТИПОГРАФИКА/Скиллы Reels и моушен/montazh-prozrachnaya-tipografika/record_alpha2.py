#!/usr/bin/env python3
# Прозрачный MOV с альфой + ТОЧНЫЙ синхрон.
# Снимаем прозрачные скриншоты, каждый помечаем ФАКТИЧЕСКИМ временем анимации (performance.now),
# затем ffmpeg concat с реальными длительностями → PTS ровно как в реальном воспроизведении.
import sys, asyncio, subprocess, shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def main(html, out, duration, fps=25):
    fdir = Path(out).parent / ("_alpha_" + Path(out).stem)
    if fdir.exists(): shutil.rmtree(fdir)
    fdir.mkdir(parents=True)

    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width":1080,"height":1920}, device_scale_factor=1)
        pg = await ctx.new_page()
        await pg.goto(f"file://{Path(html).resolve()}?qa=1")
        await pg.wait_for_load_state("domcontentloaded")
        await pg.add_style_tag(content="""
          html,body{background:transparent!important;}
          .stage{background:transparent!important;}
          .stage::before{display:none!important;}
          .panel{display:none!important;}
        """)
        await pg.evaluate("window.__t0=performance.now(); startAnimation();")
        frames = []   # (path, t_actual_sec)
        i = 0
        while True:
            t = await pg.evaluate("(performance.now()-window.__t0)/1000")
            if t >= duration: break
            fp = fdir / f"f_{i:05d}.png"
            await pg.screenshot(path=str(fp), omit_background=True)
            frames.append((fp.name, t))
            i += 1
        await ctx.close(); await b.close()

    # concat с фактическими длительностями кадров
    lst = fdir / "list.txt"
    with open(lst, "w") as f:
        for k,(name,t) in enumerate(frames):
            nt = frames[k+1][1] if k+1 < len(frames) else duration
            f.write(f"file '{name}'\nduration {max(0.001, nt-t):.4f}\n")
        f.write(f"file '{frames[-1][0]}'\n")
    print(f"снято {len(frames)} кадров за {frames[-1][1]:.1f}с анимации")
    subprocess.run([
        "ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),
        "-c:v","prores_ks","-profile:v","4444","-pix_fmt","yuva444p10le",
        str(out),
    ], check=True)
    shutil.rmtree(fdir)
    print("ГОТОВО:", out)

if __name__ == "__main__":
    html=sys.argv[sys.argv.index("--html")+1]; out=sys.argv[sys.argv.index("--out")+1]
    dur=float(sys.argv[sys.argv.index("--duration")+1])
    asyncio.run(main(html, out, dur))
