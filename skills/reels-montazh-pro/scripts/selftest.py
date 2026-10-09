#!/usr/bin/env python3
"""Сквозная проверка скилла на синтетическом ролике (2–4 минуты):
демо-запись с дублями → transcribe → pick_takes → cut (+проверки, рендер, plans.js, FCPXML) → кадры записи экрана →
графика (render_overlay) → звуки (mix_sfx) → монтаж (montage, кадр, сверка) → мельтешение → проверка расшифровкой → HDR→SDR.

  python3 selftest.py [рабочая_папка]     (по умолчанию — временная папка)"""
import json, os, shutil, subprocess, sys, tempfile, time
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
PY = sys.executable
results = []


def step(name, cmd, cwd, ok_codes=(0,)):
    t = time.time()
    print(f'\n▶ {name}\n  $ {" ".join(cmd)}')
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    out = (r.stdout + r.stderr).strip()
    print('  ' + out[-1500:].replace('\n', '\n  '))
    good = r.returncode in ok_codes
    results.append((name, good, round(time.time() - t, 1)))
    return good, out


def main():
    wd = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else tempfile.mkdtemp(prefix='reels_selftest_')
    os.makedirs(wd, exist_ok=True)
    S = lambda f: os.path.join(HERE, f)
    print('рабочая папка:', wd)
    step('демо-запись (say/espeak + ffmpeg)', [PY, os.path.join(SKILL, 'examples', 'make_demo.py'), wd], wd)
    step('transcribe', [PY, S('transcribe.py'), 'demo_source.mp4', '--words-js', 'words.js', '--quiet'], wd)
    step('pick_takes по сценарию → plan.json', [PY, S('pick_takes.py'), 'demo_source.mp4', '--script', 'сценарий.txt',
                                               '--plan', 'plan.json', '--reel', 'Демо'], wd)
    step('cut: таблица резов и проверки', [PY, S('cut.py'), 'plan.json'], wd)
    step('cut: рендер (H.264 8 бит)', [PY, S('cut.py'), 'plan.json', '--render'], wd)
    step('cut: plans.js для графики', [PY, S('cut.py'), 'plan.json', '--plans-js', 'plans.js'], wd)
    step('fcpxml для DaVinci', [PY, S('fcpxml.py'), 'plan.json'], wd)
    step('кадры записи экрана', [PY, S('clip_frames.py'), 'demo_screen.mp4', 'frames/screen', '--from', '0', '--to', '5',
                                '--width', '1340'], wd)
    shutil.copy(os.path.join(SKILL, 'engine', 'grafika.html'), wd)
    shutil.copytree(os.path.join(SKILL, 'engine', 'fonts'), os.path.join(wd, 'fonts'), dirs_exist_ok=True)
    shutil.copy(os.path.join(SKILL, 'examples', 'scenes.js'), wd)
    step('графика: проба 0–2.5 с ×2', [PY, S('render_overlay.py'), '--html', 'grafika.html', '--reel', '1', '--end', '2.5',
                                      '--scale', '2', '--out', 'test_2s.mp4'], wd)
    step('графика: весь ролик ×1', [PY, S('render_overlay.py'), '--html', 'grafika.html', '--reel', '1',
                                   '--out', 'Наложение_ролик1.mp4'], wd)
    step('звуки на действиях', [PY, S('mix_sfx.py'), '--html', 'grafika.html', '--reel', '1', '--voice', 'out/Демо.mp4',
                                '--mux', 'Наложение_ролик1.mp4'], wd)
    step('проверка расшифровкой', [PY, S('cut.py'), 'plan.json', '--verify'], wd, ok_codes=(0, 1))
    cfg = {'out': 'Итог_демо.mp4', 'canvas': [1080, 1920], 'fps': 30, 'background': 'black',
           'words': 'out/Демо.words.json',
           'layers': [
               {'name': 'я', 'file': 'out/Демо.mp4', 'main': True, 'crop': {'x': 0, 'y': 360, 'w': 1080, 'h': 1272},
                'pos': [0, 648], 'volume': 1.0},
               {'name': 'графика', 'file': 'Наложение_ролик1_sfx.mp4', 'pos': [0, 0], 'volume': 0.6},
               {'name': 'вставка', 'file': 'demo_screen.mp4', 'src_start': 1.0, 'dur': 1.5, 'at_word': 'готово',
                'size': [640, 400], 'pos': [220, 980], 'volume': 0}]}
    json.dump(cfg, open(os.path.join(wd, 'montage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    step('монтаж', [PY, S('montage.py'), 'montage.json'], wd)
    step('монтаж: кадр + сверка с самим собой', [PY, S('montage.py'), 'montage.json', '--compare', 'Итог_демо.mp4',
                                                  '--times', '1,3'], wd)
    step('мельтешение', [PY, S('flicker_check.py'), 'Наложение_ролик1.mp4'], wd, ok_codes=(0, 1))
    # HDR → SDR: синтетический HLG-клип 2 с
    hlg = os.path.join(wd, 'hlg_test.mov')
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=s=640x1136:r=30:d=2',
                        '-c:v', 'libx265', '-pix_fmt', 'yuv420p10le', '-tag:v', 'hvc1',
                        '-x265-params', 'log-level=error:colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc',
                        '-color_primaries', 'bt2020', '-color_trc', 'arib-std-b67', '-colorspace', 'bt2020nc', hlg])
    if r.returncode == 0:
        step('HDR → SDR (Apple на Mac / ffmpeg иначе)', [PY, S('to_sdr.py'), 'hlg_test.mov', '--capcut'], wd)
    print('\n================ ИТОГ ================')
    for n, g, t in results:
        print(f'{"✓" if g else "✗"} {n}  ({t} с)')
    print('папка с результатами:', wd)
    sys.exit(0 if all(g for _, g, _ in results) else 1)


if __name__ == '__main__':
    main()
