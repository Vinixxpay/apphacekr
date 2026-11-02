from pathlib import Path
import os,cv2,numpy as np,math,subprocess,json,wave
from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
R=Path(__file__).resolve().parents[1]; W,H=720,1280;FPS=30
cv2.setNumThreads(2)
INPUT=Path(os.environ.get('RUBY_INPUT',str(R/'input')))
paths={k:next(p for p in INPUT.rglob('*.mp4') if k in p.name) for k in ['18.10.41','18.08.17','18.33.48','18.42.01']}
class Clip:
 def __init__(self,p):
  self.c=cv2.VideoCapture(str(p));self.fps=self.c.get(cv2.CAP_PROP_FPS);self.n=int(self.c.get(cv2.CAP_PROP_FRAME_COUNT));self.last=-2;self.im=None
 def get(self,t):
  n=min(self.n-1,max(0,int(t*self.fps)))
  if n==self.last:return self.im.copy()
  if n!=self.last+1:self.c.set(cv2.CAP_PROP_POS_FRAMES,n)
  ok,f=self.c.read()
  if ok:self.im=f;self.last=n
  return self.im.copy()
clips={k:Clip(p) for k,p in paths.items()}
def ease(t):
 t=np.clip(t,0,1);return float(t*t*(3-2*t))
def fit(f):
 h,w=f.shape[:2];s=max(W/w,H/h);nw,nh=round(w*s),round(h*s);o=cv2.resize(f,(nw,nh),interpolation=cv2.INTER_CUBIC);return o[(nh-H)//2:(nh-H)//2+H,(nw-W)//2:(nw-W)//2+W]
yy,xx=np.mgrid[:H,:W];rad=((xx-W/2)/(W*.69))**2+((yy-H/2)/(H*.9))**2;vig=np.clip(1-.25*rad,.65,1).astype(np.float32)[...,None]
def contain(f):
 bg=cv2.GaussianBlur(fit(f),(0,0),24);h,w=f.shape[:2];sc=W/w;nh=round(h*sc);fg=cv2.resize(f,(W,nh));y=(H-nh)//2;bg[y:y+nh]=fg;return bg

def grade(f,warm=1,glow=.1):
 f=f.astype(np.float32)/255
 f=np.clip((f-.04)*1.065+.04,0,1);f[:,:,0]*=1-.075*warm;f[:,:,1]*=1+.012*warm;f[:,:,2]*=1+.045*warm
 if glow:
  bright=np.maximum(f-.65,0);f+=cv2.GaussianBlur(bright,(0,0),10)*glow
 v=vig if f.shape[1]==W else cv2.resize(vig[:,:,0],(f.shape[1],f.shape[0]))[...,None]
 return np.clip(f*v*255,0,255).astype(np.uint8)
rng=np.random.default_rng(1212);points=rng.random((78,5))
def sparkles(f,t,amount=.28,portal=False):
 layer=np.zeros_like(f)
 for x,y,z,v,phase in points:
  px=int((x*W+math.sin(t*.35+phase*6)*18)%W);py=int((y*H+t*(9+z*17))%H);r=1+int(z*3);a=(.35+.65*math.sin(t*(1+v)+phase*6)**2)
  col=tuple(int(c*a) for c in (140,210,255));cv2.circle(layer,(px,py),r,col,-1,cv2.LINE_AA)
  if z>.94:
   cv2.line(layer,(px-5,py),(px+5,py),col,1,cv2.LINE_AA);cv2.line(layer,(px,py-5),(px,py+5),col,1,cv2.LINE_AA)
 return cv2.addWeighted(f,1,cv2.GaussianBlur(layer,(0,0),.7),amount,0)
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf';sans='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def textlayer(lines):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 for text,y,size,color in lines:
  font=ImageFont.truetype(serif if size>=35 else sans,size);box=d.textbbox((0,0),text,font=font);x=(W-(box[2]-box[0]))/2;d.text((x,y),text,font=font,fill=color,stroke_width=0)
 return np.array(im)
def layer(f,im,a=1):
 alpha=im[:,:,3:4].astype(np.float32)/255*a;return np.clip(f*(1-alpha)+im[:,:,:3][:,:,::-1]*alpha,0,255).astype(np.uint8)
opening=textlayer([('Uma noite para sonhar.',1050,34,(255,242,223,255))])
endtext=textlayer([('RUBY',350,88,(249,227,191,255)),('L I N G E R I E',465,24,(243,219,190,255)),('Amigo Calcinha',605,40,(255,245,230,255)),('Um Natal de carinho.',670,32,(255,245,230,255))])
dreamtext=textlayer([('O conforto também faz sonhar.',1080,30,(255,243,224,255))])
# Chronological actions within each take; the chocolate moment precedes the remote.
segments=[('entrada',0,5.3),('chocolate',4.7,6.7),('controle',10.8,6.2),('sonho',16.5,5.9),('portal',22.4,4.2),('filme',25.9,5.4),('marca',30.5,4.5)]
DURATION=35.0;N=round(DURATION*FPS)
person=cv2.imread(str(R/'work/abduction-person.png'),cv2.IMREAD_UNCHANGED);person=fit(person)
sofa=grade(fit(cv2.imread(str(R/'work/abduction-sofa.jpg'))));tvstill=grade(contain(clips['18.08.17'].get(.4)),.3,.25)
base=np.zeros((H,W,3),np.float32);base[:]=[21,15,42];base+=np.exp(-(((xx-W*.5)/550)**2+((yy-H*.3)/400)**2))[...,None]*np.array([10,13,22]);base=np.clip(base,0,255).astype(np.uint8)
def portal(t):
 p=ease((t-.8)/2.9);reveal=ease((t-.1)/.7)
 bg=cv2.addWeighted(sofa,1-reveal,tvstill,reveal,0)
 # A soft beam comes from the TV, behind the actual sleeping foreground.
 beam=np.zeros_like(bg);strength=math.sin(min(1,t/3.8)*math.pi)
 poly=np.array([[int(W*.39),int(H*.48)],[int(W*.61),int(H*.48)],[int(W*.91),int(H*.94)],[int(W*.09),int(H*.94)]],np.int32)
 cv2.fillConvexPoly(beam,poly,(156,199,232));beam=cv2.GaussianBlur(beam,(0,0),25)
 bg=cv2.addWeighted(bg,1,beam,float(strength*.18),0)
 scale=1-.978*p;anchorx=W*.5;anchory=H*.64
 cx=anchorx;cy=anchory+(H*.50-anchory)*p-H*.13*math.sin(math.pi*p)
 m=np.array([[scale,0,cx-anchorx*scale],[0,scale,cy-anchory*scale]],np.float32)
 fg=cv2.warpAffine(person,m,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
 a=fg[:,:,3:4].astype(np.float32)/255*(1-ease((t-3.25)/.45));bg=np.clip(bg*(1-a)+fg[:,:,:3]*a,0,255).astype(np.uint8)
 magic=np.zeros_like(bg)
 for x,y,z,v,ph in points:
  theta=x*math.tau+t*(.35+v);radius=(1-p)*(.22+z*.8)+.015
  sx=int(W/2+math.cos(theta)*W*.48*radius);sy=int(H*.51+math.sin(theta)*H*.28*radius)
  cv2.circle(magic,(sx,sy),int(1+z*3),(190,231,255),-1,cv2.LINE_AA)
 bloom=cv2.GaussianBlur(magic,(0,0),12);bg=cv2.addWeighted(bg,1,cv2.addWeighted(magic,.6,bloom,1.8,0),float(strength*.6),0)
 flash=.65*math.exp(-((t-3.7)/.17)**2);return cv2.addWeighted(bg,1-flash,np.full_like(bg,(238,248,255)),flash,0)

def scene(name,t):
 if name=='entrada':
  f=grade(fit(clips['18.10.41'].get(5.7+t)),1,.23)
  if .8<t<4.9:f=layer(f,opening,ease((t-.8)/.6)*(1-ease((t-4.1)/.8)))
  return sparkles(f,t,.10)
 if name=='chocolate':return sparkles(grade(fit(clips['18.10.41'].get(17.2+t)),1,.22),t,.13)
 if name=='controle':return grade(fit(clips['18.10.41'].get(11+t)),.85,.18)
 if name=='portal':return portal(t)
 if name=='filme':
  f=grade(contain(clips['18.33.48'].get(t)),.2,.26)
  return sparkles(f,t,.32)
 if name=='sonho':
  src=clips['18.42.01'].get(min(5.75,2.8+t*.6));bg=grade(cv2.GaussianBlur(cv2.resize(src,(W,H)),(0,0),35),.9,.2)
  # Portrait is preserved, framed with a soft cinematic surround, never stretched.
  sh,sw=src.shape[:2];fw=int(sw*H/sh);fg=grade(cv2.resize(src,(fw,H)),.8,.34);x=(W-fw)//2
  bg[:,x:x+fw]=fg;bg=sparkles(bg,t,.22)
  if t>1.4:bg=layer(bg,dreamtext,ease((t-1.4)/1.2)*(1-ease((t-4.8)/1.1)))
  return bg
 if name=='marca':
  f=sparkles(base.copy(),t,.65)
  # Fine gold divider and holiday glow stay behind the brand.
  cv2.line(f,(250,555),(470,555),(121,166,207),1,cv2.LINE_AA)
  return layer(f,endtext,ease(t/1.1))

def frame(t):
 active=[s for s in segments if s[1]<=t<s[1]+s[2]]
 if not active:active=[segments[-1]]
 s=active[-1];f=scene(s[0],t-s[1])
 if len(active)>1:
  old=active[-2];overlap=old[1]+old[2]-s[1];a=ease((t-s[1])/overlap);f=cv2.addWeighted(scene(old[0],t-old[1]),1-a,f,a,0)
 # Quiet film grain and modest letterbox; facial detail remains intact.
 noise=rng.normal(0,.48,(H,W,1)).astype(np.float32);f=np.clip(f.astype(np.float32)+noise,0,255).astype(np.uint8)
 f[:27]=[8,7,10];f[-27:]=[8,7,10]
 fade=ease(t/.7)*(1-ease((t-(N/FPS-.85))/.85));return (f*fade).astype(np.uint8)

def music():
 sr=48000;dur=N/FPS;t=np.arange(round(sr*dur))/sr;left=np.zeros_like(t);right=np.zeros_like(t)
 chords=[(146.832,184.997,220),(123.471,146.832,184.997),(97.999,123.471,146.832),(110,138.591,164.814)]
 beat=60/78
 def note(start,freq,length,amp,pan=.5,bell=False):
  i=int(start*sr);n=min(int(length*sr),len(t)-i)
  if n<=0:return
  x=np.arange(n)/sr
  if bell:env=(1-np.exp(-x*90))*np.exp(-x*2.3);s=sum(np.sin(2*np.pi*freq*m*x)*v for m,v in [(1,1),(2.003,.38),(3.99,.10)])*env
  else:env=np.minimum(x/.7,1)*np.minimum((length-x)/1.2,1);s=(np.sin(2*np.pi*freq*x)+.22*np.sin(2*np.pi*freq*2*x)+.10*np.sin(2*np.pi*freq*3*x))*np.maximum(env,0)
  left[i:i+n]+=s*amp*math.sqrt(1-pan);right[i:i+n]+=s*amp*math.sqrt(pan)
 for bar in range(int(dur/(beat*4))+1):
  chord=chords[bar%4];start=bar*beat*4
  for j,f in enumerate(chord):note(start,f,beat*4+1.1,.042,.25+j*.25)
  for k in range(8):note(start+k*beat/2,chord[[0,1,2,1,0,2,1,2][k]]*4,2.4,.035,.28+(k%3)*.22,True)
 # Original glass chimes and airy portal sweep, synchronized with the teleport.
 for start,freq in [(22.7,880),(23.4,1174.66),(24.1,1479.98),(26.1,1760),(30.7,880)]:note(start,freq,3,.07,.5,True)
 a,b=int(22.4*sr),int(26.6*sr);x=np.linspace(0,1,b-a);n=rng.normal(0,1,b-a);n=cv2.GaussianBlur(n.reshape(-1,1).astype(np.float32),(1,0),1).ravel();s=n*np.sin(np.pi*x)**2*.026
 left[a:b]+=s;right[a:b]+=s
 fade=np.minimum(t/1.2,1)*np.minimum((dur-t)/1.5,1);audio=np.stack([left,right],axis=1)*fade[:,None]
 peak=np.max(np.abs(audio));audio*=.55/max(peak,.55)
 with wave.open(str(R/'work/trilha-original.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype('<i2').tobytes())
if __name__=='__main__':
 import sys
 if '--stills' in sys.argv:
  for t in [17.5,21.8,22.4,23.4,24.4,25.7,27,32]:cv2.imwrite(str(R/f'work/previa-{t}.jpg'),frame(t))
 else:
  music();finaldest=R/'entrega/ruby-lingerie-natal-cochilo-abducao.mp4';dest=R/'work/abduction-tail.mp4'
  cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-ss','16.5','-i',str(R/'work/trilha-original.wav'),'-map','0:v','-map','1:a','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(dest)]
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  for n in range(495,N):
   proc.stdin.write(frame(n/FPS).tobytes())
   if n%150==0:print(n,'/',N,flush=True)
  proc.stdin.close();assert proc.wait()==0
  original=R/'entrega/ruby-lingerie-natal-previa-vertical.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(original),'-i',str(dest),'-i',str(R/'work/trilha-original.wav'),'-filter_complex','[0:v]trim=end_frame=495,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-map','2:a','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-t',str(N/FPS),'-movflags','+faststart',str(finaldest)],check=True)
  dest=finaldest
  (R/'edicao-abducao.json').write_text(json.dumps({'brand':'Ruby Lingerie','fps':FPS,'width':1080,'height':1920,'workingWidth':W,'workingHeight':H,'frames':N,'duration':N/FPS,'segments':segments,'originalMusic':True,'status':'Prévia: cenas 1–3; aguardando o take e áudio da divulgação Amigo Calcinha','note':'Recorte com escala uniforme no portal; sem deformação de rosto ou corpo. Tomadas horizontais preservadas e sonho vertical enquadrado com fundo desfocado.'},indent=2,ensure_ascii=False));print(dest,flush=True)
