from pathlib import Path
import json,numpy as np,soundfile as sf,onnxruntime as ort
import kokoro_onnx
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text())
def session(p):
 s=ort.SessionOptions();s.intra_op_num_threads=4;s.inter_op_num_threads=1;return ort.InferenceSession(p,s,providers=['CPUExecutionProvider'])
kokoro_onnx.create_session=session;k=kokoro_onnx.Kokoro(str(r/'work/models/kokoro.onnx'),str(r/'work/models/voices.bin'));out=[]
for v in cfg['videos']:
 f=r/f'public/audio/{v["id"]}';f.mkdir(parents=True,exist_ok=True);chunks=[];cues={};pos=.12;sr=24000
 chunks.append(np.zeros(round(pos*sr)));segments=[]
 for kind,text in v['chunks']:
  gap=.28 if kind=='price' else .16 if kind=='clock' else .12 if kind=='cta' else .15
  if kind!='hook':chunks.append(np.zeros(round(gap*sr)));pos+=gap
  cues[kind]=pos
  tts=text.replace('iB Mídias','i bê Mídias').replace('Instagram','Instagrã').replace('Black Friday','Blék Fráidei');speed={'hook':1.0,'black':1.02,'price':.96,'clock':.98,'cta':1.0}[kind]
  phonemes=k.tokenizer.phonemize(tts,lang='pt-br')
  a,sr=k.create(phonemes,voice='pm_alex',speed=speed,lang='pt-br',is_phonemes=True,sentence_pause=.24,clause_pause=.10);start=pos;chunks.append(a);pos+=len(a)/sr;segments.append({'kind':kind,'start':start,'end':pos,'text':text,'nativeSpeed':speed,'synthesisText':tts,'phonemes':phonemes})
  sf.write(f'{f}/{kind}.wav',a,sr)
  if kind=='price' and pos-start<2.5:
   extra=2.5-(pos-start);chunks.append(np.zeros(round(extra*sr)));pos+=extra
 speechEnd=pos;duration=max(28.5,speechEnd+1.8,cues['cta']+3.2);frames=int(np.ceil(duration*30));duration=frames/30;voice=np.concatenate(chunks);voice=np.pad(voice,(0,max(0,round(duration*sr)-len(voice))));sf.write(f/'voice.wav',voice,sr)
 meta={'id':v['id'],'duration':duration,'frames':frames,'speechEnd':speechEnd,'cues':cues,'segments':segments,'voice':'Kokoro pm_alex pt-br','brandPronunciation':'i bê Mídias','text':v['narration']};out.append(meta);print('VOICE',v['id'],'duration',duration,'speech',round(speechEnd,2),'cues',cues,flush=True)
(r/'public/timings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
