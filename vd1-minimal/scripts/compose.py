from pathlib import Path
import subprocess,json,time
r=Path(__file__).resolve().parents[1];plan=json.loads((r/'edit-plan.json').read_text());pub=r/'public';n=plan['frames'];duration=n/30
p=pub/'video/picture.mp4'
def ready():
 try:return int(json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(p)],stderr=subprocess.DEVNULL))['streams'][0]['nb_frames'])==n
 except Exception:return False
while not ready() or not (pub/'brand.png').exists():time.sleep(2)
f=f'[0:v]eq=contrast=1.025:saturation=1.035:brightness=0.008,format=rgba[p];[p][1:v]overlay=54:144:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v];[2:a]atrim=duration={duration},apad,atrim=duration={duration},asetpts=PTS-STARTPTS[voice];[3:a]volume=.025,atrim=duration={duration},afade=t=in:d=0.7,afade=t=out:st={duration-.7}:d=0.7[music];[voice][music]amix=inputs=2:normalize=0:duration=first[a]'
dest=r/'out/ib-midias-vd1-editado.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-loop','1','-i',str(pub/'brand.png'),'-i',str(pub/'video/voice.wav'),'-stream_loop','-1','-i',str(pub/'bed-original.wav'),'-filter_complex',f,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','20','-maxrate','8M','-bufsize','16M','-threads','3','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-frames:v',str(n),'-t',str(duration),'-movflags','+faststart',str(dest)],check=True)
print('MINIMAL VD1 READY',dest,flush=True)
