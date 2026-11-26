from pathlib import Path
import numpy as np,soundfile as sf
from PIL import Image,ImageDraw,ImageFilter
r=Path(__file__).resolve().parents[1];p=r/'public';p.mkdir(exist_ok=True)
w,h=1080,1920;y,x=np.mgrid[:h,:w];a=np.zeros((h,w),dtype=float)
for cx,cy in [(60,900),(1020,900),(40,1200),(1040,1200)]:a+=np.exp(-((x-cx)/95)**2-((y-cy)/220)**2)*.2
# Only the peripheral background is touched, keeping the presenter's face clear.
a*=np.clip((np.abs(x-540)-350)/100,0,1)
img=np.zeros((h,w,4),dtype=np.uint8);img[:,:,:3]=[244,151,197];img[:,:,3]=(np.clip(a,0,.3)*255).astype('uint8');im=Image.fromarray(img);draw=ImageDraw.Draw(im)
for xx,yy,size in [(90,730,10),(980,800,9),(135,1090,8),(940,1190,10),(60,1340,7),(1010,1390,8)]:
 draw.line((xx-size,yy,xx+size,yy),fill=(255,214,237,130),width=2);draw.line((xx,yy-size,xx,yy+size),fill=(255,214,237,130),width=2)
im=im.filter(ImageFilter.GaussianBlur(.8));im.save(p/'lateral-glow.png')
sr=48000;n=int(30.005*sr);audio=np.zeros(n);rng=np.random.default_rng(53)
def add(at,v):
 i=int(at*sr);m=min(len(v),n-i)
 if m>0:audio[i:i+m]+=v[:m]
for start in [10.6266666667,20.6333333333]:
 # Falling glissando followed by a metallic coin impact and two quiet bounces.
 t=np.arange(int(.34*sr))/sr;add(start,(np.sin(2*np.pi*(1800*t-1400*t*t))*np.sin(np.pi*t/.34)**2)*.025)
 for off,gain in [(.37,1),(.64,.45),(.83,.22)]:
  t=np.arange(int(.5*sr))/sr;v=np.zeros_like(t)
  for freq,amp,dec in [(1890,1,13),(2870,.55,19),(4180,.25,27),(6200,.13,40)]:v+=amp*np.sin(2*np.pi*freq*t)*np.exp(-t*dec)
  v+=rng.normal(0,.05,len(t))*np.exp(-t*160);add(start+off,v*.055*gain)
sf.write(p/'coin-fx.wav',np.stack([audio,audio],axis=1),sr,subtype='PCM_16')
