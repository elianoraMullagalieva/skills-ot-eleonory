#!/usr/bin/env python3
"""Синтетическая «длинная запись с дублями» для проверки пайплайна (без чьих-либо личных видео).

  python3 make_demo.py <папка>   → demo_source.mp4 (речь с дублями, «погнали», «ещё раз», паузой внутри фразы)
                                    demo_screen.mp4 (5 с «записи экрана») и сценарий.txt
Голос: macOS — say (Milena), Linux — espeak-ng, иначе ошибка (whisper нечего будет распознать)."""
import os, platform, shutil, subprocess, sys

# дубли + служебные слова + пауза ВНУТРИ фразы «Сначала режем дубли, … потом добавляем графику»
TEXT = ('Погнали. [[slnc 700]] Привет, это тест монтажа. [[slnc 900]] Ещё раз. [[slnc 700]] '
        'Привет, это быстрый тест монтажа. [[slnc 900]] Сначала режем дубли, [[slnc 900]] потом добавляем графику. '
        '[[slnc 900]] Всё, готово.')
SCRIPT = ['Привет, это быстрый тест монтажа.', 'Сначала режем дубли, потом добавляем графику.', 'Всё, готово.']


def voice(out_wav):
    if platform.system() == 'Darwin' and shutil.which('say'):
        aiff = out_wav[:-4] + '.aiff'
        subprocess.run(['say', '-v', 'Milena', '-r', '170', '-o', aiff, TEXT], check=True)
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', aiff, '-ar', '48000', '-ac', '2', out_wav], check=True)
        os.remove(aiff)
        return
    esp = shutil.which('espeak-ng') or shutil.which('espeak')
    if esp:
        ssml = '<speak>' + TEXT.replace('[[slnc 700]]', '<break time="700ms"/>').replace('[[slnc 900]]', '<break time="900ms"/>') + '</speak>'
        subprocess.run([esp, '-v', 'ru', '-m', '-s', '150', '-w', out_wav, ssml], check=True)
        return
    sys.exit('Нет синтезатора речи: macOS — say, Linux — sudo apt install espeak-ng')


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(d, exist_ok=True)
    wav = os.path.join(d, 'demo_voice.wav')
    voice(wav)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav],
                               capture_output=True, text=True).stdout) + 0.6
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'testsrc2=s=1080x1920:r=30:d={dur:.2f}',
                    '-i', wav, '-af', 'apad', '-t', f'{dur:.2f}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28',
                    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                    '-c:a', 'aac', '-b:a', '192k', os.path.join(d, 'demo_source.mp4')], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'mandelbrot=s=1280x800:r=30', '-t', '5',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', os.path.join(d, 'demo_screen.mp4')], check=True)
    open(os.path.join(d, 'сценарий.txt'), 'w', encoding='utf-8').write('\n'.join(SCRIPT) + '\n')
    os.remove(wav)
    print(f'✓ demo_source.mp4 ({dur:.1f} с), demo_screen.mp4, сценарий.txt → {d}')


if __name__ == '__main__':
    main()
