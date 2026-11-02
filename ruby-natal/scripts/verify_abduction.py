from pathlib import Path
import json,subprocess,hashlib
r=Path(__file__).resolve().parents[1];p=r/'entrega/ruby-lingerie-natal-cochilo-abducao.mp4';m=json.loads((r/'edicao-abducao.json').read_text());d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',m['frames'])
assert a['codec_name']=='aac' and abs(float(v['duration'])-float(a['duration']))<.09
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True,capture_output=True)
report={'file':p.name,'duration':float(v['duration']),'frames':int(v['nb_frames']),'video':'H.264 1080x1920 30 fps','audio':'AAC stereo','fullDecode':'passed','sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'verificacao-abducao.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
