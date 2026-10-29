from pathlib import Path
import os,json,subprocess,numpy as np
os.environ['HF_HOME']='/workspace/.cache/huggingface'
os.environ['HF_HUB_DISABLE_XET']='1'
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[1]
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,num_workers=1)
for p in sorted((root/'input').rglob('*.mov')):
 target=root/'work'/f'{p.stem}-transcript.json'
 if target.exists():continue
 audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
 segments,info=model.transcribe(audio,language='pt',beam_size=5,word_timestamps=True,vad_filter=True,condition_on_previous_text=False,initial_prompt='iB Mídias. Tráfego pago. Anúncios. Vidraçaria. Pernambuco. Seiscentos reais.')
 result=[]
 for s in segments:
  d={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'text':w.word,'probability':w.probability} for w in s.words]};result.append(d);print(p.name,round(s.start,2),round(s.end,2),s.text,flush=True)
 target.write_text(json.dumps({'file':p.name,'duration':info.duration,'segments':result},ensure_ascii=False,indent=2))
