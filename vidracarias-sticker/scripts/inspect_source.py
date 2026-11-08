from pathlib import Path
import subprocess,json,time,os,numpy as np
r=Path(__file__).resolve().parents[1]
while not list((r/'input').rglob('*.MOV')):time.sleep(2)
p=next((r/'input').rglob('*.MOV'))
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));(r/'work/probe.json').write_text(json.dumps(d,indent=2));print('SOURCE',d['format']['duration'],[(s['codec_type'],s.get('width'),s.get('height')) for s in d['streams']],flush=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-ar','16000','-ac','1',str(r/'work/source-16k.wav')],check=True)
os.environ['HF_HOME']='/workspace/.cache/huggingface';os.environ['HF_HUB_OFFLINE']='1'
from faster_whisper import WhisperModel
model=WhisperModel('medium',device='cpu',compute_type='int8',cpu_threads=3,local_files_only=True)
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/'work/source-16k.wav'),'-f','f32le','-']),np.float32)
ss,info=model.transcribe(audio,language='pt',beam_size=3,word_timestamps=True,vad_filter=True,vad_parameters={'min_silence_duration_ms':600})
rows=[]
for s in ss:
 row={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'text':w.word.strip(),'probability':w.probability} for w in s.words]};rows.append(row);print(s.start,s.end,s.text,flush=True)
(r/'work/transcript.json').write_text(json.dumps({'duration':info.duration,'segments':rows},ensure_ascii=False,indent=2));print('TRANSCRIPTION COMPLETE',flush=True)
