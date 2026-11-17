from pathlib import Path
import json,re,unicodedata,difflib,subprocess,numpy as np,os
from faster_whisper import WhisperModel
r=Path(__file__).resolve().parents[1];os.environ['HF_HOME']='/workspace/.cache/huggingface';m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4);tl=json.loads((r/'public/timings.json').read_text());allcaps={};reviews=[]
def norm(s):
 n=re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode());return {'pra':'para','ib':'ibe'}.get(n,n)
for v in tl:
 words=[];review=[]
 for seg in v['segments']:
  a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/f'public/audio/{v["id"]}/{seg["kind"]}.wav'),'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32);s,_=m.transcribe(a,language='pt',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,initial_prompt='Black Friday da iB Mídias. i bê Mídias. Instagram, Facebook, Google, WhatsApp. Seiscentos e cinquenta reais. Vinte e quatro horas.')
  rec=[{'text':w.word.strip(),'start':w.start,'end':w.end} for x in s for w in x.words];fixed=[];j=0
  while j<len(rec):
   if j+1<len(rec) and norm(rec[j]['text'])=='i' and norm(rec[j+1]['text']) in ['be','b']:
    fixed.append({'text':'iB','start':rec[j]['start'],'end':rec[j+1]['end']});j+=2
   else:fixed.append(rec[j]);j+=1
  rec=fixed;target=seg['text'].split();sm=difflib.SequenceMatcher(a=[norm(w) for w in target],b=[norm(w['text']) for w in rec],autojunk=False);match={}
  for b in sm.get_matching_blocks():
   for j in range(b.size):match[b.a+j]=(rec[b.b+j]['start'],rec[b.b+j]['end'])
  count=len(match)
  for j in range(len(target)):
   if j not in match:
    left=max([n for n in match if n<j],default=-1);right=min([n for n in match if n>j],default=len(target));x=match[left][1] if left>=0 else 0;y=match[right][0] if right<len(target) else seg['end']-seg['start'];d=max(.02,(y-x)/max(1,right-left-1));match[j]=(x+(j-left-1)*d,x+(j-left)*d)
   x,y=match[j];words.append({'text':target[j],'start':round(seg['start']+x,3),'end':round(seg['start']+max(x+.02,y),3),'hot':norm(target[j]) in ['caro','resultado','black','friday','seiscentos','cinquenta','reais','vinte','quatro','horas','saiba','mais','whatsapp']})
  review.append({'kind':seg['kind'],'expected':seg['text'],'recognized':' '.join(w['text'] for w in rec),'matched':count,'words':len(target)})
 for j in range(1,len(words)):words[j]['start']=max(words[j]['start'],words[j-1]['start']+.005);words[j]['end']=max(words[j]['end'],words[j]['start']+.02)
 groups=[];j=0
 while j<len(words):
  n=min(3,len(words)-j)
  for z in range(n):
   if re.search('[,.?!]$',words[j+z]['text']) or (z<n-1 and words[j+z+1]['start']-words[j+z]['end']>.32):n=z+1;break
  if n>1 and norm(words[j+n-1]['text']) in ['o','a','e','de','da','do','no','na','por','em','ate']:n-=1
  g=words[j:j+n];groups.append({'start':g[0]['start'],'end':g[-1]['end']+.1,'words':g});j+=n
 for g,n in zip(groups,groups[1:]):g['end']=min(g['end'],n['start'])
 def find(token,after=0):return next(w['start'] for w in words if norm(w['text'])==norm(token) and w['start']>=after)
 v['cues']['problem']=find('recebeu') if v['id']==1 else find('mas');v['cues']['twentyFour']=find('vinte',v['cues']['clock']);v['cues']['hoursEnd']=next(w['end'] for w in words if norm(w['text'])=='horas');v['platformCues']={name:find(name) for name in ['Instagram','Facebook','Google']}
 allcaps[str(v['id'])]=groups;reviews.append({'id':v['id'],'segments':review});(r/f'words-{v["id"]}.json').write_text(json.dumps(words,ensure_ascii=False,indent=2));print('ALIGNED',v['id'],v['cues'],review,flush=True)
(r/'public/timings-aligned.json').write_text(json.dumps(tl,ensure_ascii=False,indent=2));(r/'public/captions.json').write_text(json.dumps(allcaps,ensure_ascii=False,indent=2));(r/'speech-review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2))
