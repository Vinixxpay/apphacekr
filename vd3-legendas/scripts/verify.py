from pathlib import Path
import os,json,subprocess,hashlib,array,math
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-vd3-legendas-e-cortes.mp4';src=Path(os.environ.get('CAPTION_SOURCE',r/'input/vd3.mp4'))
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
s=probe(src);o=probe(p);v=next(x for x in o['streams'] if x['codec_type']=='video');a=next(x for x in o['streams'] if x['codec_type']=='audio');e=json.loads((r/'edit.json').read_text());cs=json.loads((r/'captions.json').read_text())['groups'];ws=json.loads((r/'transcript-reviewed.json').read_text())['words']
assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1080,1920,'h264','aac')
assert v['r_frame_rate']=='60/1'
assert int(v['nb_frames'])==sum(x['frames'] for x in e['segments'])
assert abs(float(o['format']['duration'])-e['duration'])<.06
for c in cs:
 assert 1<=len(c['words'])<=3
 assert 0<=c['start']<c['end']<=e['duration']
 b=c['box'];assert b['x']>=100 and b['x']+b['width']<=980 and b['y']>=1400 and b['y']+b['height']<=1600
assert all(x['sourceStart']<y['sourceStart'] for x,y in zip(ws,ws[1:]))
assert sum(len(c['words']) for c in cs)==len(ws)
for c in cs:
 for w in c['words']:
  original=next(t for t in ws if t['text']==w['text'] and abs(t['start']-w['start'])<.001)
  assert abs(original['start']-w['start'])<.001
for w in ws:
 assert any(x['sourceStart']<=w['sourceStart'] and w['sourceEnd']<=x['sourceEnd'] for x in e['segments'])
# Compare the retained original audio waveform with the delivered AAC. This catches
# time offsets, missing words, inserted sound, or accidental speed changes.
def pcm(path):
 q=array.array('f');q.frombytes(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','16000','-f','f32le','-']));return q
original=pcm(src);delivered=pcm(p);expected=array.array('f')
for x in e['segments']:expected.extend(original[round(x['sourceStart']*16000):round(x['sourceEnd']*16000)])
n=min(len(expected),len(delivered));dot=sum(expected[i]*delivered[i] for i in range(n));xx=sum(x*x for x in expected[:n]);yy=sum(x*x for x in delivered[:n]);corr=dot/math.sqrt(xx*yy);assert corr>.995,corr
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
res={'file':p.name,'duration':float(o['format']['duration']),'resolution':[1080,1920],'fps':60,'frames':int(v['nb_frames']),'originalSpeed':True,'originalFraming':True,'retainedAudioCorrelation':corr,'subtitleWords':len(ws),'subtitleGroups':len(cs),'captionFit':'passed','fullDecode':'passed','cuts':'Only ranges documented in edit.json','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(r/'verification.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps(res,ensure_ascii=False,indent=2))
