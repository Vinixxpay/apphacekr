from pathlib import Path
import json,numpy as np,soundfile as sf
r=Path(__file__).resolve().parents[1];p=r/'public/timeline.json';j=json.loads(p.read_text());a,sr=sf.read(r/'public/audio/voice.wav');arr=[]
for i in range(j['frames']):
 w=a[round(i/30*sr):round((i+1)/30*sr)];arr.append(round(min(1,float(np.sqrt(np.mean(w*w)))/.13),3) if len(w) else 0)
j['mouth']=arr;p.write_text(json.dumps(j,ensure_ascii=False,indent=2));print('MOUTH TIMING READY',len(arr))
