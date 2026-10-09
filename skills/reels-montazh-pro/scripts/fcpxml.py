#!/usr/bin/env python3
"""Проект для DaVinci Resolve / Final Cut (FCPXML 1.9) из того же плана, что и cut.py:
каждый ролик — отдельный таймлайн, резы ровно как в готовых mp4, весь исходник под ними сохранён
(можно потянуть край куска и подвинуть рез).

  python3 fcpxml.py plan.json [--out Проект_для_DaVinci.fcpxml]
DaVinci: File → Import → Timeline… → выбрать .fcpxml → OK."""
import argparse, os, sys
from fractions import Fraction
from xml.sax.saxutils import escape
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut import Plan
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('plan')
    ap.add_argument('--out')
    a = ap.parse_args()
    P = Plan(a.plan)
    fps = Fraction(P.fps)
    fd = 1 / fps                                         # длительность кадра, напр. 1/60 или 1001/30000
    def tt(frames):
        v = Fraction(frames) * fd
        return f'{v.numerator}/{v.denominator}s' if v.denominator != 1 else f'{v.numerator}s'
    S0 = P.sources[0].info
    W, H = S0['width'], S0['height']
    cs = 'Rec. 2020 HLG' if S0['color_transfer'] == 'arib-std-b67' else (
         'Rec. 2020 PQ' if S0['color_transfer'] == 'smpte2084' else 'Rec. 709')
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<!DOCTYPE fcpxml>', '<fcpxml version="1.9">', '<resources>',
           f'<format id="r1" name="FFVideoFormat{W}x{H}p{round(float(fps))}" frameDuration="{fd.numerator}/{fd.denominator}s" '
           f'width="{W}" height="{H}" colorSpace="{cs}"/>']
    ids = {}
    for k, S in enumerate(P.sources):
        rid = f'r{k + 2}'
        ids[S.file] = rid
        dur = round(S.info['duration'] * fps)
        out.append(f'<asset id="{rid}" name="{escape(Path(S.file).stem)}" start="0s" duration="{tt(dur)}" hasVideo="1" '
                   f'hasAudio="1" format="r1" audioSources="1" audioChannels="2" audioRate="48000">'
                   f'<media-rep kind="original-media" src="{escape(Path(S.file).resolve().as_uri())}"/></asset>')
    out += ['</resources>', '<library>', f'<event name="{escape(Path(P.path).stem)}">']
    for name in P.reels:
        off, clips = 0, []
        for ci, co, txt, *_ in P.pieces(name):
            S = P.src(ci)
            fa, fb = round((ci - S.offset) * fps), round((co - S.offset) * fps)
            d = fb - fa
            clips.append(f'<asset-clip ref="{ids[S.file]}" name="{escape(txt[:60])}" offset="{tt(off)}" '
                         f'start="{tt(fa)}" duration="{tt(d)}" format="r1" tcFormat="NDF"/>')
            off += d
        out += [f'<project name="{escape(name)}">',
                f'<sequence format="r1" tcStart="0s" tcFormat="NDF" duration="{tt(off)}" audioLayout="stereo" audioRate="48k">',
                '<spine>'] + clips + ['</spine>', '</sequence>', '</project>']
    out += ['</event>', '</library>', '</fcpxml>']
    dst = a.out or os.path.join(P.base, 'Проект_для_DaVinci.fcpxml')
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    print('✓', dst)


if __name__ == '__main__':
    main()
