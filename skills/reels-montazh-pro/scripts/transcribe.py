#!/usr/bin/env python3
"""Расшифровка с временем и «уверенностью» КАЖДОГО слова (whisper).

  python3 transcribe.py запись.MOV                → запись.words.json + запись.transcript.txt
  python3 transcribe.py ролик.mp4 --lang ru --words-js words.js   (+ слова для движка графики)

Движок: Mac M1–M4 → mlx-whisper (large-v3-turbo, быстро); иначе faster-whisper; иначе openai-whisper.
words.json: [{start,end,text,words:[{word,start,end,probability}]}] — probability нужна pick_takes.py.
transcript.txt: строки «[12.3] слово@12.3 слово@12.8 …» — по ним пишется план нарезки."""
import argparse, json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import need


def _wav(path):
    need('ffmpeg')
    wav = os.path.join(tempfile.mkdtemp(), 'a.wav')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', path, '-vn', '-ar', '16000', '-ac', '1', wav], check=True)
    return wav


def transcribe(path, lang='ru', model=None, prompt=None):
    wav = _wav(path)
    try:
        import mlx_whisper
        r = mlx_whisper.transcribe(wav, path_or_hf_repo=model or 'mlx-community/whisper-large-v3-turbo',
                                   language=lang, word_timestamps=True, initial_prompt=prompt,
                                   condition_on_previous_text=False)
        segs = [{'start': s['start'], 'end': s['end'], 'text': s['text'].strip(),
                 'words': [{'word': w['word'].strip(), 'start': w['start'], 'end': w['end'],
                            'probability': round(float(w.get('probability', 1)), 3)} for w in s.get('words', [])]}
                for s in r['segments']]
        return [s for s in segs if s['words']]
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(model or 'large-v3', compute_type='int8')
        it, _ = m.transcribe(wav, language=lang, word_timestamps=True, initial_prompt=prompt,
                             condition_on_previous_text=False)
        segs = [{'start': s.start, 'end': s.end, 'text': s.text.strip(),
                 'words': [{'word': w.word.strip(), 'start': w.start, 'end': w.end,
                            'probability': round(float(w.probability), 3)} for w in (s.words or [])]} for s in it]
        return [s for s in segs if s['words']]
    except ImportError:
        pass
    try:
        import whisper
        m = whisper.load_model(model or 'large-v3')
        r = m.transcribe(wav, language=lang, word_timestamps=True, initial_prompt=prompt,
                         condition_on_previous_text=False)
        segs = [{'start': s['start'], 'end': s['end'], 'text': s['text'].strip(),
                 'words': [{'word': w['word'].strip(), 'start': w['start'], 'end': w['end'],
                            'probability': round(float(w.get('probability', 1)), 3)} for w in s.get('words', [])]}
                for s in r['segments']]
        return [s for s in segs if s['words']]
    except ImportError:
        sys.exit('Нет whisper. Mac M1–M4: `pip install mlx-whisper`; Windows/Linux/Intel: `pip install faster-whisper`.')


def lines(segs):
    return [f"[{s['start']:.1f}] " + ' '.join(f"{w['word']}@{w['start']:.2f}" for w in s['words']) for s in segs]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('media')
    ap.add_argument('--lang', default='ru')
    ap.add_argument('--model', help='модель whisper (по умолчанию large-v3-turbo / large-v3)')
    ap.add_argument('--prompt', help='подсказка whisper: имена, термины («Claude Code, CapCut, Figma»)')
    ap.add_argument('--out', help='куда words.json (по умолчанию <файл>.words.json)')
    ap.add_argument('--words-js', help='ещё и words.js для движка графики: window.SPEECH=[[слово,сек],…]')
    ap.add_argument('--offset', type=float, default=0, help='прибавить к временам в words.js (второй исходник = 1000)')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    segs = transcribe(a.media, a.lang, a.model, a.prompt)
    base = os.path.splitext(a.media)[0]
    out = a.out or base + '.words.json'
    json.dump(segs, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    txt = os.path.splitext(out)[0].replace('.words', '') + '.transcript.txt'
    open(txt, 'w', encoding='utf-8').write('\n'.join(lines(segs)) + '\n')
    if a.words_js:
        ws = [[w['word'], round(w['start'] + a.offset, 3)] for s in segs for w in s['words']]
        open(a.words_js, 'w', encoding='utf-8').write('/* слова речи: [слово, секунда исходника] — для W(\'слово\') в сценах */\nwindow.SPEECH=(window.SPEECH||[]).concat(' + json.dumps(ws, ensure_ascii=False) + ');\n')
    if not a.quiet:
        print('\n'.join(lines(segs)))
    print(f'слов: {sum(len(s["words"]) for s in segs)} → {out}, {txt}' + (f', {a.words_js}' if a.words_js else ''))


if __name__ == '__main__':
    main()
