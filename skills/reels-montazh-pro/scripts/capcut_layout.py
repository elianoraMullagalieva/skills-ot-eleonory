#!/usr/bin/env python3
"""Снять раскладку из проекта CapCut (draft_info.json) → montage.json для montage.py.

  python3 capcut_layout.py "<папка проекта CapCut>/draft_info.json" --out montage.json [--out-size 2160x3840]

Где лежит проект: macOS — ~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<имя>/draft_info.json,
Windows — %LOCALAPPDATA%\\CapCut\\User Data\\Projects\\com.lveditor.draft\\<имя>\\draft_info.json.
(В новых версиях CapCut файл бывает зашифрован — тогда параметры снимаются вручную по SKILL.md.)

Как CapCut хранит раскладку (проверено на реальном проекте и совпадении с экспортом):
  canvas_config.width/height — холст проекта (напр. 1080×1920; экспорт 4K = ×2);
  material.crop — углы кропа в долях исходника (upper_left_x … lower_right_y);
  обрезанный кусок вписывается в холст: base = min(Cw/cw, Ch/ch), затем × clip.scale;
  clip.transform.x/y — сдвиг ЦЕНТРА обрезанного куска в долях ПОЛОВИНЫ холста, y вверх положительный:
      cx = Cw/2 + x·Cw/2,  cy = Ch/2 − y·Ch/2  (кроп центрируется: в точку ставится центр кропа, а не исходника);
  target_timerange.start — когда слой появляется в ролике, source_timerange.start — откуда берётся (мкс);
  segment.volume — громкость; порядок слоёв — render_index (больше = выше)."""
import argparse, json, os, sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('draft')
    ap.add_argument('--out', default='montage.json')
    ap.add_argument('--out-size', help='размер итогового видео, напр. 2160x3840 (по умолчанию — по главному исходнику)')
    ap.add_argument('--fps', type=int, default=60)
    a = ap.parse_args()
    try:
        d = json.load(open(a.draft, encoding='utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        sys.exit('draft_info.json не читается как JSON (зашифрован новой версией CapCut). Сними параметры вручную — см. SKILL.md.')
    Cw, Ch = d['canvas_config']['width'], d['canvas_config']['height']
    mats = {m['id']: m for m in d['materials'].get('videos', [])}
    segs = []
    for tr in d['tracks']:
        if tr['type'] != 'video':
            if tr['type'] in ('audio', 'text', 'sticker', 'effect'):
                print(f'· дорожка {tr["type"]} ({len(tr["segments"])} шт.) не переносится — добавь вручную, если нужна')
            continue
        for s in tr['segments']:
            segs.append(s)
    segs.sort(key=lambda s: s.get('render_index', 0))
    main = segs[0]
    mm = mats[main['material_id']]
    if a.out_size:
        OW, OH = map(int, a.out_size.lower().split('x'))
    else:
        f0 = min(mm['width'] / Cw, mm['height'] / Ch)
        OW, OH = round(Cw * f0), round(Ch * f0)
    f = OW / Cw
    print(f'холст проекта {Cw}×{Ch} → итог {OW}×{OH} (×{f:g})')
    layers = []
    base_dir = os.path.dirname(os.path.abspath(a.out))
    for i, s in enumerate(segs):
        m = mats[s['material_id']]
        w, h = m['width'], m['height']
        c = m.get('crop') or {}
        x0, y0 = c.get('upper_left_x', 0) * w, c.get('upper_left_y', 0) * h
        x1, y1 = c.get('lower_right_x', 1) * w, c.get('lower_right_y', 1) * h
        cw, ch = x1 - x0, y1 - y0
        clip = s.get('clip') or {}
        sx, sy = clip.get('scale', {}).get('x', 1), clip.get('scale', {}).get('y', 1)
        tx, ty = clip.get('transform', {}).get('x', 0), clip.get('transform', {}).get('y', 0)
        if clip.get('rotation'):
            print(f'⚠ слой {i}: поворот {clip["rotation"]}° не переносится')
        if (clip.get('flip') or {}).get('horizontal') or (clip.get('flip') or {}).get('vertical'):
            print(f'⚠ слой {i}: отражение не переносится')
        if s.get('speed', 1) != 1:
            print(f'⚠ слой {i}: скорость {s["speed"]} не переносится')
        base = min(Cw / cw, Ch / ch)
        dw, dh = cw * base * sx, ch * base * sy
        cx, cy = Cw / 2 + tx * Cw / 2, Ch / 2 - ty * Ch / 2
        left, top = (cx - dw / 2) * f, (cy - dh / 2) * f
        ow, oh = round(dw * f / 2) * 2, round(dh * f / 2) * 2
        crop = {'x': round(x0), 'y': round(y0), 'w': round(cw), 'h': round(ch)}
        L = {'name': os.path.basename(m.get('path', f'слой{i}')),
             'file': os.path.relpath(m['path'], base_dir) if m.get('path') else '?',
             'crop': crop, 'pos': [round(left), round(top)], 'volume': round(s.get('volume', 1), 3)}
        if abs(ow - crop['w']) > 2 or abs(oh - crop['h']) > 2:
            L['size'] = [ow, oh]
        tgt, src = s['target_timerange'], s['source_timerange']
        if s is main:
            L['main'] = True
        else:
            L['at'] = round(tgt['start'] / 1e6, 3)
            if src['start'] or tgt['start']:
                L['src_start'] = round(src['start'] / 1e6, 3)
                L['dur'] = round(tgt['duration'] / 1e6, 3)
        if crop == {'x': 0, 'y': 0, 'w': w, 'h': h}:
            del L['crop']
        layers.append(L)
        print(f'  {i}: {L["name"][:40]:40s} кроп {crop["w"]}×{crop["h"]}+{crop["x"]}+{crop["y"]} → '
              f'{ow}×{oh} в ({L["pos"][0]}, {L["pos"][1]}), громкость {L["volume"]}'
              + (f', с {L["at"]} с' if 'at' in L else ''))
    cfg = {'out': 'Итог.mp4', 'canvas': [OW, OH], 'fps': a.fps, 'background': 'black', 'layers': layers,
           'limiter': 0.95, 'codec': 'h264', 'bitrate': '80M'}
    json.dump(cfg, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('✓', a.out, '— проверь пути к файлам; для нового ролика замени файлы и "at" (или "at_word").')


if __name__ == '__main__':
    main()
