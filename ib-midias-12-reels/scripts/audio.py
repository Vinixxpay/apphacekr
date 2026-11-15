from pathlib import Path
import json,re,numpy as np,soundfile as sf,onnxruntime as ort
import kokoro_onnx
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text())
def session(p):
 s=ort.SessionOptions();s.intra_op_num_threads=4;s.inter_op_num_threads=1;return ort.InferenceSession(p,s,providers=['CPUExecutionProvider'])
kokoro_onnx.create_session=session;k=kokoro_onnx.Kokoro(str(r/'work/models/kokoro.onnx'),str(r/'work/models/voices.bin'));out=[]
for v in cfg['videos']:
 folder=r/f'public/audio/{v["id"]:02d}';folder.mkdir(parents=True,exist_ok=True)
 meta=folder/'meta.json'
 if meta.exists() and json.loads(meta.read_text()).get('nativeSpeed')==.93:out.append(json.loads(meta.read_text()));print('CACHED',v['id'],flush=True);continue
 parts=re.split(r'\[pausa de 2 segundos\]',v['narration']);speed=.93;chunks=[];pauses=[];pos=.15
 for j,part in enumerate(parts):
  tts=part.strip().replace('Comenta A pra','Comenta á, pra').replace('ou B pra','ou bê, pra')
  a,sr=k.create(tts,voice='pm_santa',speed=speed,lang='pt-br',sentence_pause=.30,clause_pause=.12)
  chunks.append(a);pos+=len(a)/sr
  if j<len(parts)-1:pauses.append({'start':round(pos,3),'end':round(pos+2,3)});chunks.append(np.zeros(sr*2));pos+=2
 speech=np.concatenate(chunks);duration=.15+len(speech)/sr+3;frames=int(np.ceil(duration*30));duration=frames/30
 voice=np.zeros(round(duration*sr));voice[round(.15*sr):round(.15*sr)+len(speech)]=speech
 sf.write(folder/'speech.wav',speech,sr);sf.write(folder/'voice.wav',voice,sr)
 data={'id':v['id'],'duration':duration,'frames':frames,'speechStart':.15,'speechEnd':.15+len(speech)/sr,'text':v['narration'].replace('[pausa de 2 segundos]',''),'nativeSpeed':speed,'voice':'Kokoro pm_santa, pt-br','pauses':pauses};meta.write_text(json.dumps(data,ensure_ascii=False,indent=2));out.append(data);print('VOICE',v['id'],round(duration,2),'speech end',round(data['speechEnd'],2),'pauses',pauses,flush=True)
(r/'public/timings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
