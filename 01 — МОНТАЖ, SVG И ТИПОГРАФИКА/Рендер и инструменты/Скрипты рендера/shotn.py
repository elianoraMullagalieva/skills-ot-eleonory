import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
html='/Users/elianora/Documents/Reels-animations/reel-nedelai/nedelai.html'
times=[float(t) for t in sys.argv[1:]]
url='file://'+str(pathlib.Path(html).resolve())
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for t in times:
        pg=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=1)
        pg.goto(url+'?qa=1')
        pg.evaluate(f"""()=>{{document.querySelectorAll('.scene').forEach(s=>s.style.opacity=0);
          const c=CUES.filter(c=>c[0]<={t});if(!c.length)return;c[c.length-1][1]();}}""")
        pg.wait_for_timeout(1500)
        f=f'n_{t}.png';pg.screenshot(path=f);shots.append((t,f));pg.close()
    b.close()
cols=min(5,len(shots));rows=(len(shots)+cols-1)//cols;tw=250
ims=[Image.open(s[1]) for s in shots];th=int(tw*ims[0].height/ims[0].width)
sheet=Image.new('RGB',(cols*tw,rows*(th+24)),'#222');d=ImageDraw.Draw(sheet)
for i,((t,_),im) in enumerate(zip(shots,ims)):
    x=(i%cols)*tw;y=(i//cols)*(th+24)
    sheet.paste(im.resize((tw,th)),(x,y+24));d.text((x+4,y+6),f'{t}s',fill='white')
sheet.save('nsheet.png');print('ok')
