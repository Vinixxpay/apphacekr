import subprocess,json,pathlib
import numpy as np
root=pathlib.Path(__file__).resolve().parent.parent
out=[]
for v in json.loads((root/'timings.json').read_text()):
 p=root/'out'/f'video_0{v["id"]}_lavai.mp4'
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 vid=next(s for s in probe['streams'] if s['codec_type']=='video'); aud=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (vid['width'],vid['height'],vid['codec_name'],vid['r_frame_rate'])==(1080,1920,'h264','30/1')
 assert aud['codec_name']=='aac' and int(vid['nb_frames'])==v['frames']
 assert 25<=float(probe['format']['duration'])<=35
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
 def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','1','-ar','24000','-']),dtype=np.float32)
 actual=samples(p);expected=samples(root/'public'/'audio'/f'v{v["id"]}'/'mix.wav');n=min(len(actual),len(expected));cor=float(np.corrcoef(actual[:n],expected[:n])[0,1]);assert cor>.98,cor
 captions=json.loads((root/'public'/f'captions-{v["id"]}.json').read_text());assert all(len(c['words'])<=3 for c in captions)
 out.append({'file':p.name,'duration':float(probe['format']['duration']),'frames':int(vid['nb_frames']),'size':p.stat().st_size,'video':'H.264 1080x1920 30fps','audio':'AAC','audio_correlation':cor,'full_decode':'passed'})
 print(out[-1],flush=True)
(root/'verification.json').write_text(json.dumps(out,indent=2))
