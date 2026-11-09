from pathlib import Path
import os,json,subprocess,cv2,numpy as np
r=Path(__file__).resolve().parents[1];plan=json.loads((r/'edit-plan.json').read_text());cv2.setNumThreads(1)
source=Path(os.environ.get('VD1_PROXY',str(r/'work/source.mkv')))
if not source.exists():raise SystemExit('Prepare work/source.mkv from input/vd1.MOV first, or set VD1_PROXY to an existing 1080x1920/30fps proxy.')
pub=r/'public/video';pub.mkdir(exist_ok=True,parents=True)
voice=pub/'voice.wav'
if not voice.exists():
 fs=[];labels=[]
 for i,p in enumerate(plan['parts']):
  dur=p['end']-p['start'];fs.append(f"[0:a]atrim=start={p['start']}:end={p['end']},asetpts=PTS-STARTPTS,afade=t=in:d=0.003,afade=t=out:st={dur-.003}:d=0.003[a{i}]");labels.append(f'[a{i}]')
 fs.append(''.join(labels)+f"concat=n={len(labels)}:v=0:a=1,highpass=f=65,lowpass=f=14500,loudnorm=I=-16:TP=-1.5:LRA=10,aresample=48000,apad,atrim=duration={plan['duration']}[a]")
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-filter_complex',';'.join(fs),'-map','[a]','-ac','2','-c:a','pcm_s16le',str(voice)],check=True)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size','1080x1920','-framerate','30','-i','-','-an','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(pub/'picture.mp4')],stdin=subprocess.PIPE)
c=cv2.VideoCapture(str(source));face=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml');target=np.array([450.,805.]);tracking=target.copy();scale=1.22;n=0;records=[]
for part in plan['parts']:
 c.set(cv2.CAP_PROP_POS_FRAMES,round(part['start']*30))
 for si in range(round(part['start']*30),round(part['end']*30)):
  ok,f=c.read();assert ok,(n,si)
  if n%12==0:
   tiny=cv2.resize(f,(540,960));boxes=face.detectMultiScale(cv2.cvtColor(tiny,cv2.COLOR_BGR2GRAY),1.12,5,minSize=(65,65))
   if len(boxes):
    x,y,w,h=max(boxes,key=lambda z:z[2]*z[3]);target=np.array([(x+w/2)*2,(y+h*.41)*2])
    if n==0:tracking=target.copy()
  tracking+=(target-tracking)*.07
  cues=[z for z in plan['zooms'] if z['start']<=n/30];z=cues[-1] if cues else {'scale':1.,'fast':False}
  multiplier=1+(z['scale']-1)*.5;minimum=1350/max(820,1920-tracking[1]);goal=min(1.62,max(1.22*multiplier,minimum));scale+=(goal-scale)*(.24 if z['fast'] else .07)
  cw=1080/scale;ch=1920/scale;cx=float(np.clip(tracking[0],cw/2,1080-cw/2));top=float(np.clip(tracking[1]-570/scale,0,1920-ch));cy=top+ch/2
  crop=cv2.getRectSubPix(f,(round(cw),round(ch)),(cx,cy));frame=cv2.resize(crop,(1080,1920),interpolation=cv2.INTER_LANCZOS4);enc.stdin.write(frame.tobytes())
  if n in [30,180,900,2100]:cv2.imwrite(str(r/f'work/framing-{n}.jpg'),cv2.resize(frame,(540,960)))
  if n%300==0:print(n,'/',plan['frames'],flush=True)
  if n%15==0:records.append({'frame':n,'zoom':round(float(scale),3),'eyeX':round(float(tracking[0]),1),'eyeY':round(float(tracking[1]),1)})
  n+=1
enc.stdin.close();assert enc.wait()==0;assert n==plan['frames'];(r/'work/framing.json').write_text(json.dumps(records));print('PICTURE READY',flush=True)
