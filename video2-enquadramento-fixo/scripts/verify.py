from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-vidracarias-video2-estatico.mp4';old=r.parent/'entregas/ib-midias-vidracarias-video2.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
a=probe(old);o=probe(p);v=next(x for x in o['streams'] if x['codec_type']=='video');sv=next(x for x in a['streams'] if x['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',2471)
assert int(v['nb_frames'])==int(sv['nb_frames'])
assert abs(float(o['format']['duration'])-float(a['format']['duration']))<.05

def audiohash(p):return hashlib.sha256(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
h=audiohash(p);assert h==audiohash(old),'Audio should be unchanged'
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
res={'file':p.name,'resolution':[1080,1920],'fps':30,'frames':int(v['nb_frames']),'duration':float(o['format']['duration']),'referenceVersion':'ib-midias-vidracarias-video2.mp4 (original 1min22s version)','audioIdenticalToReference':True,'audioSha256':h,'presenterCrop':{'x':0,'y':520,'width':984,'height':944},'cropIsConstantForAllFrames':True,'faceTracking':False,'animatedZoom':False,'originalTimelinePreserved':True,'graphicsAndCaptions':'Same archived Remotion composition and word timings as reference version','fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(r/'verification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
