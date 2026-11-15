from pathlib import Path
import json,numpy as np,subprocess,re,unicodedata,difflib,os,soundfile as sf
from faster_whisper import WhisperModel
from scenes import SCENES
r=Path(__file__).resolve().parents[1];os.environ['HF_HOME']='/workspace/.cache/huggingface';m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4);selected={int(i) for i in os.environ.get('ONLY_IDS','').split(',') if i};timings=json.loads((r/('public/timings-aligned.json' if selected else 'public/timings.json')).read_text());reviews=json.loads((r/'speech-review.json').read_text()) if selected else []
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
for v in timings:
 i=v['id']
 if selected and i not in selected:continue
 if selected:
  fresh=json.loads((r/f'public/audio/{i:02d}/meta.json').read_text());v.update(fresh);reviews=[rv for rv in reviews if rv['id']!=i]
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/f'public/audio/{i:02d}/speech.wav'),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
 segs,_=m.transcribe(a,language='pt',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,initial_prompt='iB Mídias. Vidraçaria, esquadrias, box, guarda-corpo, portão de alumínio. Seiscentos e cinquenta reais. WhatsApp. CRM.')
 recog=[{'text':w.word.strip(),'start':float(w.start),'end':float(w.end)} for s in segs for w in s.words];target=v['text'].split();matches={};sm=difflib.SequenceMatcher(a=[norm(w) for w in target],b=[norm(w['text']) for w in recog],autojunk=False)
 for block in sm.get_matching_blocks():
  for n in range(block.size):matches[block.a+n]=(recog[block.b+n]['start'],recog[block.b+n]['end'])
 originalMatched=len(matches)
 for j in range(len(target)):
  if j not in matches:
   before=max([k for k in matches if k<j],default=-1);after=min([k for k in matches if k>j],default=len(target));x=matches[before][1] if before>=0 else 0;y=matches[after][0] if after<len(target) else v['speechEnd']-.15;step=max(.02,(y-x)/(after-before-1));matches[j]=(x+(j-before-1)*step,x+(j-before)*step)
 words=[]
 for j,w in enumerate(target):
  x,y=matches[j];x=max(0,min(x,v['speechEnd']-.17));y=max(x+.02,min(y,v['speechEnd']-.15));words.append({'text':w,'start':round(x+.15,3),'end':round(y+.15,3),'hot':norm(w) in ['whatsapp','analise','crm','650','box','portao','acabamento','projeto','anuncios','vendas','bairro','medida','salva','controle','desconto']})
 for j in range(1,len(words)):
  words[j]['start']=max(words[j]['start'],words[j-1]['start']+.005);words[j]['end']=max(words[j]['end'],words[j]['start']+.02)
 if v['pauses']:
  original=next(c for c in json.loads((r/'campaign.json').read_text())['videos'] if c['id']==i)['narration']
  splitIndex=len(original.split('[pausa de 2 segundos]')[0].split());pause=v['pauses'][0]
  for word in words[:splitIndex]:word['end']=min(word['end'],pause['start'])
  for word in words[splitIndex:]:word['start']=max(word['start'],pause['end']);word['end']=max(word['end'],word['start']+.02)
 groups=[];j=0
 while j<len(words):
  n=min(3,len(words)-j)
  for k in range(n):
   if re.search('[,.?!…:]$',words[j+k]['text']) or (k<n-1 and words[j+k+1]['start']-words[j+k]['end']>.5):n=k+1;break
  if n>1 and norm(words[j+n-1]['text']) in ['o','a','e','de','do','da','por','no','na','seu','pra']:n-=1
  g=words[j:j+n];groups.append({'start':g[0]['start'],'end':min(v['speechEnd']+.1,g[-1]['end']+.1),'words':g});j+=n
 for j,g in enumerate(groups[:-1]):g['end']=min(g['end'],groups[j+1]['start'])
 scenes=[];lastIndex=0;nt=[norm(w) for w in target]
 for phrase,layout in SCENES[i]:
  if not phrase:scenes.append({'start':0,'layout':layout,'anchor':''});continue
  nparts=[norm(w) for w in phrase.split()];found=next((k for k in range(lastIndex,len(nt)-len(nparts)+1) if nt[k:k+len(nparts)]==nparts),None)
  if found is None:raise RuntimeError(f'Anchor not found: {i}, {phrase}')
  lastIndex=found
  if scenes[-1]['layout']==layout:continue
  scenes.append({'start':words[found]['start'],'layout':layout,'anchor':phrase})
 # Keep the final branded CTA visible for at least three seconds after narration.
 scenes[-1]['end']=v['duration'];v['scenes']=scenes
 audio,sr=sf.read(r/f'public/audio/{i:02d}/voice.wav');v['mouth']=[round(min(1,float(np.sqrt(np.mean(audio[round(f/30*sr):round((f+1)/30*sr)]**2)))/.13),3) for f in range(v['frames'])]
 (r/f'public/captions-{i:02d}.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2));(r/f'public/words-{i:02d}.json').write_text(json.dumps(words,ensure_ascii=False,indent=2));reviews.append({'id':i,'expected':v['text'],'recognized':' '.join(w['text'] for w in recog),'matchedWords':originalMatched,'targetWords':len(target)})
 print('ALIGNED',i,originalMatched,'/',len(target),'scenes',[(s['layout'],s['start']) for s in scenes],flush=True)
 (r/'speech-review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2));(r/'public/timings-aligned.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2))
print('COMPLETE',flush=True)

(r/'public/captions.json').write_text(json.dumps({str(v['id']):json.loads((r/f"public/captions-{v['id']:02d}.json").read_text()) for v in timings},ensure_ascii=False,indent=2))
