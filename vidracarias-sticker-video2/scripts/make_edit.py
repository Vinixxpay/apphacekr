from pathlib import Path
import json,re,unicodedata,math
r=Path(__file__).resolve().parents[1];raw=json.loads((r/'work/transcript.json').read_text())
config=json.loads((r/'source-edit.json').read_text())
for repl in config.get('replacementSegments',[]):
 a,b=repl['replaceRange'];raw['segments']=[s for s in raw['segments'] if not (a<=s['start'] and s['end']<=b)]+[repl['segment']]
raw['segments'].sort(key=lambda s:s['start'])
parts=[(a/30,b/30) for a,b in config['keepFrames']]
parts=[{'start':a,'end':b,'output':sum(y-x for x,y in parts[:i])} for i,(a,b) in enumerate(parts)]
def mapped(t):
 for p in parts:
  if p['start']<=t<=p['end']:return p['output']+t-p['start']
 return None
def norm(s):return re.sub('[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
words=[]
for s in raw['segments']:
 for original in s['words']:
  w=dict(original);key=str(w['start']);times=config.get('wordTimeOverrides',{}).get(norm(w['text'])+'@'+key,config.get('wordTimeOverrides',{}).get(key))
  if times:w['start'],w['end']=times
  if key in config.get('wordTextOverrides',{}):w['text']=config['wordTextOverrides'][key]
  a=mapped(w['start']);b=mapped(w['end'])
  if a is None or b is None:continue
  text=w['text'];n=norm(text)
  fixes={'boxe':'box','vida':'vidro','cações':'indicações'}
  if text.lower().strip('.,?!') in fixes:text=fixes[text.lower().strip('.,?!')]+('?' if '?' in text else '.' if '.' in text else ',' if ',' in text else '')
  words.append({'text':text,'start':round(a,4),'end':round(b,4),'sourceStart':w['start'],'sourceEnd':w['end']})
# Highlight phrases in natural two-word groups, without changing the recorded voice.
for i,w in enumerate(words[:-1]):
 if (norm(w['text']),norm(words[i+1]['text'])) in [('mais','barato'),('saiba','mais')]:w['highlight']=True;words[i+1]['highlight']=True
leading=['vidraceiro','voce quer','vender mais','mas toda vez','que manda','um orcamento','escuta','a outra ali','faz','mais barato','imagina duas','vidracarias','na mesma cidade','as duas','trabalham com','box','espelho','e porta','de vidro','e escuta','o outro','foi']
caps=[];i=0;stop={'e','de','da','do','no','na','com','para','pelo','a','o','um','uma','seu','sua'}
while i<len(words):
 n=0
 for phrase in leading:
  bits=phrase.split()
  if [norm(w['text']) for w in words[i:i+len(bits)]]==bits:n=len(bits);break
 if not n:
  n=min(3,len(words)-i)
  for k in range(n):
   if re.search('[,?.!]$',words[i+k]['text']):n=k+1;break
  if n>1 and norm(words[i+n-1]['text']) in stop:n-=1
  # Keep the two highlighted pairs together.
  if n>1 and norm(words[i+n-1]['text']) in ['mais','saiba'] and i+n<len(words) and norm(words[i+n]['text']) in ['barato','mais']:n-=1
 group=words[i:i+n];start=group[0]['start'];end=group[-1]['end'];nxt=words[i+n]['start'] if i+n<len(words) else end+.15
 caps.append({'start':start,'end':round(min(nxt,end+.18),4),'words':[{k:v for k,v in w.items() if not k.startswith('source')} for w in group]});i+=n
scene_specs=[tuple(s) for s in config['scenes']]
duration=sum(p['end']-p['start'] for p in parts);frames=round(duration*30);scenes=[]
for j,(kind,source,title) in enumerate(scene_specs):
 start=mapped(source);end=mapped(scene_specs[j+1][1]) if j+1<len(scene_specs) else frames/30
 local=[w for w in words if start<=w['start']<end]
 cues={}
 for key,alternatives in {'mais barato':['mais barato'],'box':['box'],'espelho':['espelho'],'porta':['porta'],'promoção':['promocao'],'desconto':['desconto'],'orçamentos':['compara'],'mede':['mede'],'material':['material'],'instala':['instala'],'lucro':['lucro','nada'],'acabamento':['acabamento'],'depoimentos':['depoimentos'],'confiar':['confiar'],'indicar':['indicar','indicacoes','indicacao'],'whatsapp':['whatsapp']}.items():
  cue=None
  for alt in alternatives:
   tokens=alt.split()
   for k,w in enumerate(local):
    if [norm(z['text']) for z in local[k:k+len(tokens)]]==tokens:cue=w['start']-start;break
   if cue is not None:break
  cues[key]=round(cue if cue is not None else max(.5,(end-start)*.45),4)
 if kind=='hook':cues['mais barato']=round(mapped(config['fastZooms'][0])-start,4)
 scenes.append({'kind':kind,'start':round(start,4),'end':round(end,4),'title':title,'cues':cues})
# Camera changes at real phrase boundaries, with three deliberately fast emphasis zooms.
zooms=[]
for s in raw['segments']:
 a=mapped(s['start'])
 if a is not None:zooms.append({'start':a,'scale':[1.0,1.06,1.10][len(zooms)%3],'fast':False})
for source in config['fastZooms']:
 a=mapped(source)
 if a is not None:zooms.append({'start':a,'scale':1.18,'fast':True});zooms.append({'start':a+1.8,'scale':1.04,'fast':False})
zooms.sort(key=lambda z:z['start'])
edit={'frames':frames,'scenes':scenes,'captions':caps}
(r/'src/data.ts').write_text("import type {Scene,Word} from './Film';\nexport const edit:"+"{frames:number;scenes:Scene[];captions:{start:number;end:number;words:Word[]}[]}="+json.dumps(edit,ensure_ascii=False,separators=(',',':'))+';\n')
plan={'source':config['source'],'sourceFramesPerSecond':30,'parts':parts,'frames':frames,'duration':frames/30,'zooms':zooms,'words':words,'edits':config['edits'],'audioPolicy':'Voz original, sem aceleração, clonagem ou remoção de pausas internas às tomadas mantidas.'}
(r/'edit-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2));(r/'work/edit.json').write_text(json.dumps(edit,ensure_ascii=False));print('EDIT',frames,frames/30,'seconds',len(words),'words',len(caps),'caption groups');print([(s['kind'],s['start'],s['end']) for s in scenes])
