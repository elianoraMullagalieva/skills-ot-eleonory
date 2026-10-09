#!/usr/bin/env python3
"""Расшифровка ролика со временем КАЖДОГО слова.
python3 transcribe.py ролик.mp4 [ru]   → печатает: [0.00-8.36] Слово@0.0 слово@0.6 …  и сохраняет ролик.words.json
Mac M1–M4: mlx-whisper (быстро). Иначе: faster-whisper."""
import sys,json,subprocess,tempfile,os
v=sys.argv[1];lang=sys.argv[2] if len(sys.argv)>2 else 'ru'
wav=os.path.join(tempfile.mkdtemp(),'a.wav')
subprocess.run(['ffmpeg','-v','error','-y','-i',v,'-ar','16000','-ac','1',wav],check=True)
segs=[]
try:
    import mlx_whisper
    r=mlx_whisper.transcribe(wav,path_or_hf_repo='mlx-community/whisper-large-v3-turbo',language=lang,word_timestamps=True)
    segs=[{'start':s['start'],'end':s['end'],'words':[{'w':w['word'].strip(),'t':w['start']} for w in s.get('words',[])]} for s in r['segments']]
except ImportError:
    from faster_whisper import WhisperModel
    m=WhisperModel('large-v3',compute_type='int8')
    it,_=m.transcribe(wav,language=lang,word_timestamps=True)
    segs=[{'start':s.start,'end':s.end,'words':[{'w':w.word.strip(),'t':w.start} for w in (s.words or [])]} for s in it]
segs=[s for s in segs if s['words']]
json.dump(segs,open(os.path.splitext(v)[0]+'.words.json','w'),ensure_ascii=False,indent=1)
for s in segs:print(f"[{s['start']:.2f}-{s['end']:.2f}] "+' '.join(f"{w['w']}@{w['t']:.1f}" for w in s['words']))
