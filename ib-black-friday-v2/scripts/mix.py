from pathlib import Path
import json,numpy as np,soundfile as sf,subprocess
r=Path(__file__).resolve().parents[1];tl=json.loads((r/'public/timings-aligned.json').read_text());sr=48000
for v in tl:
 n=round(v['duration']*sr);t=np.arange(n)/sr;bed=np.zeros(n);fx=np.zeros(n);rng=np.random.default_rng(151+v['id']);beat=60/122;events=[]
 for k in range(int(v['duration']/beat)+1):
  at=k*beat;ids=(t>=at)&(t<at+.32);u=t[ids]-at;root=[55,65.406,73.416,61.735][(k//8)%4];freq=root*(2 if k%2 else 1);bed[ids]+=.017*(np.sin(2*np.pi*freq*u)+.28*np.sin(2*np.pi*freq*2*u))*np.exp(-u*10)*np.minimum(1,u/.007)
  ids=(t>=at)&(t<at+.19);u=t[ids]-at;bed[ids]+=.028*np.sin(2*np.pi*(48+44*np.exp(-u*35))*u)*np.exp(-u*24)*np.minimum(1,u/.003)
  if k%2:
   ids=(t>=at+.24)&(t<at+.31);u=t[ids]-at-.24;noise=rng.normal(0,.3,len(u));bed[ids]+=.008*noise*np.exp(-u*40)
 bed*=np.minimum(1,t/.25)*np.minimum(1,(v['duration']-t)/.8)*(.55+.45*np.minimum(1,t/max(1,v['cues']['price'])))
 def hit(at,kind):
  dur=.34 if kind=='impact' else .23 if kind=='tick' else .35;u=np.arange(round(sr*dur))/sr;z=np.zeros(len(u))
  if kind=='impact':z=.42*np.sin(2*np.pi*(47+60*np.exp(-u*35))*u)*np.exp(-u*18)+.16*rng.normal(0,.4,len(u))*np.exp(-u*35)
  elif kind=='tick':z=.20*np.sin(2*np.pi*920*u)*np.exp(-u*25)+.15*np.sin(2*np.pi*1380*u)*np.exp(-u*29)
  else:z=np.convolve(rng.normal(0,.3,len(u)),np.ones(9)/9,mode='same')*np.sin(np.pi*u/dur)**2
  z*=np.minimum(1,u/.003);st=round(at*sr);end=min(n,st+len(z));fx[st:end]+=.22*z[:end-st];events.append({'time':round(at,4),'kind':kind})
 hit(v['cues']['problem'],'whoosh');hit(v['cues']['black'],'whoosh');hit(v['cues']['price']-.2,'impact');hit(v['cues']['clock'],'whoosh');hit(v['cues']['twentyFour'],'tick');hit(v['cues']['cta'],'impact')
 # Short rising sweep stops at the exact reveal of 24H; no promotion countdown.
 start=v['cues']['clock'];stop=v['cues']['twentyFour'];ids=(t>=start)&(t<stop);u=(t[ids]-start)/max(.1,stop-start);fx[ids]+=.008*np.sin(2*np.pi*(170*(t[ids]-start)+450*(t[ids]-start)**2/max(.1,stop-start)))*u**1.7
 f=r/f'public/audio/{v["id"]}';sf.write(f/'bed.wav',bed,sr);sf.write(f/'effects.wav',fx,sr)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(f/'voice.wav'),'-i',str(f/'bed.wav'),'-i',str(f/'effects.wav'),'-filter_complex','[0:a]loudnorm=I=-15.5:TP=-2:LRA=8,aresample=48000[v];[v][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]','-map','[a]','-ar','48000','-ac','2',str(f/'mix.wav')],check=True);(f/'events.json').write_text(json.dumps(events,indent=2));print('MIX',v['id'],flush=True)
