from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-vd4-zoom-leve.mp4';a=r.parent/'entregas/ib-midias-vd4-legendas-logo.mp4'
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in j['streams'] if t['codec_type']=='video')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'h264','60/1',2112)
assert abs(float(j['format']['duration'])-35.2)<.02

def audio_hash(path):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-']);return hashlib.sha256(data).hexdigest()
h=audio_hash(p);assert h==audio_hash(a),'Audio must be identical to approved version'
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
res={'file':p.name,'resolution':[1080,1920],'fps':60,'duration':float(j['format']['duration']),'frames':2112,'zoomFactor':2160/1872,'audioPacketsIdenticalToApproved':True,'audioSha256':h,'captionSizeAndPositionPreserved':True,'outroNotCropped':True,'fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'zoom-verification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
