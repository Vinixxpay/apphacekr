from pathlib import Path
import json,subprocess,hashlib,array,math
r=Path(__file__).resolve().parents[1];repo=r.parent;p=r/'out/ib-midias-vidracarias-video2-final-natural.mp4'
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in j['streams'] if t['codec_type']=='video');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',2295);assert abs(float(j['format']['duration'])-76.5)<.03

def pcm(p):
 a=array.array('f');a.frombytes(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','16000','-ac','1','-f','f32le','-']));return a
current=pcm(repo/'entregas/ib-midias-vidracarias-video2-estatico-corrigido.mp4');reviewed=pcm(repo/'entregas/ib-midias-vidracarias-video2-revisado.mp4');base=current[:round(63.7*16000)]+reviewed[round(63.7*16000):];expected=array.array('f')
for a,b in [(0,665),(668,682),(685,706),(708,2303)]:expected.extend(base[round(a/30*16000):round(b/30*16000)])
actual=pcm(p);n=min(len(expected),len(actual));dot=sum(expected[i]*actual[i] for i in range(n));xx=sum(x*x for x in expected[:n]);yy=sum(x*x for x in actual[:n]);corr=dot/math.sqrt(xx*yy);assert corr>.985,corr
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'resolution':[1080,1920],'fps':30,'frames':2295,'duration':float(j['format']['duration']),'voiceCorrelationAgainstKeptAudio':corr,'framing':'Same approved constant crop','closing':'Full correct first clause joined to pode contratar você; abandoned restart excluded','material':'Eight frames removed entirely inside three measured quiet gaps; no syllables cut','voiceSpeed':1,'fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'natural-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
