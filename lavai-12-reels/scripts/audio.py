from pathlib import Path
import json,re,numpy as np,soundfile as sf,onnxruntime as ort
import kokoro_onnx
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());CTA='Toque em Saiba mais e responda ao quiz do Lavaí.'
def session(p):
 s=ort.SessionOptions();s.intra_op_num_threads=4;s.inter_op_num_threads=1;return ort.InferenceSession(p,s,providers=['CPUExecutionProvider'])
kokoro_onnx.create_session=session;k=kokoro_onnx.Kokoro(str(r/'work/models/kokoro.onnx'),str(r/'work/models/voices.bin'));out=[]
for v in cfg['videos']:
 folder=r/f'public/audio/{v["id"]:02d}';folder.mkdir(parents=True,exist_ok=True);meta=folder/'meta.json'
 if meta.exists() and json.loads(meta.read_text()).get('text')==v['narration'].replace('[pausa de 2 segundos]',''):
  data=json.loads(meta.read_text())
  if data['duration']<v['targetMin']:
   delta=v['targetMin']-data['duration'];voice,sr=sf.read(folder/'voice.wav');off=round(data['ctaStart']*sr);voice=np.concatenate([voice[:off],np.zeros(round(delta*sr)),voice[off:]]);sf.write(folder/'voice.wav',voice,sr);data['ctaStart']+=delta;data['speechEnd']+=delta;data['duration']=v['targetMin'];data['frames']=v['targetMin']*30;sf.write(folder/'speech.wav',voice[round(.15*sr):round(data['speechEnd']*sr)],sr);meta.write_text(json.dumps(data,ensure_ascii=False,indent=2))
  out.append(data);print('CACHED',v['id'],flush=True);continue
 body=v['narration'].removesuffix(CTA).strip();speed=.90
 def generate(speed):
  bodyToSpeak=body
  breaks={4:[('No Lavaí',.85),('Dá pra compartilhar',.85),('O cliente recebe',.85)],8:[('Esse número',.65),('No Lavaí',.65),('Dá pra comparar',.65)],12:[('Quanto você',.4),('Qual serviço',.4),('Se um cliente',.4)]}
  for phrase,seconds in breaks.get(v['id'],[]):bodyToSpeak=bodyToSpeak.replace(phrase,f'[leitura {seconds}] '+phrase)
  bodyToSpeak=bodyToSpeak.replace('[pausa de 2 segundos]','[quiz 2]');parts=re.split(r'(\[(?:leitura|quiz) [0-9.]+\])',bodyToSpeak);chunks=[];pauses=[];pos=.15
  for part in parts:
   if not part.strip():continue
   if part.startswith('['):
    seconds=float(re.search(r'[0-9.]+',part).group());chunks.append(np.zeros(round(sr*seconds)))
    if part.startswith('[quiz'):pauses.append({'start':round(pos,3),'end':round(pos+seconds,3)})
    pos+=seconds;continue
   a,sr=k.create(part.strip(),voice='pm_santa',speed=speed,lang='pt-br',sentence_pause=.28,clause_pause=.10);chunks.append(a);pos+=len(a)/sr
  return np.concatenate(chunks),sr,pauses
 main,sr,pauses=generate(speed);cta,sr=k.create(CTA,voice='pm_santa',speed=.93,lang='pt-br',sentence_pause=.20,clause_pause=.08)
 ctaStart=.15+len(main)/sr+.18;screenDuration=max(4,len(cta)/sr+.45);duration=ctaStart+screenDuration
 # Adjust native delivery, rather than stretching recorded audio, to the requested range.
 if duration<v['targetMin']-1 or duration>v['targetMax']:
  target=(v['targetMin']+min(v['targetMax'],v['targetMin']+2))/2
  desired=max(3,target-screenDuration-.33);newSpeed=max(.78,min(1.10,speed*(len(main)/sr)/desired));speed=round(newSpeed,3);main,sr,pauses=generate(speed);ctaStart=.15+len(main)/sr+.18;duration=ctaStart+screenDuration
 ctaStart=max(ctaStart,v['targetMin']-screenDuration);duration=ctaStart+screenDuration;frames=int(np.ceil(duration*30));duration=frames/30;voice=np.zeros(round(duration*sr));start=round(.15*sr);voice[start:start+len(main)]=main;off=round(ctaStart*sr);voice[off:off+len(cta)]=cta;speech=voice[start:off+len(cta)]
 sf.write(folder/'speech.wav',speech,sr);sf.write(folder/'voice.wav',voice,sr)
 data={'id':v['id'],'duration':duration,'frames':frames,'speechStart':.15,'speechEnd':ctaStart+len(cta)/sr,'ctaStart':ctaStart,'finalScreenDuration':duration-ctaStart,'text':v['narration'].replace('[pausa de 2 segundos]',''),'nativeSpeed':speed,'voice':'Kokoro pm_santa, pt-br','pauses':pauses};meta.write_text(json.dumps(data,ensure_ascii=False,indent=2));out.append(data);print('VOICE',v['id'],round(duration,2),'speed',speed,'CTA',round(ctaStart,2),flush=True)
(r/'public/timings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
