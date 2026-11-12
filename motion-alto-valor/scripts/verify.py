from pathlib import Path
import json,subprocess,hashlib,numpy as np,soundfile as sf
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-alto-valor.mp4';timeline=json.loads((r/'timeline.json').read_text());caps=json.loads((r/'public/captions.json').read_text())
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in j['streams'] if t['codec_type']=='video');a=next(t for t in j['streams'] if t['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1080,1920,'h264','aac')
assert v['r_frame_rate']=='30/1' and int(v['nb_frames'])==timeline['frames']
assert abs(float(j['format']['duration'])-timeline['duration'])<.08
for c in caps:
 assert 1<=len(c['words'])<=3 and 0<=c['start']<c['end']<=timeline['duration']
 f=ImageFont.truetype(str(r/'public/fonts/Montserrat-ExtraBold.ttf'),c['fontSize']);width=sum(f.getlength(w['text'].upper())+8 for w in c['words'])+12*(len(c['words'])-1)+48
 assert width<=940,(c,width)
for s in timeline['scenes']:assert s['speechDuration']>0 and s['start']+s['speechDuration']<s['end']
assert timeline['scenes'][-1]['end']-(timeline['scenes'][-1]['start']+timeline['scenes'][-1]['speechDuration'])>=3
expected,sr=sf.read(r/'public/audio/mix.wav');expected=expected.mean(axis=1)
actual=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(sr),'-f','f32le','-']),dtype=np.float32);n=min(len(expected),len(actual));corr=float(np.corrcoef(expected[:n],actual[:n])[0,1]);assert corr>.99,corr
peak=float(np.max(np.abs(actual)));assert peak<1,peak
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'resolution':[1080,1920],'fps':30,'frames':int(v['nb_frames']),'duration':float(j['format']['duration']),'scenes':len(timeline['scenes']),'voice':'Generated Brazilian Portuguese male voice — Kokoro pm_alex','narrationIntact':True,'audioCorrelationWithMix':corr,'peak':peak,'captionGroups':len(caps),'captionWords':sum(len(c['words']) for c in caps),'captionFit':'passed','endCtaVisibleSeconds':timeline['scenes'][-1]['end']-timeline['scenes'][-1]['start'],'holdAfterNarrationSeconds':timeline['scenes'][-1]['end']-(timeline['scenes'][-1]['start']+timeline['scenes'][-1]['speechDuration']),'fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
