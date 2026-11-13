from pathlib import Path
import json,subprocess,numpy as np,os,re,unicodedata,difflib
from faster_whisper import WhisperModel
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];os.environ['HF_HOME']='/workspace/.cache/huggingface';m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)
timeline=json.loads((r/'timeline.json').read_text());groups=[];review=[]
def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFD',t.lower()).encode('ascii','ignore').decode())
for i,s in enumerate(timeline['scenes']):
 audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/f'public/audio/scene-{i}.wav'),'-f','f32le','-ar','16000','-ac','1','-']),dtype=np.float32)
 segs,_=m.transcribe(audio,language='pt',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,initial_prompt='iB Mídias. Vidros, portões de alumínio, esquadrias. WhatsApp. Saiba Mais.')
 recognized=[{'text':w.word.strip(),'start':float(w.start),'end':float(w.end)} for seg in segs for w in seg.words]
 target=s['text'].replace('i bê','iB').replace('...','…').split();mapping={}
 sm=difflib.SequenceMatcher(a=[norm(w) for w in target],b=[norm(w['text']) for w in recognized],autojunk=False)
 for block in sm.get_matching_blocks():
  for q in range(block.size):mapping[block.a+q]=(recognized[block.b+q]['start'],recognized[block.b+q]['end'])
 # For a pronunciation or spelling mismatch, interpolate only between the adjacent timed words.
 for j in range(len(target)):
  if j not in mapping:
   before=max([k for k in mapping if k<j],default=-1);after=min([k for k in mapping if k>j],default=len(target))
   a=mapping[before][1] if before>=0 else 0;b=mapping[after][0] if after<len(target) else s['speechDuration'];step=max(.03,(b-a)/(after-before-1));mapping[j]=(a+(j-before-1)*step,a+(j-before)*step)
 words=[]
 for j,tx in enumerate(target):
  a,b=mapping[j];a=min(max(0,a),s['speechDuration']-.01);b=min(s['speechDuration'],max(a+.02,b));words.append({'text':tx,'start':round(s['start']+a,3),'end':round(s['start']+b,3),'hot':norm(tx) in ['vidros','portoes','esquadrias','whatsapp','orcamento','alto','padrao']})
 for j in range(len(words)-1):
  if (norm(words[j]['text']),norm(words[j+1]['text'])) in [('saiba','mais'),('menor','preco'),('maior','valor')]:words[j]['hot']=True;words[j+1]['hot']=True
 j=0
 while j<len(words):
  n=min(3,len(words)-j)
  for k in range(n):
   if re.search('[,.?!…]$',words[j+k]['text']):n=k+1;break
  if n>1 and norm(words[j+n-1]['text']) in ['de','e','o','a','para','no','na','ou','ao','seu','sua']:n-=1
  block=words[j:j+n];size=64
  while size>46:
   f=ImageFont.truetype(str(r/'public/fonts/Montserrat-ExtraBold.ttf'),size)
   if sum(f.getlength(w['text'].upper()) for w in block)+12*(n-1)+56<=880:break
   size-=2
  groups.append({'start':block[0]['start'],'end':min(s['start']+s['speechDuration']+.12,block[-1]['end']+.12),'words':block,'fontSize':size});j+=n
 review.append({'scene':i,'expected':s['text'],'recognized':' '.join(w['text'] for w in recognized),'matchedWords':sum(b.size for b in sm.get_matching_blocks()),'words':len(target)})
 print(i,review[-1],flush=True)
for i,g in enumerate(groups[:-1]):g['end']=min(g['end'],groups[i+1]['start'])
# Split the longest three-word label rather than reducing mobile text size.
fixed=[]
for c in groups:
 if ' '.join(w['text'].lower() for w in c['words'])=='criamos anúncios estratégicos':
  a=dict(c);a['words']=c['words'][:2];a['fontSize']=64;a['end']=c['words'][2]['start'];b=dict(c);b['words']=c['words'][2:];b['fontSize']=64;b['start']=b['words'][0]['start'];fixed.extend([a,b])
 else:fixed.append(c)
groups=fixed
(r/'public/captions.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2));(r/'speech-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2));(r/'public/timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2));print('CAPTIONS READY',len(groups),flush=True)
