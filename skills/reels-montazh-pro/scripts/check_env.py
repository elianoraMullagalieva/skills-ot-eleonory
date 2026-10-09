#!/usr/bin/env python3
"""Проверка окружения: что есть, чего нет и как поставить. Запускать первым делом на новой машине.
  python3 check_env.py"""
import importlib, platform, shutil, subprocess, sys

MAC = platform.system() == 'Darwin'
ARM = platform.machine() in ('arm64', 'aarch64')
ok = True


def row(good, name, hint=''):
    global ok
    ok &= good or hint.startswith('(необязательно')
    print(f'{"✓" if good else "✗"} {name}' + ('' if good else f'  →  {hint}'))


print(f'Система: {platform.system()} {platform.machine()}, Python {platform.python_version()}')
row(sys.version_info >= (3, 8), 'Python ≥ 3.8', 'поставь Python 3.10+ с python.org')
ff = shutil.which('ffmpeg') and shutil.which('ffprobe')
row(bool(ff), 'ffmpeg + ffprobe',
    'macOS: brew install ffmpeg · Windows: winget install Gyan.FFmpeg · Linux: sudo apt install ffmpeg')
if ff:
    enc = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
    flt = subprocess.run(['ffmpeg', '-hide_banner', '-filters'], capture_output=True, text=True).stdout
    row('libx264' in enc, 'кодек libx264', 'нужна сборка ffmpeg с libx264 (brew/gyan.dev full)')
    row('libx265' in enc or 'hevc_videotoolbox' in enc, 'кодек HEVC (libx265 или VideoToolbox)', '(необязательно: только для HDR-мастера)')
    if not MAC:
        row(' zscale ' in flt or ' libplacebo ' in flt, 'zscale/libplacebo для HDR→SDR без Mac',
            '(необязательно) полная сборка ffmpeg (gyan.dev full / johnvansickle static)')
for mod, hint in [('numpy', 'pip install numpy'), ('playwright', 'pip install playwright && python3 -m playwright install chromium')]:
    try:
        importlib.import_module(mod)
        row(True, mod)
    except ImportError:
        row(False, mod, hint)
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        p.chromium.launch().close()
    row(True, 'Chromium для рендера графики')
except Exception as e:
    row(False, 'Chromium для рендера графики', 'python3 -m playwright install chromium')
w = None
for mod in ('mlx_whisper', 'faster_whisper', 'whisper'):
    try:
        importlib.import_module(mod)
        w = mod
        break
    except ImportError:
        pass
row(bool(w), f'whisper ({w or "нет"})', 'pip install mlx-whisper' if MAC and ARM else 'pip install faster-whisper')
if MAC:
    row(bool(shutil.which('swift') or shutil.which('swiftc')), 'Swift (HDR→SDR движком Apple)', 'xcode-select --install')
    row(bool(shutil.which('say')), 'say (демо-голос для selftest)', '(необязательно)')
else:
    print('· не macOS: HDR→SDR пойдёт через ffmpeg-тонмаппинг (цвет хуже, чем у Apple — предупреди автора)')
print('\nВсё готово ✓' if ok else '\nПоставь отмеченное ✗ и запусти проверку ещё раз.')
sys.exit(0 if ok else 1)
