from pathlib import Path
import subprocess,json,time,sys
r=Path(__file__).resolve().parents[1];mode=sys.argv[1] if len(sys.argv)>1 else 'preview';plan=json.loads((r/'edit-plan.json').read_text());n=300 if mode=='preview' else plan['frames'];duration=n/30
panel=r/'public/video'/('presenter-preview.mp4' if mode=='preview' else 'presenter.mp4');stage=r/'out'/f'stage-{mode}.mp4'
def ready(p):
 try:return int(json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(p)],stderr=subprocess.DEVNULL))['streams'][0]['nb_frames'])==n
 except Exception:return False
while not ready(panel) or not ready(stage):time.sleep(2)
name='ib-midias-vidracarias-video2-previa-10s.mp4' if mode=='preview' else 'ib-midias-vidracarias-video2.mp4';dest=r/'out'/name
bed=r/'public/bed-original.wav'
filt=f'[0:v]pad=1080:1920:0:884:white,format=rgba[base];[1:v]format=rgba,colorkey=0x000000:0.12:0.03[graphics];[base][graphics]overlay=0:0:format=rgb,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v];[2:a]atrim=duration={duration},asetpts=PTS-STARTPTS[voice];[3:a]volume=0.045,atrim=duration={duration},afade=t=in:d=0.5,afade=t=out:st={duration-.6}:d=0.6[music];[voice][music]amix=inputs=2:duration=first:normalize=0[a]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(panel),'-i',str(stage),'-i',str(r/'public/video/voice.wav'),'-stream_loop','-1','-i',str(bed),'-filter_complex',filt,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-t',str(duration),'-frames:v',str(n),'-movflags','+faststart',str(dest)],check=True)
s=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(dest)]));v=next(x for x in s['streams'] if x['codec_type']=='video');assert (v['width'],v['height'],int(v['nb_frames']),v['r_frame_rate'])==(1080,1920,n,'30/1')
print('COMPOSED',dest,flush=True)
