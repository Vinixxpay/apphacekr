from pathlib import Path
import json,wave,numpy as np,re,math
r=Path(__file__).resolve().parents[1];plans=json.loads((r/'plan.json').read_text())
fix={'Seba':'Saiba','Ceiba':'Saiba','preste':'preencha','IB':'iB','lides':'leads','milagroso':'milagrosos','agente':'agende'}
for p in plans:
 mf=r/'work'/f"{p['id']}-frames.json";m=json.loads(mf.read_text()) if mf.exists() else {'frames':math.ceil(p['duration']*30),'duration':math.ceil(p['duration']*30)/30};p['frames']=m['frames'];p['duration']=m['duration']
 audio=r/'public/video'/f"{p['id']}-voice.wav"
 if audio.exists():
  with wave.open(str(audio)) as w:
   a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32).reshape(-1,w.getnchannels()).mean(1)/32768;rate=w.getframerate()
  step=round(rate/25);p['wave']=[round(min(1.,float(np.sqrt(np.mean(a[i:i+step]**2)))*6),3) for i in range(0,len(a),step)]
 else:p['wave']=[0]*math.ceil(p['duration']*25)
 cues=[]
 for s in p['segments']:
  transcript=json.loads((r/'work'/f"{s['file']}-transcript.json").read_text())
  words=[]
  for t in transcript['segments']:
   for w in t['words']:
    if s['file']=='IMG_2203':
     z=w['start']
     if 29.47<=z<29.88 and w['text'].strip().strip(',.')=='é':continue
     if 32.25<=z<32.48:
      if z<32.34:w={**w,'text':'alinha','end':32.48}
      else:continue
     if 32.48<=z<32.97:w={**w,'text':'a expectativa.'}
     if 57.53<=z<57.70:w={**w,'text':'uma'}
     if 57.89<=z<58.10:continue
    if w['start']>=s['start']-.025 and w['end']<=s['end']+.025:
     raw=w['text'].strip();clean=re.sub(r'[,.:;!?]','',raw);text=raw.replace(clean,fix.get(clean,clean));words.append({'text':text,'start':round(s['from']+w['start']-s['start'],3),'end':round(s['from']+w['end']-s['start'],3)})
  if s['file']=='IMG_2200' and s['theme']=='swap':
   cues.append({'start':s['from']+.1,'end':s['from']+s['duration']-.1,'words':[{'text':'Cansado de trocar de gestor?','start':s['from'],'end':s['from']+s['duration']}]});continue
  group=[]
  for w in words:
   if group and (len(group)>=4 or len(' '.join(v['text'] for v in group))+len(w['text'])>31 or w['start']-group[-1]['end']>.42):
    cues.append({'start':group[0]['start'],'end':group[-1]['end']+.12,'words':group});group=[]
   group.append(w)
  if group:cues.append({'start':group[0]['start'],'end':min(s['from']+s['duration'],group[-1]['end']+.14),'words':group})
 for i,c in enumerate(cues[:-1]):c['end']=min(c['end'],cues[i+1]['start'])
 p['captions']=cues
(r/'src/data.ts').write_text('export const films='+json.dumps(plans,ensure_ascii=False,separators=(',',':'))+';\n')
print([(p['id'],p['frames'],len(p['captions'])) for p in plans])
