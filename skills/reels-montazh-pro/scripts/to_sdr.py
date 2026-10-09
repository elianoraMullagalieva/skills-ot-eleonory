#!/usr/bin/env python3
"""iPhone HDR (Dolby Vision / HLG) → нормальный SDR-цвет без «пересвета» и бликов.

  python3 to_sdr.py IMG_3061.MOV                 → IMG_3061_SDR.mov (рядом с исходником)
  python3 to_sdr.py IMG_3061.MOV --capcut        → ещё IMG_3061_SDR_capcut.mp4 (H.264 8 бит)
  python3 to_sdr.py IMG_3061.MOV --out путь.mov

macOS: ТОЛЬКО движок Apple (sdr_apple.swift, AVAssetExportSession + композиция Rec.709) — как «Фото».
Windows/Linux: запасной вариант ffmpeg (zscale + tonemap), цвет хуже — предупреждаем.
Свой LUT не делаем. Разрешение не меняем (никогда не растягиваем выше исходного)."""
import argparse, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import probe, need, IS_MAC, HERE, SKILL, has_filter, video_codec_args, color_bsf


def apple(src, dst, codec='hevc'):
    swift = os.path.join(HERE, 'sdr_apple.swift')
    cache = os.path.join(SKILL, '_cache')
    binp = os.path.join(cache, 'sdr_apple')
    if not os.path.exists(binp) or os.path.getmtime(binp) < os.path.getmtime(swift):
        if shutil.which('swiftc'):
            os.makedirs(cache, exist_ok=True)
            r = subprocess.run(['swiftc', '-O', swift, '-o', binp], capture_output=True, text=True)
            if r.returncode:
                print('swiftc не собрал (запущу через swift):', r.stderr[-300:])
    cmd = [binp, src, dst, codec] if os.path.exists(binp) else ['swift', swift, src, dst, codec]
    if not shutil.which(cmd[0]) and not os.path.exists(cmd[0]):
        sys.exit('Нет Swift. Поставь инструменты разработчика: xcode-select --install')
    print('Apple-перевод HDR → SDR (это долго: ~реальное время для 4K)…')
    subprocess.run(cmd, check=True)


def ffmpeg_fallback(src, dst, info):
    print('⚠ ВНИМАНИЕ: не macOS — перевожу ffmpeg-тонмаппингом. Цвет будет чуть хуже, чем у Apple. '
          'Если есть Mac — лучше сделать там (to_sdr.py), или экспортировать из «Фото»/iPhone как «Наиболее совместимый».')
    trc = info['color_transfer']
    if has_filter('zscale'):
        vf = (f'zscale=t=linear:npl=203:tin={"arib-std-b67" if trc == "arib-std-b67" else "smpte2084"}:pin=bt2020:min=bt2020nc,'
              'format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0:peak=4,'
              'zscale=t=bt709:m=bt709:r=tv,format=yuv420p')
    elif has_filter('libplacebo'):
        vf = 'libplacebo=colorspace=bt709:color_primaries=bt709:color_trc=bt709:tonemapping=bt.2390:format=yuv420p'
    else:
        print('⚠ в этом ffmpeg нет zscale/libplacebo — только перевод матрицы без тонмаппинга (блики могут быть плоскими). '
              'Поставь полную сборку ffmpeg (gyan.dev full / johnvansickle static).')
        vf = 'scale=in_color_matrix=bt2020:out_color_matrix=bt709:in_range=tv:out_range=tv,format=yuv420p'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y', '-i', src, '-vf', vf]
                   + video_codec_args('h264', '60M')
                   + ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                      '-c:a', 'copy', dst], check=True)


def capcut(src, dst):
    """H.264 8 бит yuv420p, Rec.709, разрешение как у исходника — CapCut открывает без «файл повреждён»."""
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-stats', '-y'] + (['-hwaccel', 'videotoolbox'] if IS_MAC else [])
                   + ['-i', src] + video_codec_args('h264', '60M') + color_bsf(['h264'])
                   + ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
                      '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', dst], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src')
    ap.add_argument('--out')
    ap.add_argument('--capcut', action='store_true', help='ещё H.264 8-бит копия для CapCut')
    ap.add_argument('--h264', action='store_true', help='Apple-экспорт сразу в H.264 (иначе HEVC)')
    ap.add_argument('--force-ffmpeg', action='store_true', help='на Mac тоже ffmpeg (не рекомендуется)')
    a = ap.parse_args()
    need('ffmpeg')
    info = probe(a.src)
    stem = os.path.splitext(a.src)[0]
    dst = a.out or stem + '_SDR.mov'
    if not info.get('hdr'):
        print(f'Исходник уже SDR ({info.get("color_transfer") or "без меток"}) — перевод не нужен.')
        dst = a.src
    elif IS_MAC and not a.force_ffmpeg:
        apple(a.src, dst, 'h264' if a.h264 else 'hevc')
    else:
        ffmpeg_fallback(a.src, os.path.splitext(dst)[0] + '.mp4', info)
        dst = os.path.splitext(dst)[0] + '.mp4'
    o = probe(dst)
    print(f'✓ {dst}: {o["width"]}×{o["height"]}, {float(o["fps"]):.2f} fps, цвет {o["color_transfer"] or "bt709"}')
    if (o['width'], o['height']) != (info['width'], info['height']):
        print('⚠ размер изменился — проверь (растягивать выше исходника нельзя)')
    if a.capcut:
        c = os.path.splitext(dst)[0] + '_capcut.mp4'
        capcut(dst, c)
        print('✓ для CapCut:', c)


if __name__ == '__main__':
    main()
