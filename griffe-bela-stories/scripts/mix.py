from pathlib import Path
import json,numpy as np,soundfile as sf,subprocess
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());sr=48000
for v in cfg['videos']:
 n=round(v['duration']*sr);time=np.arange(n)/sr;bed=np.zeros(n);fx=np.zeros(n);rng=np.random.default_rng(700+v['id']);beat=60/(108 if v['theme']=='wine' else 116)
 for k in range(int(v['duration']/beat)+1):
  start=k*beat;idx=(time>=start)&(time<start+1.3);u=time[idx]-start;chords=[[220,261.626,329.628,391.995],[174.614,220,261.626,329.628],[130.813,195.998,261.626,329.628],[195.998,246.942,293.665,391.995]];freq=chords[(k//4)%4][k%4]
  z=(np.sin(2*np.pi*freq*u)+.25*np.sin(2*np.pi*freq*2*u)+.1*np.sin(2*np.pi*freq*3*u))*np.exp(-u*4)*np.minimum(1,u/.012);bed[idx]+=.018*z
  if k%2==0:
   idx=(time>=start)&(time<start+.2);u=time[idx]-start;bed[idx]+=.013*np.sin(2*np.pi*(54+20*np.exp(-u*20))*u)*np.exp(-u*22)
 # Gentle ducking follows actual narration energy.
 voice,srate=sf.read(r/f'public/audio/{v["audio"]}/voice.wav');mono=voice.mean(axis=1) if voice.ndim>1 else voice;env=np.convolve(np.abs(mono),np.ones(2400)/2400,mode='same');duck=np.clip(1-env*7,.42,1);bed*=duck[:n]*np.minimum(1,time/.4)*np.minimum(1,(v['duration']-time)/.8)
 for at in [s['at'] for s in v['shots'][1:]]+[v['finalStart']]:
  u=np.arange(round(sr*.25))/sr;z=np.convolve(rng.normal(0,.3,len(u)),np.ones(11)/11,mode='same')*np.sin(np.pi*u/.25)**2;st=round(at*sr);end=min(n,st+len(z));fx[st:end]+=.045*z[:end-st]
 sf.write(r/f'public/audio/bed-{v["id"]}.wav',bed,sr);sf.write(r/f'public/audio/effects-{v["id"]}.wav',fx,sr)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(r/f'public/audio/{v["audio"]}/voice.wav'),'-i',str(r/f'public/audio/bed-{v["id"]}.wav'),'-i',str(r/f'public/audio/effects-{v["id"]}.wav'),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0[a]','-map','[a]','-ar','48000','-ac','2',str(r/f'public/audio/mix-{v["id"]}.wav')],check=True);print('MIX',v['id'],flush=True)
