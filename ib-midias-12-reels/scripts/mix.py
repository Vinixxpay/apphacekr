from pathlib import Path
import json,numpy as np,soundfile as sf,subprocess
r=Path(__file__).resolve().parents[1];tl=json.loads((r/'public/timings-aligned.json').read_text());sr=48000
for v in tl:
 folder=r/f'public/audio/{v["id"]:02d}';n=round(v['duration']*sr);t=np.arange(n)/sr;bed=np.zeros(n);fx=np.zeros(n);rng=np.random.default_rng(120+v['id']);events=[]
 for beat in range(int(v['duration']/.6)+1):
  st=beat*.6;idx=(t>=st)&(t<st+.4);u=t[idx]-st;hz=[196,246.94,293.66,246.94][beat%4];bed[idx]+=.007*np.sin(2*np.pi*hz*u)*np.exp(-u*14)*np.minimum(1,u/.012)
  if beat%2==0:
   idx=(t>=st)&(t<st+.15);u=t[idx]-st;bed[idx]+=.008*np.sin(2*np.pi*65*u)*np.exp(-u*24)
 bed*=np.minimum(1,t/.6)*np.minimum(1,(v['duration']-t)/1)
 for j,s in enumerate(v['scenes']):
  at=s['start']+.08;length=.23;u=np.arange(round(sr*length))/sr;z=rng.normal(0,.3,len(u));z=np.convolve(z,np.ones(9)/9,mode='same');z*=np.sin(np.pi*u/length)**2
  if s['layout'] in ['answerGate','formula','visit','offer','final']:z+=.35*np.sin(2*np.pi*880*u)*np.exp(-u*19)
  start=round(at*sr);end=min(n,start+len(z));fx[start:end]+=.045*z[:end-start];events.append({'time':round(at,3),'scene':s['layout']})
 sf.write(folder/'bed.wav',bed,sr);sf.write(folder/'effects.wav',fx,sr)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(folder/'voice.wav'),'-i',str(folder/'bed.wav'),'-i',str(folder/'effects.wav'),'-filter_complex','[0:a]loudnorm=I=-16:TP=-2:LRA=8,aresample=48000[v];[v][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]','-map','[a]','-ar','48000','-ac','2',str(folder/'mix.wav')],check=True)
 (folder/'effects.json').write_text(json.dumps(events,indent=2));print('MIX',v['id'],flush=True)
