from pathlib import Path
import subprocess,json,hashlib,time,concurrent.futures
import numpy as np
from scipy.signal import correlate,correlation_lags
from PIL import ImageFont
r=Path(__file__).resolve().parents[1]
plan=json.loads((r/'edit-plan.json').read_text());edit=json.loads((r/'work/edit.json').read_text())
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def check(name,frames):
 p=r/'out'/name;d=probe(p);v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio');assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',frames)
 assert a['codec_name']=='aac' and abs(float(v['duration'])-float(a['duration']))<.15
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],capture_output=True,check=True)
 return {'file':name,'frames':frames,'duration':float(v['duration']),'video':'H.264 1080x1920 30 fps','audio':'AAC','fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(2) as ex:reports=list(ex.map(lambda p:check(*p),[('ib-midias-vidracarias-video2-previa-10s.mp4',300),('ib-midias-vidracarias-video2-revisado.mp4',plan['frames'])]))
# Caption readability, screen bounds and timing against the real recording.
for c in edit['captions']:
 assert 1<=len(c['words'])<=3
 tx=' '.join(w['text'].upper() for w in c['words']);size=46 if len(tx)>25 else 56;font=ImageFont.truetype(str(r/'public/Montserrat.ttf'),size);font.set_variation_by_axes([800]);width=sum(font.getlength(w['text'].upper())+10 for w in c['words'])+12*(len(c['words'])-1)+50;assert width<=1016,(tx,width)
 for w in c['words']:assert 0<=w['start']<=w['end']<=plan['duration']
assert sum(len(c['words']) for c in edit['captions'])==len(plan['words'])
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','8000','-ac','1','-f','f32le','-']),np.float32)
expected=audio(r/'public/video/voice.wav');actual=audio(r/'out/ib-midias-vidracarias-video2-revisado.mp4');checks=[]
assert abs(len(expected)-len(actual))/8000<.08, 'Unexpected decoded audio length difference'
duration=plan['duration']
for start,end in [(0.4,4.4),(duration*.45,duration*.45+4),(duration-5.0,duration-.03)]:
 x=expected[round(start*8000):round(end*8000)];y=actual[round(start*8000):round(end*8000)];c=correlate(y,x,method='fft');lags=correlation_lags(len(y),len(x));i=int(np.argmax(c));lag=int(lags[i]);assert abs(lag)<=320,lag
 if lag>=0:y=y[lag:];x=x[:len(y)]
 else:x=x[-lag:];y=y[:len(x)]
 common=min(len(x),len(y));x=x[:common];y=y[:common];assert common>24000
 value=float(np.corrcoef(x,y)[0,1]);assert value>.90,(start,value)
 checks.append({'interval':[start,end],'voiceCorrelation':round(value,6),'offsetSeconds':lag/8000})
report={'deliveries':reports,'captions':{'groups':len(edit['captions']),'words':len(plan['words']),'maxWordsPerGroup':3,'fit':'passed','timing':'passed'},'voicePreservation':checks,'speed':1.0,'sourceEditPlan':'edit-plan.json'}
(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
