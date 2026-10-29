from pathlib import Path
import json,subprocess,os,time,wave
import cv2,numpy as np,onnxruntime as ort
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'work';PUB=ROOT/'public/video';PUB.mkdir(parents=True,exist_ok=True)
plans=json.loads((ROOT/'plan.json').read_text());cv2.setNumThreads(1)
def run(a):subprocess.run(a,check=True)
for src in sorted((ROOT/'input').rglob('*.mov')):
 out=WORK/f'{src.stem}-proxy.mp4'
 if out.exists():continue
 print('Proxy',src.name,flush=True)
 run(['ffmpeg','-v','error','-y','-threads','2','-i',str(src),'-vf','scale=540:960:flags=lanczos,fps=30','-c:v','libx264','-preset','fast','-crf','15','-threads','2','-c:a','aac','-b:a','256k','-movflags','+faststart',str(out)])
options=ort.SessionOptions();options.intra_op_num_threads=3;options.inter_op_num_threads=1
session=ort.InferenceSession(str(WORK/'rvm.onnx'),options,providers=['CPUExecutionProvider'])
face=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
basefaces={'IMG_2196':(175,410,290),'IMG_2197':(190,470,325),'IMG_2200':(290,470,289),'IMG_2203':(220,280,390)}
for plan in plans:
 pid=plan['id'];base=WORK/f'{pid}-edit.mp4';alpha=PUB/f'{pid}-person.webm';audio=PUB/f'{pid}-voice.wav'
 if not base.exists():
  args=['ffmpeg','-v','error','-y','-filter_complex_threads','2'];filters=[];pairs=[]
  for i,s in enumerate(plan['segments']):
   args+=['-threads','1','-i',str(WORK/f"{s['file']}-proxy.mp4")]
   filters += [f"[{i}:v]trim=start={s['start']}:end={s['end']},setpts=PTS-STARTPTS,fps=30[v{i}]",f"[{i}:a]atrim=start={s['start']}:end={s['end']},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={max(0,s['duration']-.01)}:d=0.01[a{i}]"]
   pairs += [f'[v{i}][a{i}]']
  filters += [''.join(pairs)+f"concat=n={len(plan['segments'])}:v=1:a=1[vc][ac]",'[vc]tpad=stop_mode=clone:stop_duration=0.7[vo]','[ac]apad=pad_dur=0.7[ao]']
  args+=['-filter_complex',';'.join(filters),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','15','-threads','2','-c:a','aac','-b:a','256k','-movflags','+faststart',str(base)]
  run(args)
 if not audio.exists():
  print('Áudio',pid,flush=True);run(['ffmpeg','-v','error','-y','-i',str(base),'-vn','-af','highpass=f=75,lowpass=f=13500,loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','pcm_s16le',str(audio)])
 if alpha.exists():continue
 print('Recorte RVM',pid,flush=True);dec=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(base),'-an','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgba','-video_size','540x800','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-crf','22','-b:v','0','-deadline','realtime','-cpu-used','5','-row-mt','1','-threads','2','-pix_fmt','yuva420p','-auto-alt-ref','0',str(alpha)],stdin=subprocess.PIPE)
 states=[np.zeros((1,1,1,1),np.float32) for _ in range(4)];n=0;last_seg=-1;tracking=np.array(basefaces[plan['segments'][0]['file']],float)
 while True:
  raw=dec.stdout.read(540*960*3)
  if len(raw)!=540*960*3:break
  rgb=np.frombuffer(raw,np.uint8).reshape(960,540,3);t=n/30;idx=max(i for i,s in enumerate(plan['segments']) if s['from']<=t+.0001)
  if idx!=last_seg:
   states=[np.zeros((1,1,1,1),np.float32) for _ in range(4)];tracking=np.array(basefaces[plan['segments'][idx]['file']],float);last_seg=idx
  src=rgb.astype('float32').transpose(2,0,1)[None]/255
  feed={'src':src,'downsample_ratio':np.array([.5],np.float32),**{f'r{i+1}i':v for i,v in enumerate(states)}}
  fgr,pha,*states=session.run(None,feed);a=pha[0,0];fore=np.clip(fgr[0].transpose(1,2,0)*255,0,255).astype(np.uint8)
  if n%6==0:
   boxes=face.detectMultiScale(cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY),scaleFactor=1.12,minNeighbors=5,minSize=(185,185))
   if len(boxes):
    x,y,w,h=max(boxes,key=lambda b:b[2]*b[3]);target=np.array([x+w/2,y+h/2,w]);tracking=tracking*.78+target*.22
  cx,cy,fw=tracking;scale=225/max(215,fw);tx=270-cx*scale;ty=240-cy*scale
  rows=np.flatnonzero((a>.8).sum(axis=1)>18)
  if len(rows):ty=max(ty,55-rows[0]*scale)
  mat=np.array([[scale,0,tx],[0,scale,ty]],np.float32)
  fg=cv2.warpAffine(fore,mat,(540,800),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
  mask=cv2.warpAffine(a,mat,(540,800),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
  out=np.dstack([fg,np.clip(mask*255,0,255).astype(np.uint8)])
  enc.stdin.write(out.tobytes());n+=1
  if n%150==0:print(pid,'quadros',n,flush=True)
 enc.stdin.close();assert enc.wait()==0;assert dec.wait()==0
 plan['frames']=n;print('Recorte concluído',pid,n,flush=True)
 (WORK/f'{pid}-frames.json').write_text(json.dumps({'frames':n,'duration':n/30}))
(ROOT/'work/prepared.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2))
