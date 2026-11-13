from pathlib import Path
import os,json,numpy as np,soundfile as sf,subprocess,onnxruntime as ort,shutil
import kokoro_onnx
r=Path(__file__).resolve().parents[1]
def session(p):
 s=ort.SessionOptions();s.intra_op_num_threads=4;s.inter_op_num_threads=1;return ort.InferenceSession(p,s,providers=['CPUExecutionProvider'])
kokoro_onnx.create_session=session
k=kokoro_onnx.Kokoro(str(r/'work/models/kokoro.onnx'),str(r/'work/models/voices.bin'))
print('Portuguese voices:',[v for v in k.get_voices() if v.startswith('p')],flush=True)
scenes=json.loads((r/'roteiro.json').read_text());sr=24000;pieces=[];cursor=.18;pieces.append(np.zeros(round(cursor*sr),dtype=np.float32))
for i,s in enumerate(scenes):
 p=r/f'public/audio/scene-{i}.wav'
 if p.exists():audio,sr=sf.read(p,dtype='float32')
 else:
  audio,sr=k.create(s['text'],voice='pm_santa',speed=1.02,lang='pt-br',sentence_pause=.20,clause_pause=.08)
  sf.write(p,audio,sr)
 s['start']=round(cursor,4);s['speechDuration']=len(audio)/sr;pieces.append(audio);cursor+=len(audio)/sr
 # Small breathing space, without long empty beats.
 pause=.22 if i<len(scenes)-1 else 3.2
 pieces.append(np.zeros(round(pause*sr),dtype=np.float32));cursor+=pause;s['end']=round(cursor,4)
 print(i,s['start'],s['end'],s['text'],flush=True)
voice=np.concatenate(pieces);sf.write(r/'public/audio/voice.wav',voice,sr)
# Quiet original electronic bed, ducked under narration, plus short transition accents.
rate=48000;dur=len(voice)/sr;t=np.arange(round(dur*rate))/rate;music=np.zeros_like(t)
chords=[[130.8128,164.8138,195.9977],[110,130.8128,164.8138],[87.3071,110,130.8128],[97.9989,123.4708,146.8324]]
for beat in range(int(dur/.6)+1):
 st=beat*.6;mask=(t>=st)&(t<st+.5);u=t[mask]-st;hz=chords[(beat//8)%4][beat%3]*2
 music[mask]+=.010*np.sin(2*np.pi*hz*u)*np.exp(-u*12)*np.minimum(1,u/.02)
 if beat%2==0:
  mask=(t>=st)&(t<st+.17);u=t[mask]-st;music[mask]+=.012*np.sin(2*np.pi*(58*u+12*(1-np.exp(-u*28))/28))*np.exp(-u*25)
for i in range(int(dur/4.8)+1):
 st=i*4.8;en=min(dur,st+5.1);mask=(t>=st)&(t<en);u=t[mask]-st;env=np.minimum(1,u/.7)*np.minimum(1,(en-st-u)/.8)
 for hz in chords[i%4]:music[mask]+=.004*env*np.sin(2*np.pi*hz*u)
music*=np.minimum(1,t/.7)*np.minimum(1,(dur-t)/1.2)
rng=np.random.default_rng(47)
for s in scenes[1:]:
 at=s['start'];mask=(t>=at-.12)&(t<at+.15);u=t[mask]-(at-.12);noise=rng.normal(0,.008,len(u));music[mask]+=np.convolve(noise,np.ones(9)/9,mode='same')*np.sin(np.pi*u/.27)**2
sf.write(r/'public/audio/bed.wav',music,rate)
delay=round((scenes[-1]['start']+scenes[-1]['speechDuration']+.16)*1000)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(r/'public/audio/voice.wav'),'-i',str(r/'public/audio/bed.wav'),'-i',str(r/'public/audio/brand-sound.wav'),'-filter_complex',f'[0:a]loudnorm=I=-16:TP=-2:LRA=8,aresample=48000[v];[2:a]volume=0.65,adelay={delay}|{delay}[fx];[v][1:a][fx]amix=inputs=3:duration=first:normalize=0[a]','-map','[a]','-ar','48000','-ac','2',str(r/'public/audio/mix.wav')],check=True)
frames=int(np.ceil(dur*30));scenes[-1]['end']=frames/30
(r/'timeline.json').write_text(json.dumps({'fps':30,'frames':frames,'duration':frames/30,'voice':'Kokoro pm_santa, Brazilian Portuguese, generated speech','scenes':scenes},ensure_ascii=False,indent=2))
print('VOICE READY',frames/30,flush=True)

shutil.copyfile(r/'public/audio/mix.wav',r/'work/base-mix.wav')
