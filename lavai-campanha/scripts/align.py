from pathlib import Path
import json,numpy as np,subprocess,re,unicodedata,difflib,os
from faster_whisper import WhisperModel
r=Path(__file__).resolve().parents[1];os.environ['HF_HOME']='/workspace/.cache/huggingface';m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4);timings=json.loads((r/'timings.json').read_text());reviews=[]
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
for v in timings:
 i=v['id'];a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/f'public/audio/v{i}/speech.wav'),'-vn','-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32);segs,_=m.transcribe(a,language='pt',beam_size=5,word_timestamps=True,vad_filter=False,condition_on_previous_text=False,initial_prompt='Lavaí App. Lava-jato. Lava-rápido. Trinta e nove reais e noventa centavos por mês. Saiba Mais. WhatsApp.')
 recog=[{'text':w.word.strip(),'start':float(w.start),'end':float(w.end)} for s in segs for w in s.words];target=v['text'].replace('...','…').split();matches={};sm=difflib.SequenceMatcher(a=[norm(w) for w in target],b=[norm(w['text']) for w in recog],autojunk=False)
 for block in sm.get_matching_blocks():
  for n in range(block.size):matches[block.a+n]=(recog[block.b+n]['start'],recog[block.b+n]['end'])
 for j in range(len(target)):
  if j not in matches:
   before=max([k for k in matches if k<j],default=-1);after=min([k for k in matches if k>j],default=len(target));x=matches[before][1] if before>=0 else 0;y=matches[after][0] if after<len(target) else v['speechDuration'];step=max(.025,(y-x)/(after-before-1));matches[j]=(x+(j-before-1)*step,x+(j-before)*step)
 words=[]
 for j,w in enumerate(target):
  x,y=matches[j];x=max(0,min(x,v['speechDuration']-.02));y=max(x+.02,min(y,v['speechDuration']));words.append({'text':w,'start':round(x+.16,3),'end':round(y+.16,3),'hot':norm(w) in ['lavai','caderno','controle','clientes','servicos','whatsapp','profissional','organizacao','organiza']})
 for j in range(1,len(words)):
  words[j]['start']=max(words[j]['start'],words[j-1]['start']+.005);words[j]['end']=max(words[j]['end'],words[j]['start']+.02)
 groups=[];j=0
 while j<len(words):
  n=min(3,len(words)-j)
  for k in range(n):
   if re.search('[,.?!…]$',words[j+k]['text']):n=k+1;break
  if n>1 and norm(words[j+n-1]['text']) in ['o','a','e','de','do','da','por','no','na','seu']:n-=1
  group=words[j:j+n];groups.append({'start':group[0]['start'],'end':min(v['speechEnd']+.12,group[-1]['end']+.1),'words':group});j+=n
 for j,g in enumerate(groups[:-1]):g['end']=min(g['end'],groups[j+1]['start'])
 def cue(token,after=0,default=0):
  return next((w['start'] for w in words if norm(w['text'])==norm(token) and w['start']>=after),default)
 intro=cue('Lavaí',default=v['duration']*.42);price=cue('trinta',default=v['speechEnd']-6);cta=cue('Clique',after=price,default=v['speechEnd']-2)
 v['cues']={'intro':intro,'price':price,'cta':cta,'clients':cue('clientes',after=intro,default=intro+1),'services':cue('serviços',after=intro,default=intro+2.6),'receipt':cue('comprovantes',after=max(0,intro-7),default=intro+4),'notebook':cue('caderno',default=4),'imagine':cue('Imagina',default=5.4)}
 if i==2:v['cues']['demoServices']=cue('serviços',after=v['cues']['imagine'],default=v['cues']['imagine']+2)
 (r/f'public/captions-{i}.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2));(r/f'public/words-{i}.json').write_text(json.dumps(words,ensure_ascii=False,indent=2));audio,sr=__import__('soundfile').read(r/f'public/audio/v{i}/voice.wav');v['mouth']=[round(min(1,float(np.sqrt(np.mean(audio[round(f/30*sr):round((f+1)/30*sr)]**2)))/.13),3) for f in range(v['frames'])]
 reviews.append({'id':i,'expected':v['text'],'recognized':' '.join(w['text'] for w in recog),'matchedWords':sum(b.size for b in sm.get_matching_blocks()),'targetWords':len(target)});print('ALIGNED',i,v['cues'],reviews[-1]['recognized'],flush=True)
(r/'timings.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2));(r/'public/timings.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2));(r/'speech-review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2))
