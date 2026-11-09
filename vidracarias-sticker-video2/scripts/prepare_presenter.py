from pathlib import Path
import cv2,numpy as np,subprocess,json,math
r=Path(__file__).resolve().parents[1];plan=json.loads((r/'edit-plan.json').read_text());pub=r/'public/video';pub.mkdir(parents=True,exist_ok=True);cv2.setNumThreads(1)
# Sample-accurate original speech; retain all natural pauses in each kept take.
filters=[];labels=[]
for i,p in enumerate(plan['parts']):
 dur=p['end']-p['start'];filters.append(f"[0:a]atrim=start={p['start']}:end={p['end']},asetpts=PTS-STARTPTS,afade=t=in:d=0.003,afade=t=out:st={dur-.003}:d=0.003[a{i}]");labels.append(f'[a{i}]')
filters.append(''.join(labels)+f"concat=n={len(labels)}:v=0:a=1,highpass=f=65,lowpass=f=14500,loudnorm=I=-16:TP=-1.5:LRA=10,aresample=48000,apad,atrim=duration={plan['duration']}[a]")
subprocess.run(['ffmpeg','-v','error','-y','-i',str(r/'work/source.mkv'),'-filter_complex',';'.join(filters),'-map','[a]','-ac','2','-c:a','pcm_s16le',str(pub/'voice.wav')],check=True)
def encoder(name):return subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1036','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(pub/name)],stdin=subprocess.PIPE)
full=encoder('presenter.mp4');preview=encoder('presenter-preview.mp4');c=cv2.VideoCapture(str(r/'work/source.mkv'));face=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml');n=0;tracking=np.array([450.,805.]);lastscale=1.16;records=[]
sourceIndex=0
for part in plan['parts']:
 first=round(part['start']*30);last=round(part['end']*30)
 while sourceIndex<first:
  ok,discard=c.read();assert ok;sourceIndex+=1
 for srcn in range(first,last):
  ok,f=c.read();assert ok,(n,srcn);sourceIndex+=1
  t=n/30
  if n%12==0:
   small=cv2.resize(f,(540,960));boxes=face.detectMultiScale(cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),1.12,5,minSize=(65,65))
   if len(boxes):
    x,y,w,h=max(boxes,key=lambda z:z[2]*z[3]);target=np.array([(x+w/2)*2,(y+h*.41)*2]);tracking=tracking*.55+target*.45
   records.append({'frame':n,'sourceFrame':srcn,'eyeX':round(float(tracking[0]),1),'eyeY':round(float(tracking[1]),1)})
  z=[z for z in plan['zooms'] if z['start']<=t];current=z[-1] if z else {'scale':1.,'fast':False};goal=1.16*current['scale'];lastscale+=(goal-lastscale)*(.40 if current['fast'] else .10)
  cw=1080/lastscale;ch=1036/lastscale;cx=float(np.clip(tracking[0],cw/2,1080-cw/2));top=float(np.clip(tracking[1]-310/lastscale,0,1920-ch));cy=top+ch/2
  crop=cv2.getRectSubPix(f,(round(cw),round(ch)),(cx,cy));panel=cv2.resize(crop,(1080,1036),interpolation=cv2.INTER_LANCZOS4)
  full.stdin.write(panel.tobytes())
  if n<300:preview.stdin.write(panel.tobytes())
  if n==299:
   preview.stdin.close();assert preview.wait()==0;print('PREVIEW PRESENTER READY',flush=True)
  n+=1
  if n%300==0:print(n,'/',plan['frames'],flush=True)
full.stdin.close();assert full.wait()==0;assert n==plan['frames'],(n,plan['frames']);(r/'work/framing.json').write_text(json.dumps(records));print('FULL PRESENTER READY',flush=True)
