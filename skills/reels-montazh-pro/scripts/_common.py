"""Общие функции скилла reels-montazh-pro: ffprobe, загрузка звука, выбор кодеков.
Работает на macOS, Linux и Windows (нужны ffmpeg/ffprobe в PATH)."""
import json, os, platform, shutil, subprocess, sys
from fractions import Fraction

IS_MAC = platform.system() == 'Darwin'
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def need(tool):
    if not shutil.which(tool):
        sys.exit(f'Не найден {tool}. Поставь ffmpeg: macOS — `brew install ffmpeg`, '
                 f'Windows — `winget install ffmpeg`, Linux — `sudo apt install ffmpeg`.')


def probe(path):
    """Размер, fps, длительность и цветовые метки первого видеопотока."""
    need('ffprobe')
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', path],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'ffprobe не открыл {path}: {r.stderr.strip()}')
    d = json.loads(r.stdout)
    v = next((s for s in d['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    info = {'duration': float(d['format'].get('duration', 0)), 'has_audio': a is not None}
    if v:
        w, h = int(v['width']), int(v['height'])
        rot = 0
        for sd in v.get('side_data_list', []) or []:
            if 'rotation' in sd:
                rot = int(float(sd['rotation']))
        rot = int(v.get('tags', {}).get('rotate', rot) or rot)
        if abs(rot) % 180 == 90:          # iPhone пишет горизонталь + поворот
            w, h = h, w
        fr = v.get('avg_frame_rate') or v.get('r_frame_rate') or '30/1'
        try:
            fps = Fraction(fr)
        except (ValueError, ZeroDivisionError):
            fps = Fraction(30)
        if fps == 0:
            fps = Fraction(v.get('r_frame_rate', '30/1'))
        trc = v.get('color_transfer', '') or ''
        info.update(width=w, height=h, fps=fps, codec=v.get('codec_name'),
                    pix_fmt=v.get('pix_fmt', ''), color_primaries=v.get('color_primaries', ''),
                    color_transfer=trc, color_space=v.get('color_space', ''),
                    hdr=trc in ('arib-std-b67', 'smpte2084'),
                    dolby_vision=any('dovi' in json.dumps(sd).lower() or 'dolby' in json.dumps(sd).lower()
                                     for sd in v.get('side_data_list', []) or []))
    return info


def nice_fps(fps):
    """Приводит «грязные» средние fps iPhone (59.98, 29.97…) к ближайшему стандарту (точная дробь)."""
    f = float(fps)
    std = [Fraction(24000, 1001), Fraction(24), Fraction(25), Fraction(30000, 1001), Fraction(30), Fraction(50),
           Fraction(60000, 1001), Fraction(60), Fraction(120)]
    best = min(std, key=lambda s: abs(float(s) - f))
    return best if abs(float(best) - f) < 0.3 else Fraction(round(f))


def load_audio(path, sr=16000, cache_dir=None):
    """Моно float32 звук файла (numpy). Кэширует в .npy рядом с планом."""
    import numpy as np
    need('ffmpeg')
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        st = os.stat(path)
        key = f'{os.path.basename(path)}.{sr}.{int(st.st_size)}.{int(st.st_mtime)}.npy'
        cp = os.path.join(cache_dir, key)
        if os.path.exists(cp):
            return np.load(cp)
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', path, '-vn', '-ac', '1', '-ar', str(sr),
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    if cache_dir:
        np.save(cp, a)
    return a


def encoders():
    r = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True)
    return r.stdout


def has_filter(name):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-filters'], capture_output=True, text=True)
    return any(line.split()[1:2] == [name] for line in r.stdout.splitlines() if len(line.split()) > 1)


def video_codec_args(kind, bitrate=None):
    """kind: 'h264' (8 бит, для CapCut/телефона), 'hevc10' (10 бит мастер), 'preview'.
    На Mac — аппаратные кодеки VideoToolbox, иначе libx264/libx265."""
    enc = encoders()
    hw = IS_MAC and 'videotoolbox' in enc
    if kind in ('h264', 'preview'):
        br = bitrate or ('12M' if kind == 'preview' else '60M')
        if hw:
            return ['-c:v', 'h264_videotoolbox', '-profile:v', 'high', '-b:v', br, '-pix_fmt', 'yuv420p', '-tag:v', 'avc1']
        return ['-c:v', 'libx264', '-preset', 'medium', '-crf', '23' if kind == 'preview' else '16',
                '-pix_fmt', 'yuv420p', '-profile:v', 'high']
    if kind == 'hevc10':
        br = bitrate or '100M'
        if hw:
            return ['-c:v', 'hevc_videotoolbox', '-profile:v', 'main10', '-pix_fmt', 'p010le', '-b:v', br, '-tag:v', 'hvc1']
        if 'libx265' in enc:
            return ['-c:v', 'libx265', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p10le', '-tag:v', 'hvc1']
        print('⚠ libx265 нет — пишу H.264 8 бит (HDR так не сохранить).')
        return video_codec_args('h264', bitrate)
    raise ValueError(kind)


def color_args(info):
    """Цветовые метки на выход = как у исходника (HDR остаётся HDR, SDR — Rec.709)."""
    if info.get('hdr'):
        return ['-color_primaries', 'bt2020', '-color_trc', info['color_transfer'], '-colorspace', 'bt2020nc', '-color_range', 'tv']
    return ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv']


def color_bsf(codec_args, info=None):
    """Пишет цветовые метки прямо в поток (VideoToolbox иногда их не ставит → плееры гадают цвет)."""
    c = ' '.join(codec_args)
    hdr = bool(info and info.get('hdr'))
    trc = 18 if hdr and info.get('color_transfer') == 'arib-std-b67' else (16 if hdr else 1)
    pm = '9' if hdr else '1'
    kv = f'colour_primaries={pm}:transfer_characteristics={trc}:matrix_coefficients={pm}'
    if 'h264' in c or 'libx264' in c:
        return ['-bsf:v', 'h264_metadata=' + kv]
    if 'hevc' in c or 'libx265' in c:
        return ['-bsf:v', 'hevc_metadata=' + kv]
    return []


def hwdec():
    return ['-hwaccel', 'videotoolbox'] if IS_MAC else []


def words_from_json(path, offset=0.0):
    """Плоский список слов из words.json (формат transcribe.py / whisper)."""
    d = json.load(open(path, encoding='utf-8'))
    segs = d['segments'] if isinstance(d, dict) else d
    out = []
    for s in segs:
        for w in s.get('words', []):
            word = (w.get('word') or w.get('w') or '').strip()
            st = float(w.get('start', w.get('t', 0)))
            en = float(w.get('end', st + 0.3))
            out.append({'word': word, 'start': st + offset, 'end': en + offset,
                        'probability': float(w.get('probability', 1.0))})
    out.sort(key=lambda w: w['start'])
    return out


def norm(s):
    import re
    s = s.lower().replace('ё', 'е')
    return re.sub(r'[^\w\s]', ' ', s).split()
