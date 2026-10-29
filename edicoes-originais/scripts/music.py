from pathlib import Path
import numpy as np,wave
r=Path(__file__).resolve().parents[1];rate=24000;duration=33;t=np.arange(rate*duration)/rate;out=np.zeros_like(t)
chords=[(130.8128,155.5635,195.9977),(103.8262,130.8128,155.5635),(87.3071,103.8262,130.8128),(97.9989,123.4708,146.8324)]
for n in range(11):
 st=n*3;end=min(duration,st+3.6);idx=(t>=st)&(t<end);u=t[idx]-st;env=np.minimum(1,u/.6)*np.minimum(1,(end-st-u)/.8)
 for hz in chords[n%4]:out[idx]+=.038*env*(np.sin(2*np.pi*hz*u)+.12*np.sin(2*np.pi*hz*2*u))
for b in range(55):
 st=b*.6;idx=(t>=st)&(t<st+.4);u=t[idx]-st;hz=chords[(b//5)%4][b%3]*2;out[idx]+=.035*np.sin(2*np.pi*hz*u)*np.exp(-u*11)*np.minimum(1,u/.012)
out*=np.minimum(1,t/.8)*np.minimum(1,(duration-t)/1.5)
with wave.open(str(r/'public/bed-original.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(out,-.95,.95)*32767).astype(np.int16).tobytes())
