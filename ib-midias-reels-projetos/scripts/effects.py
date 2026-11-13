from pathlib import Path
import numpy as np,soundfile as sf,json,shutil,unicodedata,re
r=Path(__file__).resolve().parents[1];tl=json.loads((r/'timeline.json').read_text());sr=48000;base=r/'work/base-mix.wav'
if not base.exists():shutil.copyfile(r/'public/audio/mix.wav',base)
audio,rate=sf.read(base);assert rate==sr;n=len(audio);fx=np.zeros(n);events=[];rng=np.random.default_rng(53)
def sound(at,kind,gain=.04):
 length={'ring':.50,'tool':.16,'coin':.32,'notification':.36,'click':.09,'impact':.25,'tick':.045,'pop':.12}.get(kind,.18);t=np.arange(round(length*sr))/sr
 if kind in ['coin','tool']:
  v=(np.sin(2*np.pi*1870*t)+.5*np.sin(2*np.pi*2730*t))*np.exp(-t*(24 if kind=='tool' else 14))*np.minimum(1,t/.002)
 elif kind in ['ring','notification']:
  v=np.sin(2*np.pi*np.where(t<length*.45,740,988)*t)*np.exp(-((t%(length*.5))/(length*.5)))*np.minimum(1,t/.008)*np.minimum(1,(length-t)/.02)
 elif kind=='impact':v=np.sin(2*np.pi*(70*t+45*t*t))*np.exp(-t*16)*np.minimum(1,t/.008)
 elif kind=='pop':v=np.sin(2*np.pi*(360*t-900*t*t))*np.exp(-t*32)*np.minimum(1,t/.004)
 else:v=rng.normal(0,.7,len(t))*np.exp(-t*70)*np.minimum(1,t/.002)
 start=round(at*sr);stop=min(n,start+len(v));fx[start:stop]+=gain*v[:stop-start];events.append({'time':round(at,3),'type':kind,'gain':gain})
s=tl['scenes'];sound(s[0]['start']+.02,'impact',.07);sound(s[0]['start']+.7,'ring',.03)
for d in [1.65,2.5]:sound(s[0]['start']+d,'tool',.045)
for d in np.arange(.3,3.8,.45):sound(s[1]['start']+float(d),'tick',.009)
sound(s[1]['start']+5.7,'coin',.035);sound(s[2]['start'],'impact',.06);sound(s[2]['start']+3,'coin',.025)
for d in [4.4,5.5,6.4]:sound(s[3]['start']+d,'tool',.025)
sound(s[3]['start']+8.1,'coin',.025);sound(s[4]['start']+6.35,'notification',.055)
for d in [2.25,3,3.75,4.5,5.25]:sound(s[5]['start']+d,'pop',.024)
caps=json.loads((r/'public/captions.json').read_text());words=[w for c in caps for w in c['words']]
click=next((w['start'] for w in words if w['text'].lower().strip(',.!?')=='clique' and w['start']>s[-1]['start']),s[-1]['start']+8)
sound(click,'click',.045)
full=audio+fx[:,None];assert np.max(np.abs(full))<.98
sf.write(r/'public/audio/effects.wav',fx,sr);sf.write(r/'public/audio/mix.wav',full,sr);(r/'sound-events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2));print('SYNCED EFFECTS',len(events),'events',float(np.max(np.abs(full))))
