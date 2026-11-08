from pathlib import Path
import json,re,unicodedata,math
r=Path(__file__).resolve().parents[1];raw=json.loads((r/'work/transcript.json').read_text())
# Trim only setup/tail and the abandoned 'no seu lucro' before the corrected phrase.
parts=[(123/30,956/30),(980/30,2310/30),(2359/30,2468/30)]
parts=[{'start':a,'end':b,'output':sum(y-x for x,y in parts[:i])} for i,(a,b) in enumerate(parts)]
def mapped(t):
 for p in parts:
  if p['start']<=t<=p['end']:return p['output']+t-p['start']
 return None
def norm(s):return re.sub('[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
words=[]
for s in raw['segments']:
 for w in s['words']:
  a=mapped(w['start']);b=mapped(w['end'])
  if a is None or b is None:continue
  text=w['text'];n=norm(text)
  fixes={'boxe':'box','vida':'vidro','cações':'indicações'}
  if text.lower().strip('.,?!') in fixes:text=fixes[text.lower().strip('.,?!')]+('?' if '?' in text else '.' if '.' in text else ',' if ',' in text else '')
  words.append({'text':text,'start':round(a,4),'end':round(b,4),'sourceStart':w['start'],'sourceEnd':w['end']})
# Highlight phrases in natural two-word groups, without changing the recorded voice.
for i,w in enumerate(words[:-1]):
 if (norm(w['text']),norm(words[i+1]['text'])) in [('mais','barato'),('saiba','mais')]:w['highlight']=True;words[i+1]['highlight']=True
leading=['vidraceiro','voce quer','vender mais','mas toda vez','que manda','um orcamento','escuta','a outra ali','faz','mais barato','imagina duas','vidracarias','na mesma cidade','as duas','trabalham com','box','espelho','e porta','de vidro']
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
scene_specs=[('hook',4.1,'VOCÊ OUVE ISSO?'),('shops',11.56,'DUAS LOJAS. A MESMA CIDADE.'),('price',18.22,'PREÇO SOZINHO VIRA COMPARAÇÃO.'),('trust',34.09,'PROJETOS QUE GERAM CONFIANÇA.'),('map',48.27,'SEJA ENCONTRADO NA SUA REGIÃO.'),('ads',59.41,'DO ANÚNCIO À CONVERSA.'),('cta',68.35,'SUA VIDRAÇARIA EM DESTAQUE.')]
duration=sum(p['end']-p['start'] for p in parts);frames=round(duration*30);scenes=[]
for j,(kind,source,title) in enumerate(scene_specs):
 start=mapped(source);end=mapped(scene_specs[j+1][1]) if j+1<len(scene_specs) else frames/30
 local=[w for w in words if start<=w['start']<end]
 cues={}
 for key,alternatives in {'mais barato':['mais barato'],'box':['box'],'espelho':['espelho'],'porta':['porta'],'promoção':['promocao'],'desconto':['desconto'],'orçamentos':['compara'],'mede':['mede'],'material':['material'],'instala':['instala'],'lucro':['nada'],'acabamento':['acabamento'],'depoimentos':['depoimentos'],'confiar':['confiar'],'indicar':['indicacao'],'whatsapp':['whatsapp']}.items():
  cue=None
  for alt in alternatives:
   tokens=alt.split()
   for k,w in enumerate(local):
    if [norm(z['text']) for z in local[k:k+len(tokens)]]==tokens:cue=w['start']-start;break
   if cue is not None:break
  cues[key]=round(cue if cue is not None else max(.5,(end-start)*.45),4)
 if kind=='hook':cues['mais barato']=round(mapped(9.58)-start,4)
 scenes.append({'kind':kind,'start':round(start,4),'end':round(end,4),'title':title,'cues':cues})
# Camera changes at real phrase boundaries, with three deliberately fast emphasis zooms.
zooms=[]
for s in raw['segments']:
 a=mapped(s['start'])
 if a is not None:zooms.append({'start':a,'scale':[1.0,1.06,1.10][len(zooms)%3],'fast':False})
for source in [9.58,30.6,80.25]:
 a=mapped(source)
 if a is not None:zooms.append({'start':a,'scale':1.18,'fast':True});zooms.append({'start':a+1.8,'scale':1.04,'fast':False})
zooms.sort(key=lambda z:z['start'])
edit={'frames':frames,'scenes':scenes,'captions':caps}
(r/'src/data.ts').write_text("import type {Scene,Word} from './Film';\nexport const edit:"+"{frames:number;scenes:Scene[];captions:{start:number;end:number;words:Word[]}[]}="+json.dumps(edit,ensure_ascii=False,separators=(',',':'))+';\n')
plan={'sourceFramesPerSecond':30,'parts':parts,'frames':frames,'duration':frames/30,'zooms':zooms,'words':words,'edits':[{'source':[0,4.1],'reason':'Preparação antes da fala'},{'source':[956/30,980/30],'reason':'Trecho abandonado “no seu lucro”; preserva “no seu bolso” e a frase inteira'},{'source':[77.0,2359/30],'reason':'Pergunta com tropeço na dicção; preserva “Quer vender mais?” e o convite completo ao Saiba Mais'}, {'source':[2468/30,raw['duration']],'reason':'Após o fim da fala'}],'audioPolicy':'Voz original, sem aceleração, clonagem ou remoção de pausas internas às tomadas mantidas.'}
(r/'edit-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2));(r/'work/edit.json').write_text(json.dumps(edit,ensure_ascii=False));print('EDIT',frames,frames/30,'seconds',len(words),'words',len(caps),'caption groups');print([(s['kind'],s['start'],s['end']) for s in scenes])
