from pathlib import Path
import os,cv2,numpy as np
r=Path(__file__).resolve().parents[1];w=r/'work';w.mkdir(exist_ok=True)
inputs=Path(os.environ.get('RUBY_INPUT',str(r/'input')))
def frame(key,t):
 p=next(p for p in inputs.rglob('*.mp4') if key in p.name);c=cv2.VideoCapture(str(p));c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();assert ok;return f
raw=frame('18.42.01',5.75);original=cv2.imread(str(w/'abduction-person.png'),-1);a=original[:,:,3].copy()
# Keep the actual hair and the blanket covering the lower body; no synthetic body.
gray=cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY);hair=np.zeros_like(a);hair[345:390,48:155]=(gray[345:390,48:155]<88).astype('uint8')*255;a=np.maximum(a,hair)
poly=np.array([[126,420],[237,422],[260,485],[241,552],[237,655],[70,655],[30,588],[25,539],[43,482],[70,446]],np.int32)
lower=np.zeros_like(a);cv2.fillPoly(lower,[poly],255)
b,g,red=cv2.split(raw.astype(np.int16));pink=((red-g)>5)&((red-b)>-2)
lower=(lower.astype(np.float32)*pink).astype(np.uint8)
lower=cv2.morphologyEx(lower,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
a=np.maximum(a,lower);a=cv2.GaussianBlur(a,(7,7),1.6)
fade=np.clip((raw.shape[0]-1-np.arange(raw.shape[0]))/75,0,1).astype(np.float32)
a=(a.astype(np.float32)*fade[:,None]).astype(np.uint8)
cv2.imwrite(str(w/'same-scene-person.png'),np.dstack([raw,a]));cv2.imwrite(str(w/'same-scene-empty-sofa.jpg'),frame('18.10.41',0))
