from pathlib import Path
import json,numpy as np,soundfile as sf,subprocess,onnxruntime as ort
import kokoro_onnx
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text())
def session(p):
 s=ort.SessionOptions();s.intra_op_num_threads=4;s.inter_op_num_threads=1;return ort.InferenceSession(p,s,providers=['CPUExecutionProvider'])
kokoro_onnx.create_session=session;k=kokoro_onnx.Kokoro(str(r/'work/models/kokoro.onnx'),str(r/'work/models/voices.bin'))
result=[]
for video in cfg['videos']:
 i=video['id'];folder=r/f'public/audio/v{i}';folder.mkdir(parents=True,exist_ok=True);speed={1:1.06,2:1.08,3:1.14}[i]
 audio,sr=k.create(video['narration'],voice='pm_santa',speed=speed,lang='pt-br',sentence_pause=.15,clause_pause=.06)
 spoken=len(audio)/sr
 if spoken>32.1:
  speed=min(1.24,speed*spoken/31.6);audio,sr=k.create(video['narration'],voice='pm_santa',speed=speed,lang='pt-br',sentence_pause=.15,clause_pause=.06);spoken=len(audio)/sr
 if spoken>32.5:raise RuntimeError('Review copy or natural speech duration; do not cut words.')
 sf.write(folder/'speech.wav',audio,sr)
 duration=max({1:30.5,2:29.5,3:31.5}[i],spoken+2.55);frames=int(np.ceil(duration*30));duration=frames/30
 full=np.zeros(round(duration*sr),dtype=np.float64);offset=round(.16*sr);full[offset:offset+len(audio)]=audio;sf.write(folder/'voice.wav',full,sr)
 result.append({'id':i,'title':video['title'],'text':video['narration'],'voice':'Kokoro pm_santa, pt-br','nativeSpeed':round(speed,4),'speechStart':.16,'speechEnd':round(.16+spoken,4),'speechDuration':spoken,'fps':30,'frames':frames,'duration':duration})
 print('VIDEO',i,'speech',spoken,'duration',duration,'speed',speed,flush=True)
(r/'timings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));(r/'public/timings.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
