from pathlib import Path
import json,numpy as np,soundfile as sf
r=Path(__file__).resolve().parents[1];e=json.loads((r/'edit.json').read_text());sr=48000;dur=e['duration'];n=int(dur*sr);rng=np.random.default_rng(24);a=np.zeros(n);fx=np.zeros(n)
def add(dst,at,v,g=1):
 i=int(at*sr);m=min(len(v),len(dst)-i)
 if i>=0 and m>0:dst[i:i+m]+=v[:m]*g
beat=60/120
for k,t0 in enumerate(np.arange(0,dur,beat)):
 t=np.arange(int(.25*sr))/sr
 if k%4 in (0,2):add(a,t0,np.sin(2*np.pi*(48*t+22*(1-np.exp(-t*40))/40))*np.exp(-t*20),.55)
 if k%4 in (1,3):
  noise=rng.normal(0,1,len(t));noise=np.r_[0,np.diff(noise)]
  add(a,t0,(noise*.3+np.sin(2*np.pi*180*t)*.35)*np.exp(-t*38),.3)
 for off in [0,.25]:
  th=np.arange(int(.045*sr))/sr;noise=rng.normal(0,1,len(th));noise=np.r_[0,np.diff(noise)]
  add(a,t0+off,noise*np.exp(-th*90),.055 if off==0 else .035)
 # Plucked minor arpeggio, soft and sparse.
 f=[261.63,311.13,392,466.16][k%4];tp=np.arange(int(.35*sr))/sr
 add(a,t0,np.sin(2*np.pi*f*tp)*np.exp(-tp*13)+.2*np.sin(4*np.pi*f*tp)*np.exp(-tp*18),.12)
 if k%2==0:
  tb=np.arange(int(.7*sr))/sr;f=[65.41,58.27,51.91,58.27][(k//8)%4]
  add(a,t0,np.sin(2*np.pi*f*tb)*np.minimum(tb/.015,1)*np.exp(-tb*4),.2)
# Short stereo-free effects remain beneath speech.
for at in [.05,1.1,e['outroStart']]:
 t=np.arange(int(.32*sr))/sr;noise=rng.normal(0,1,len(t));freq=np.fft.rfftfreq(len(t),1/sr);z=np.fft.rfft(noise);z*=np.exp(-((freq-2400)/1600)**2);noise=np.fft.irfft(z,len(t));add(fx,at,noise*np.sin(np.pi*t/.32)**2,.11)
for at in [10.6267,21.1667,e['outroStart']+1.6]:
 t=np.arange(int(.5*sr))/sr;add(fx,at,(np.sin(2*np.pi*1046.5*t)+.5*np.sin(2*np.pi*1568*t))*np.exp(-t*11),.06)
t=np.arange(n)/sr;gain=np.where((t<1.46)|(t>e['outroStart']),.15,.05)
a=a*gain+fx
fade=np.minimum(1,np.maximum(0,(dur-t)/.5));a*=fade
sf.write(r/'public/music-and-effects.wav',np.stack([a,a],axis=1),sr,subtype='PCM_16')
