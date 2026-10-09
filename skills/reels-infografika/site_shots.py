#!/usr/bin/env python3
"""Скриншоты сайта автора для изучения стиля.
python3 site_shots.py https://site.ru папка_вывода   (или путь к локальной папке с index.html)
Делает 14 экранов + site_contact.jpg + печатает CSS-переменные, шрифты и частые цвета."""
import sys,os,asyncio,subprocess,re,collections,http.server,threading,functools
from playwright.async_api import async_playwright
src,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True)
if os.path.isdir(src):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    h=functools.partial(Q,directory=src)
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',8765),h);threading.Thread(target=srv.serve_forever,daemon=True).start()
    url='http://127.0.0.1:8765/index.html'
else: url=src
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(url,wait_until='networkidle');await pg.wait_for_timeout(2000)
        H=await pg.evaluate('document.body.scrollHeight')
        for i in range(14):
            await pg.evaluate(f'window.scrollTo(0,{int(H*i/14)})');await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'{out}/site{i:02d}.jpg',quality=60)
        info=await pg.evaluate('''()=>{const c={},f={};for(const e of document.querySelectorAll('body *')){const s=getComputedStyle(e);
          [s.color,s.backgroundColor,s.borderColor].forEach(x=>{if(x&&x!=='rgba(0, 0, 0, 0)')c[x]=(c[x]||0)+1});f[s.fontFamily]=(f[s.fontFamily]||0)+1;}
          const v=[...document.styleSheets].flatMap(sh=>{try{return [...sh.cssRules]}catch(e){return []}}).filter(r=>r.selectorText===':root').map(r=>r.cssText);
          return {colors:Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0,15),fonts:Object.entries(f).sort((a,b)=>b[1]-a[1]).slice(0,5),root:v.slice(0,3)}}''')
        await b.close()
    print('ШРИФТЫ:',*info['fonts'],sep='\n  ');print('ЦВЕТА (частота):',*info['colors'],sep='\n  ');print(':root:',*info['root'],sep='\n  ')
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{out}/site%02d.jpg','-vf','scale=720:-1,tile=2x7','-frames:v','1',f'{out}/site_contact.jpg'])
    print('контакт-лист:',f'{out}/site_contact.jpg')
asyncio.run(main())
