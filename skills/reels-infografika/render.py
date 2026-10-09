#!/usr/bin/env python3
"""Покадровый рендер HTML → mp4 (точный синхрон, без пропусков кадров).
python3 render.py --html grafika.html --out grafika.mp4 [--start 0 --end 10] [--audio ролик.mp4]
HTML должен экспортировать window.render(t) и window.DURATION, размер сцены #stage."""
import argparse,asyncio,subprocess,pathlib
from playwright.async_api import async_playwright
ap=argparse.ArgumentParser();ap.add_argument('--html',required=True);ap.add_argument('--out',default='grafika.mp4')
ap.add_argument('--start',type=float,default=0);ap.add_argument('--end',type=float);ap.add_argument('--fps',type=int,default=30)
ap.add_argument('--audio',help='исходный ролик — добавит звук в *_so_zvukom.mp4 для проверки синхрона');a=ap.parse_args()
async def main():
    html=pathlib.Path(a.html).resolve()
    async with async_playwright() as p:
        br=await p.chromium.launch();pg=await br.new_page(viewport={'width':1080,'height':1920})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(html.as_uri()+'?render=1');await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(300)
        w,h,dur=await pg.evaluate('[stage.offsetWidth,stage.offsetHeight,window.DURATION]')
        await pg.set_viewport_size({'width':w,'height':h})
        end=a.end if a.end is not None else dur;n=int(round((end-a.start)*a.fps))
        ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate',str(a.fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','16',a.out],stdin=subprocess.PIPE)
        for i in range(n):
            await pg.evaluate(f'render({a.start+i/a.fps})');ff.stdin.write(await pg.screenshot(type='jpeg',quality=94))
            if i%300==0:print(f'{i}/{n}')
        await br.close();ff.stdin.close();ff.wait()
        if errs:print('⚠️ JS-ошибки:',errs[:3])
    if a.audio:
        o=a.out.replace('.mp4','_so_zvukom.mp4')
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(a.start),'-i',a.audio,'-i',a.out,'-map','1:v','-map','0:a','-c:v','copy','-c:a','aac','-shortest',o]);print('со звуком:',o)
    print('готово:',a.out)
asyncio.run(main())
