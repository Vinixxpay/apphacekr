from pathlib import Path
import math,random,wave,struct,subprocess
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).resolve().parents[1];work=r/'work/outro';work.mkdir(parents=True,exist_ok=True)
s=(r/'public/logo.svg').read_text().replace('<svg ','<svg width="800" height="661" ',1)
(work/'logo-sized.svg').write_text(s)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(work/'logo-sized.svg'),'-frames:v','1',str(work/'logo.png')],check=True)
logo=Image.open(work/'logo.png').convert('RGBA');logo.thumbnail((640,530),Image.Resampling.LANCZOS)
layer=Image.new('RGBA',(1080,1920));layer.alpha_composite(logo,((1080-logo.width)//2,570))
d=ImageDraw.Draw(layer);font=ImageFont.truetype(str(r/'public/fonts/Montserrat-ExtraBold.ttf'),104)
d.text((540,1190),'iB Mídias',font=font,fill='#0131CD',anchor='mm')
d.rounded_rectangle((340,1324,740,1332),radius=4,fill='#B9FC01')
for frame in range(132):
 t=frame/60;u=min(1,t/.50);ease=1+2.70158*(u-1)**3+1.70158*(u-1)**2;scale=.90+.10*ease
 sz=(round(1080*scale),round(1920*scale));pic=layer.resize(sz,Image.Resampling.LANCZOS)
 if t<.18:pic.putalpha(pic.getchannel('A').point(lambda v:round(v*min(1,t/.18))))
 canvas=Image.new('RGB',(1080,1920),'white');canvas.paste(pic,((1080-sz[0])//2,(1920-sz[1])//2),pic)
 canvas.save(work/f'{frame:04d}.png')
# Original short sonic signature: soft whoosh followed by a two-tone shimmer.
sr=48000;rng=random.Random(47);data=bytearray();lp=0
for i in range(round(2.2*sr)):
 t=i/sr;n=rng.uniform(-1,1);lp=.87*lp+.13*n
 env=math.sin(math.pi*t/.34)**2 if t<.34 else 0
 whoosh=(n-lp)*.055*env
 u=t-.20
 bell=0 if u<0 else (.085*math.sin(2*math.pi*659.255*u)+.053*math.sin(2*math.pi*987.767*u)+.018*math.sin(2*math.pi*1975.534*u))*math.exp(-u*4.8)*min(1,u/.012)
 sample=max(-1,min(1,whoosh+bell));v=round(sample*32767);data+=struct.pack('<hh',v,v)
with wave.open(str(r/'public/logo-sound.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(data)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','60','-i',str(work/'%04d.png'),'-i',str(r/'public/logo-sound.wav'),'-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','2.2','-movflags','+faststart',str(r/'work/outro.mp4')],check=True)
print('OUTRO READY — 2.2 seconds, supplied logo + original sonic signature',flush=True)
