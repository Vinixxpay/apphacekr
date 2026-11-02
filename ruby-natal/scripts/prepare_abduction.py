"""Create the proportion-preserving foreground used in the TV portal."""
from pathlib import Path
import os,cv2,numpy as np,onnxruntime as ort
r=Path(__file__).resolve().parents[1];(r/'work').mkdir(exist_ok=True)
inputs=Path(os.environ.get('RUBY_INPUT',str(r/'input')))
p=next(p for p in inputs.rglob('*.mp4') if '18.42.01' in p.name)
c=cv2.VideoCapture(str(p));c.set(cv2.CAP_PROP_POS_MSEC,5750);ok,b=c.read();assert ok
rgb=cv2.cvtColor(b,cv2.COLOR_BGR2RGB);options=ort.SessionOptions();options.intra_op_num_threads=2
model=os.environ.get('RUBY_RVM',str(r/'work/rvm.onnx'))
s=ort.InferenceSession(model,options,providers=['CPUExecutionProvider'])
feed={'src':rgb.astype(np.float32).transpose(2,0,1)[None]/255,'downsample_ratio':np.array([.5],np.float32),**{f'r{i}i':np.zeros((1,1,1,1),np.float32) for i in range(1,5)}}
for _ in range(5):
 fg,a,*st=s.run(None,feed);feed.update({f'r{i+1}i':x for i,x in enumerate(st)})
cv2.imwrite(str(r/'work/abduction-person.png'),np.dstack([np.clip(fg[0].transpose(1,2,0)[:,:,::-1]*255,0,255).astype(np.uint8),np.clip(a[0,0]*255,0,255).astype(np.uint8)]))
cv2.imwrite(str(r/'work/abduction-sofa.jpg'),b)
