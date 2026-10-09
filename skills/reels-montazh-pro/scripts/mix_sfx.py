#!/usr/bin/env python3
"""Лёгкие звуки ТОЛЬКО на действиях (copy / paste / click / send / pop) из window.SFX графики.

SFX в сценах: window.SFX=(window.SFX||[]).concat([[151.8,'click'],[160.4,'paste']]) — секунды ИСХОДНИКА
(мульти-ролик с plans.js) или секунды ролика (один ролик без plans.js). Для каждого ролика берутся только
события внутри его кусков и переводятся во время ролика.

  python3 mix_sfx.py --html grafika.html --reel 1 --voice out/Ролик1.mp4
        → sfx_r1.wav (только эффекты) + Наложение_r1_zvuk.m4a (голос + эффекты, для проверки на слух)
  --keep click,copy,paste,send,pop   какие типы оставить   --min-gap 0.8   не чаще раза в N с
  --volume 1.0   общий множитель громкости эффектов
  --mux Наложение_ролик1.mp4   приклеить эффекты к видео наложения (в CapCut громкость наложения = громкость эффектов)"""
import argparse, asyncio, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import need, SKILL

VOL = {'click': .4, 'copy': .45, 'paste': .5, 'send': .45, 'pop': .3, 'whoosh': .25, 'ding': .3, 'type': .3}


async def page_data(html, reel):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto(Path(html).resolve().as_uri() + '?render=1' + (f'&reel={reel}' if reel else ''))
        r = await pg.evaluate('[window.SFX||[], (typeof PLANS!=="undefined" && window.REEL) ? PLANS[window.REEL] : null, window.DURATION]')
        await b.close()
        return r


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--html', required=True)
    ap.add_argument('--reel')
    ap.add_argument('--voice', help='ролик с голосом (нарезка) — сведу голос+эффекты в m4a')
    ap.add_argument('--keep', default='click,copy,paste,send,pop')
    ap.add_argument('--min-gap', type=float, default=0.8)
    ap.add_argument('--volume', type=float, default=1.0)
    ap.add_argument('--sfx-dir', default=os.path.join(SKILL, 'sfx'))
    ap.add_argument('--mux', help='видео наложения: приклеить к нему дорожку эффектов → *_sfx.mp4 (кладёшь в CapCut одним файлом)')
    ap.add_argument('--out-dir', help='куда класть (по умолчанию рядом с html)')
    a = ap.parse_args()
    need('ffmpeg')
    sfx, plan, dur = asyncio.run(page_data(a.html, a.reel))
    keep = set(a.keep.split(','))
    plan = plan or [[0, dur]]
    off, ev = 0.0, []
    for s, e in plan:
        for t, k in sfx:
            if k in keep and s <= t < e:
                ev.append((off + t - s, k))
        off += e - s
    dur = off
    ev.sort()
    clean, last = [], -9
    for t, k in ev:
        if t - last < a.min_gap:
            continue
        clean.append((t, k))
        last = t
    tag = f'r{a.reel}' if a.reel else 'r'
    od = Path(a.out_dir or Path(a.html).resolve().parent)
    od.mkdir(parents=True, exist_ok=True)
    print(f'{len(clean)} звуков:', [(round(t, 2), k) for t, k in clean])
    ins = ['-f', 'lavfi', '-t', f'{dur:.3f}', '-i', 'anullsrc=r=48000:cl=stereo']
    fc = []
    for i, (t, k) in enumerate(clean):
        f = os.path.join(a.sfx_dir, f'{k}.wav')
        if not os.path.exists(f):
            sys.exit(f'нет звука {f} (сгенерируй: python3 sfx/gen_sfx.py)')
        ins += ['-i', f]
        ms = int(t * 1000)
        fc.append(f'[{i + 1}]adelay={ms}|{ms},volume={VOL.get(k, .4) * a.volume:.3f}[e{i}]')
    fc.append('[0]' + ''.join(f'[e{i}]' for i in range(len(clean))) +
              f'amix=inputs={len(clean) + 1}:normalize=0:duration=first,alimiter=limit=0.9[o]')
    out = od / f'sfx_{tag}.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[o]',
                    '-ar', '48000', '-ac', '2', str(out)], check=True)
    print('эффекты →', out)
    if a.voice:
        m = od / f'Наложение_{tag}_zvuk.m4a'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', a.voice, '-i', str(out), '-filter_complex',
                        '[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[o]', '-map', '[o]',
                        '-c:a', 'aac', '-b:a', '256k', str(m)], check=True)
        print('голос + эффекты →', m)
    if a.mux:
        mo = Path(a.mux).with_name(Path(a.mux).stem + '_sfx.mp4')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', a.mux, '-i', str(out), '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', str(mo)], check=True)
        print('наложение + эффекты →', mo)


if __name__ == '__main__':
    main()
