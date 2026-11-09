from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from scipy.signal import correlate,correlation_lags
from PIL import Image
r=Path(__file__).resolve().parents[1];plan=json.loads((r/'edit-plan.json').read_text());p=r/'out/ib-midias-vd1-editado.mp4';d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',plan['frames'])
assert a['codec_name']=='aac' and abs(float(v['duration'])-float(a['duration']))<.15
assert not any(s['codec_type']=='subtitle' for s in d['streams'])
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True,capture_output=True)
image=np.asarray(Image.open(r/'public/brand.png').convert('RGBA'));colors={}
for label,rgb in [('blue',(1,49,205)),('white',(255,255,255)),('lime',(185,252,1))]:
 count=int(((image[:,:,:3]==rgb).all(axis=2)&(image[:,:,3]>200)).sum());assert count>50,(label,count);colors[label]={'rgb':rgb,'pixels':count}
def audio(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ar','8000','-ac','1','-f','f32le','-']),np.float32)
xall=audio(r/'public/video/voice.wav');yall=audio(p);assert abs(len(xall)-len(yall))/8000<.08;checks=[]
for start,end in [(.4,4.4),(25.4,29.4),(plan['duration']-5,plan['duration']-.04)]:
 x=xall[round(start*8000):round(end*8000)];y=yall[round(start*8000):round(end*8000)];c=correlate(y,x,method='fft');lags=correlation_lags(len(y),len(x));lag=int(lags[int(np.argmax(c))]);assert abs(lag)<320
 if lag>=0:y=y[lag:]
 else:x=x[-lag:]
 n=min(len(x),len(y));value=float(np.corrcoef(x[:n],y[:n])[0,1]);assert value>.90,(start,value);checks.append({'interval':[start,end],'correlation':round(value,6),'offsetSeconds':lag/8000})
report={'file':p.name,'video':'H.264 1080x1920 30 fps','audio':'AAC','duration':float(d['format']['duration']),'frames':plan['frames'],'style':plan['style'],'brandColors':colors,'voicePreservation':checks,'speed':1.0,'fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
