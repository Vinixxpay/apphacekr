from pathlib import Path
import subprocess,json
import cv2,numpy as np,onnxruntime as ort
r=Path(__file__).resolve().parents[1];pub=r/'public/video';work=r/'work';cv2.setNumThreads(1)
op=ort.SessionOptions();op.intra_op_num_threads=3;op.inter_op_num_threads=1
sess=ort.InferenceSession(str(work/'rvm.onnx'),op,providers=['CPUExecutionProvider'])
face=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
basefaces={'IMG_2196':(175,410,290),'IMG_2197':(190,470,325),'IMG_2200':(290,470,289),'IMG_2203':(220,280,390)}
for stem in ['IMG_2203','IMG_2200','IMG_2197','IMG_2196']:
 source=work/f'{stem}-proxy.mp4';pid='r2-'+stem[-4:];alpha=pub/f'{pid}-person.webm';audio=pub/f'{pid}-voice.wav';meta=work/f'{pid}-frames.json'
 if not audio.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vn','-af','highpass=f=75,lowpass=f=13500,loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','pcm_s16le',str(audio)],check=True)
 if alpha.exists() and meta.exists():continue
 dec=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(source),'-an','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size','540x800','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-crf','22','-b:v','0','-deadline','realtime','-cpu-used','5','-row-mt','1','-threads','2','-pix_fmt','yuva420p','-auto-alt-ref','0',str(alpha)],stdin=subprocess.PIPE)
 states=[np.zeros((1,1,1,1),np.float32) for _ in range(4)];n=0;tracking=np.array(basefaces[stem],float)
 while True:
  raw=dec.stdout.read(540*960*3)
  if len(raw)!=540*960*3:break
  rgb=np.frombuffer(raw,np.uint8).reshape(960,540,3);feed={'src':rgb.astype('float32').transpose(2,0,1)[None]/255,'downsample_ratio':np.array([.5],np.float32),**{f'r{i+1}i':v for i,v in enumerate(states)}}
  fgr,pha,*states=sess.run(None,feed);a=pha[0,0];fore=np.clip(fgr[0].transpose(1,2,0)*255,0,255).astype(np.uint8)
  if n%6==0:
   boxes=face.detectMultiScale(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY),scaleFactor=1.12,minNeighbors=5,minSize=(185,185))
   if len(boxes):
    x,y,w,h=max(boxes,key=lambda b:b[2]*b[3]);tracking=tracking*.78+np.array([x+w/2,y+h/2,w])*.22
  cx,cy,fw=tracking;scale=225/max(215,fw);tx=270-cx*scale;ty=240-cy*scale;rows=np.flatnonzero((a>.8).sum(axis=1)>18)
  if len(rows):ty=max(ty,55-rows[0]*scale)
  mat=np.array([[scale,0,tx],[0,scale,ty]],np.float32)
  fg=cv2.warpAffine(fore,mat,(540,800),flags=cv2.INTER_LINEAR);mask=cv2.warpAffine(a,mat,(540,800),flags=cv2.INTER_LINEAR)
  enc.stdin.write(np.dstack([fg,np.clip(mask*255,0,255).astype(np.uint8)]).tobytes());n+=1
  if n%300==0:print(pid,n,flush=True)
 enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
 meta.write_text(json.dumps({'frames':n,'duration':n/30}));print(pid,'completo',n,flush=True)
