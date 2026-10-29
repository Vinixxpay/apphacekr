from pathlib import Path
import os,json,subprocess,numpy as np
os.environ['HF_HOME']='/workspace/.cache/huggingface';os.environ['HF_HUB_DISABLE_XET']='1'
from faster_whisper import WhisperModel
r=Path(__file__).resolve().parents[1];m=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=3)
p=next((r/'input').rglob('*.m4a'));a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
ss,info=m.transcribe(a,language='pt',beam_size=5,word_timestamps=True,vad_filter=False)
rows=[]
for s in ss:
 print(s.start,s.end,s.text,flush=True);rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'text':w.word,'probability':w.probability} for w in s.words]})
(r/'work/client-medium.json').write_text(json.dumps({'duration':info.duration,'segments':rows},ensure_ascii=False,indent=2))
