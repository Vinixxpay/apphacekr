from pathlib import Path
import json,re,unicodedata,difflib,subprocess,numpy as np
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());source=Path('/workspace/scratch/stories-4-originais');allcaps={};meta={}
def norm(s):
 n=re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode());return {'lojista':'logista','griffe':'grife','bela':'bella','vitrine':'vitina','look':'lugar','festa':'fecha'}.get(n,n)
for key,v in cfg['voices'].items():
 aid=int(key);folder=r/f'public/audio/{aid}';folder.mkdir(parents=True,exist_ok=True);duration=max(t['duration'] for t in cfg['videos'] if t['audio']==aid)
 trim=v['trimStart'];length=v['trimEnd']-trim
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(trim),'-t',str(length),'-i',str(source/f'{aid}.ogg'),'-af',f'highpass=f=70,lowpass=f=11000,loudnorm=I=-16:TP=-2:LRA=8,aresample=48000,apad=whole_dur={duration}', '-ar','48000','-ac','2',str(folder/'voice.wav')],check=True)
 recog=[w for s in json.loads((r/f'{aid}-transcript.json').read_text()) for w in s['words']];target=v['text'].split();sm=difflib.SequenceMatcher(a=[norm(w) for w in target],b=[norm(w['text']) for w in recog],autojunk=False);mapping={}
 for b in sm.get_matching_blocks():
  for j in range(b.size):mapping[b.a+j]=(recog[b.b+j]['start'],recog[b.b+j]['end'])
 for j in range(len(target)):
  if j not in mapping:
   left=max([i for i in mapping if i<j],default=-1);right=min([i for i in mapping if i>j],default=len(target));x=mapping[left][1] if left>=0 else trim;y=mapping[right][0] if right<len(target) else v['trimEnd'];step=max(.025,(y-x)/max(1,right-left-1));mapping[j]=(x+(j-left-1)*step,x+(j-left)*step)
 words=[]
 for j,text in enumerate(target):
  x,y=mapping[j];x=max(0,x-trim);y=max(x+.025,y-trim);words.append({'text':text,'start':round(x,3),'end':round(y,3),'hot':norm(text) in [norm(w) for w in ['lojista','vitrine','tamanho','coleção','festa','combinações','Natal','virada']]})
 for j in range(1,len(words)):words[j]['start']=max(words[j]['start'],words[j-1]['start']+.005);words[j]['end']=max(words[j]['end'],words[j]['start']+.025)
 groups=[];j=0
 while j<len(words):
  n=min(3,len(words)-j)
  for k in range(n):
   if re.search('[,.?!:]$',words[j+k]['text']):n=k+1;break
  if n>1 and norm(words[j+n-1]['text']) in ['a','o','e','de','na','no','sua','para','em','ao']:n-=1
  g=words[j:j+n];groups.append({'start':g[0]['start'],'end':min(length+.05,g[-1]['end']+.12),'words':g});j+=n
 for c,nxt in zip(groups,groups[1:]):c['end']=min(c['end'],nxt['start'])
 allcaps[str(aid)]=groups;meta[str(aid)]={'source':f'{aid}.ogg','trimStart':trim,'trimEnd':v['trimEnd'],'speechEnd':max(w['end'] for w in words),'duration':duration,'sourceText':v['text'],'transcriptCorrection':'Grafia da marca confirmada pelo usuário; correções ortográficas em lojista, vitrine, look e festa. Voz original preservada.'}
 (r/f'words-{aid}.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
(r/'public/captions.json').write_text(json.dumps(allcaps,ensure_ascii=False,indent=2));(r/'audio-metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print(meta,flush=True)
