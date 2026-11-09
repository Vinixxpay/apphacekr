from pathlib import Path
import subprocess,json,time
r=Path(__file__).resolve().parents[1];repo=r.parent;plan=json.loads((r/'edit-plan.json').read_text());n=plan['frames'];panel=r/'work/presenter-static.mp4';stage=r/'out/stage-full.mp4';approved=repo/'entregas/ib-midias-vidracarias-video2.mp4'
def ready(p):
 try:
  v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(p)],stderr=subprocess.DEVNULL))['streams'][0]
  return int(v['nb_frames'])==n and v['r_frame_rate']=='30/1'
 except Exception:return False
while not ready(panel) or not ready(stage):time.sleep(2)
f='[0:v]pad=1080:1920:0:884:white,format=rgba[base];[1:v]format=rgba,colorkey=0x000000:0.12:0.03[graphics];[base][graphics]overlay=0:0:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
dest=r/'out/ib-midias-vidracarias-video2-estatico.mp4'
subprocess.run(['ffmpeg','-v','warning','-y','-threads','2','-i',str(panel),'-threads','2','-i',str(stage),'-i',str(approved),'-filter_complex_threads','2','-filter_complex',f,'-map','[v]','-map','2:a:0','-c:v','libx264','-preset','fast','-crf','19','-maxrate','7M','-bufsize','14M','-threads','4','-pix_fmt','yuv420p','-r','30','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-frames:v',str(n),'-movflags','+faststart','-progress',str(r/'work/compose-progress.txt'),'-nostats',str(dest)],check=True);print('STATIC FINAL READY',flush=True)
