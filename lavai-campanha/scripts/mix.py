from pathlib import Path
import json,numpy as np,soundfile as sf,subprocess
r=Path(__file__).resolve().parents[1];tl=json.loads((r/'timings.json').read_text());sr=48000
for v in tl:
 i=v['id'];folder=r/f'public/audio/v{i}';n=round(v['duration']*sr);t=np.arange(n)/sr;bed=np.zeros(n);fx=np.zeros(n);events=[];rng=np.random.default_rng(110+i)
 for beat in range(int(v['duration']/.55)+1):
  st=beat*.55;idx=(t>=st)&(t<st+.4);u=t[idx]-st;hz=[164.8138,195.9977,246.9417,195.9977][beat%4];bed[idx]+=.009*np.sin(2*np.pi*hz*u)*np.exp(-u*15)*np.minimum(1,u/.012)
  if beat%2==0:
   idx=(t>=st)&(t<st+.15);u=t[idx]-st;bed[idx]+=.011*np.sin(2*np.pi*62*u)*np.exp(-u*25)
 bed*=np.minimum(1,t/.5)*np.minimum(1,(v['duration']-t)/.8)
 def hit(at,kind,gain=.035):
  if at<0 or at>=v['duration']:return
  length={'ring':.42,'coin':.22,'whoosh':.32,'tap':.08,'notify':.29,'paper':.2}[kind];u=np.arange(round(sr*length))/sr
  if kind in ['coin','notify']:z=(np.sin(2*np.pi*(1150 if kind=='coin' else 880)*u)+.3*np.sin(2*np.pi*1710*u))*np.exp(-u*16)*np.minimum(1,u/.003)
  elif kind=='ring':z=np.sin(2*np.pi*740*u)*(.5+.5*np.sin(2*np.pi*13*u))*np.exp(-u*6)
  else:
   z=rng.normal(0,.6,len(u));z=np.convolve(z,np.ones(7 if kind=='whoosh' else 3)/(7 if kind=='whoosh' else 3),mode='same');z*=np.sin(np.pi*u/length)**2
  start=round(at*sr);end=min(n,start+len(z));fx[start:end]+=gain*z[:end-start];events.append({'time':round(at,3),'kind':kind})
 hit(.2,'whoosh',.05)
 if i==1:
  hit(4.9,'paper');hit(6.8,'coin');hit(8.8,'paper')
 elif i==2:
  for at in [.8,1.6,2.5,3.3]:hit(at,'paper' if at<2 else 'tap')
  hit(4.5,'whoosh')
 else:
  hit(3.2,'ring');hit(5.2,'paper');hit(9,'paper')
 c=v['cues'];intro=max(5.2,c['imagine']) if i==2 else c['intro'];hit(intro,'whoosh',.055);hit(intro+.6,'tap');hit(c['services']+.2,'tap')
 if i>1:hit(c['receipt']+.5,'notify',.035)
 hit(c['price'],'coin',.045);hit(c['cta'],'tap',.05)
 sf.write(folder/'bed.wav',bed,sr);sf.write(folder/'effects.wav',fx,sr)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(folder/'voice.wav'),'-i',str(folder/'bed.wav'),'-i',str(folder/'effects.wav'),'-filter_complex','[0:a]loudnorm=I=-16:TP=-2:LRA=8,aresample=48000[v];[v][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]','-map','[a]','-ar','48000','-ac','2',str(folder/'mix.wav')],check=True)
 (r/f'sound-events-{i}.json').write_text(json.dumps(events,indent=2));print('MIX READY',i,len(events),'events',flush=True)
