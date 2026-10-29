from pathlib import Path
import subprocess,json,time,math
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];work=r/'work';out=r/'out/review';data=json.loads((work/'review-data.json').read_text());font=ImageFont.truetype(str(r/'public/Inter-ExtraBold.ttf'),49)
def ready(path,frames):
 try:
  q=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(path)],stderr=subprocess.DEVNULL));return int(q['streams'][0]['nb_frames'])==frames
 except Exception:return False
def wait(path,n):
 while not ready(path,n):time.sleep(2)
def tm(t):
 c=round(max(0,t)*100);return f'{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}'
def make_ass(f):
 header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nScaledBorderAndShadow: yes\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Text,Inter,49,&H00FFF8F4,&H00FFF8F4,&H00000000,&H00000000,-1,0,0,0,100,100,-1.5,0,1,0,0,5,0,0,0,1\nStyle: Box,Inter,1,&H20180902,&H20180902,&H20180902,&H20180902,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
 rows=[]
 for c in f['captions']:
  words=c['words'];plain=' '.join(w['text'] for w in words);lines=[plain]
  if font.getlength(plain)>805:
   parts=plain.split();mid=max(1,len(parts)//2);lines=[' '.join(parts[:mid]),' '.join(parts[mid:])]
  width=min(862,round(max(font.getlength(z) for z in lines))+54);h=66*len(lines)+14;x=540-width/2;y=1502;w=width
  path=f'm 18 0 l {w-18} 0 b {w-6} 0 {w} 6 {w} 18 l {w} {h-18} b {w} {h-6} {w-6} {h} {w-18} {h} l 18 {h} b 6 {h} 0 {h-6} 0 {h-18} l 0 18 b 0 6 6 0 18 0'
  rows.append(f'Dialogue: 0,{tm(c["start"])},{tm(c["end"])},Box,,0,0,0,,{{\\pos({x:.1f},{y})\\p1}}{path}{{\\p0}}')
  points=sorted(set([c['start'],c['end']]+[max(c['start'],min(c['end'],z)) for word in words for z in [word['start'],word['end']]]))
  for a,b in zip(points,points[1:]):
   if b-a<.005:continue
   current=(a+b)/2;txt='';linechar=len(lines[0]);done=0
   for i,word in enumerate(words):
    token=word['text'].replace('{','').replace('}','');color='FF9F24' if word['start']<=current<=word['end'] else 'FFF8F4'
    txt+=('{\\c&H'+color+'&}'+token)
    done+=len(word['text'])
    if len(lines)>1 and done==linechar:txt+='\\N'
    elif i<len(words)-1:txt+=' ';done+=1
   rows.append(f'Dialogue: 1,{tm(a)},{tm(b)},Text,,0,0,0,,{{\\pos(540,{y+h/2:.1f})}}{txt}')
 p=work/f"{f['id']}.ass";p.write_text(header+'\n'.join(rows)+'\n');return p
# Wait for the source matting pass to close all four alpha streams.
while not (work/'r2-2196-frames.json').exists():time.sleep(2)
client=data['client'];master=out/'ReviewClient-master.mp4';wait(master,client['frames']);target=out/'r2-client.mp4'
if not target.exists():
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-vf','scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',str(target)],check=True)
 print('Áudio da cliente completo:',client['audioDuration'],'s',flush=True)
for f in data['films']:
 pid=f['id'];master=out/f"Review{pid[-4:]}-master.mp4";wait(master,f['frames']);target=out/f'{pid}.mp4'
 if target.exists():continue
 ass=make_ass(f);dur=f['frames']/30;voice=r/'public/video'/f'{pid}-voice.wav';alpha=r/'public/video'/f'{pid}-person.webm'
 filt=f"color=c=0x050D1C:s=1080x1920:r=30:d={dur}[bg];[0:v]scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p[g];[bg][g]overlay=0:0:shortest=1[stage];[1:v]scale=900:1334:flags=lanczos:in_color_matrix=bt601:out_color_matrix=bt709:in_range=tv:out_range=tv,format=yuva420p[p];[stage][p]overlay=90:880:format=yuv420:shortest=0:eof_action=repeat[people];[people]ass=filename='{ass}':fontsdir='{r/'public'}'[v];[2:a]apad,atrim=duration={dur},asetpts=PTS-STARTPTS[voice];[3:a]volume=0.10,afade=t=in:d=0.5,afade=t=out:st={max(0,dur-.6)}:d=0.6,atrim=duration={dur}[music];[voice][music]amix=inputs=2:normalize=0:duration=first[a]"
 args=['ffmpeg','-v','error','-y','-filter_complex_threads','1','-i',str(master),'-c:v','libvpx-vp9','-i',str(alpha),'-i',str(voice),'-stream_loop','-1','-i',str(r/'public/bed-original.wav'),'-filter_complex',filt,'-map','[v]','-map','[a]','-t',str(dur),'-c:v','libx264','-preset','fast','-crf','19','-threads','2','-pix_fmt','yuv420p','-r','30','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart',str(target)]
 subprocess.run(args,check=True);print(pid,'gravação completa composta',dur,flush=True)
print('Todas as gravações integrais prontas.',flush=True)
