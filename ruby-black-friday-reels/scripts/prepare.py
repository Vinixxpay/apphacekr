from pathlib import Path
import json,copy
r=Path(__file__).resolve().parents[1]
segments=[{'start':0,'end':4.4,'speed':3,'zoom':1},*({'start':a,'end':b,'speed':1,'zoom':z} for a,b,z in [(4.4,9.5,1.02),(9.5,14.4,1.1),(14.4,17,1.025),(17.2666666667,21.2,1.09),(21.4666666667,25.14,1.035),(25.14,30.4,1.08)])]
o=0
for s in segments:s['outputStart']=o;o+=(s['end']-s['start'])/s['speed'];s['outputEnd']=o
end=o;duration=end+3
words=[copy.deepcopy(w) for s in json.load(open('/workspace/scratch/black-friday-loja/transcript.json')) for w in s['words']]
for w in words:
 if w['text']=='boca':w['text']='louca'
 if w['text'].lower().rstrip('.')=='rubi':w['text']='Ruby'+('.' if w['text'].endswith('.') else '')
 if w['text']=='que' and w['start']==28.24:w['text']='e'
out=[]
for w in words:
 for s in segments:
  if s['start']<=w['start'] and w['end']<=s['end']:
   w.update(sourceStart=w['start'],sourceEnd=w['end'],start=s['outputStart']+(w['start']-s['start'])/s['speed'],end=s['outputStart']+(w['end']-s['start'])/s['speed']);out.append(w);break
(r/'edit.json').write_text(json.dumps({'fps':30,'segments':segments,'speechDuration':end,'duration':duration,'outroStart':end,'source':'input/original.mp4','outro':'Zoom animado sobre frame real da placa aos 32,9 segundos; sem alteração do texto da placa.'},ensure_ascii=False,indent=2))
(r/'transcript-reviewed.json').write_text(json.dumps({'words':out},ensure_ascii=False,indent=2))
s=Path('/workspace/apphacekr/lavai-gravacao-editada/scripts/make_captions.py').read_text()
a=s.index('phrases=[');b=s.index('\nphrases.sort',a)
s=s[:a]+"phrases=['deu a louca','na ruby','e isso mesmo','que voce ouviu','black friday','aqui na ruby','com produtos','a partir de','um real','voce escutou direito','a nossa','nos vamos fazer','o que nunca','foi visto','produtos e pecas','ta','entao corre','vem participar','da nossa black','e garante','seus produtinhos']"+s[b:]
a=s.index("w['highlight']=norm(w['text']) in ");b=s.index('\nfor i in range',a)
s=s[:a]+"w['highlight']=norm(w['text']) in ['louca','ruby','black','friday','um','real','corre','produtinhos']"+s[b:]
s=s.replace("GREEN='00B8FF'","GREEN='C9A0F4'").replace("BLUE='2A170F'","BLUE='241622'").replace('Y=1480','Y=1460')
(r/'scripts/make_captions.py').write_text(s)
print(duration,end,len(out))
