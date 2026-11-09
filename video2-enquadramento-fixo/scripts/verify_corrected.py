from pathlib import Path
import json,subprocess,hashlib,array,math
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-vidracarias-video2-estatico-corrigido.mp4';old=r.parent/'entregas/ib-midias-vidracarias-video2-estatico.mp4'
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in j['streams'] if t['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',2298);assert abs(float(j['format']['duration'])-76.6)<.05

def pcm(p):
 a=array.array('f');a.frombytes(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']));return a
ref=pcm(old);actual=pcm(p);expected=ref[:round(52.7*16000)]+ref[round((1754/30)*16000):];n=min(len(expected),len(actual));dot=sum(expected[i]*actual[i] for i in range(n));xx=sum(x*x for x in expected[:n]);yy=sum(x*x for x in actual[:n]);corr=dot/math.sqrt(xx*yy);assert corr>.99,corr
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'resolution':[1080,1920],'fps':30,'frames':2298,'duration':float(j['format']['duration']),'retainedAudioCorrelation':corr,'removedFrames':[1581,1754],'removedSeconds':[52.7,1754/30],'durationRemoved':173/30,'completeAdsTake':'Instagram, Facebook e Google, once','captionPatch':'Aligned to complete retained take using previously reviewed graphics','framing':'Same fixed crop, no face tracking or animated zoom','fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'corrected-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
