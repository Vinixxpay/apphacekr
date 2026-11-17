from pathlib import Path
import json,copy
r=Path(__file__).resolve().parents[1];src=Path('/workspace/scratch/lavai-gravacao')
removed=[(3.5,3.93),(10.46,11.1),(20.43,22.96),(29.4,29.9),(32.65,33.4),(37.93,41.03),(43.05,44.8),(57.16,58.43)]
# Frame-accurate cuts at 30fps, preserving breathing space around speech.
removed=[(round(a*30)/30,round(b*30)/30) for a,b in removed]
kept=[];last=0
for a,b in removed:kept.append([last,a]);last=b
kept.append([last,60.5]);duration=sum(b-a for a,b in kept)
def mapped(t):
 offset=0
 for a,b in kept:
  if a<=t<=b:return offset+t-a
  offset+=b-a
 return None
words=[copy.deepcopy(w) for s in json.loads((src/'transcript.json').read_text()) for w in s['words']]
# Correct recognizer mistakes and align words which crossed detected silent sections.
for i,w in enumerate(words):
 if w['text']=='lava':w['text']='lava-jato';w['end']=words[i+1]['end'];words[i+1]['text']=''
 if w['text']=='admissão,':w['text']='admin,'
 if w['text']=='equip,':w['text']='equipe,'
 if w['text']=='equip':w['text']='equipe'
 if w['text']=='tem' and w['start']==2.18:w['text']='ter'
 if w['text']=='vendas,' and 10<w['start']<12:w['start']=9.86;w['end']=10.28
 if w['text']=='sair,':w['end']=32.4
 if w['text']=='cliente' and w['start']>35:w['end']=37.3
 if w['text']=='fez.' and w['start']>35:w['start']=37.3;w['end']=37.71
 if w['text']=='aplicativo' and w['start']>55:w['start']=56.38;w['end']=56.92
 if w['text']=='tanto' and w['start']>55:w['start']=58.65;w['end']=58.84
 if w['text']=='aplicativo' and w['start']<4:w['end']=3.31
 if w['text']=='ou' and 3<w['start']<4:w['start']=4.1
out=[]
for w in words:
 if not w['text']:continue
 # Retain only words belonging to kept source intervals.
 center=(w['start']+w['end'])/2
 if mapped(center) is None:continue
 a=mapped(w['start']);b=mapped(w['end'])
 if a is None:a=mapped(center)
 if b is None:b=mapped(center)+.04
 w.update(sourceStart=w['start'],sourceEnd=w['end'],start=a,end=max(a+.03,b));out.append(w)
(r/'edit.json').write_text(json.dumps({'fps':30,'source':'input/original.mp4','keptSourceIntervals':kept,'removedSourceIntervals':removed,'speechDuration':duration,'notes':'Pausas longas e repetição da apresentação da equipe removidas. Sem mudança de voz ou velocidade.'},ensure_ascii=False,indent=2))
(r/'transcript-reviewed.json').write_text(json.dumps({'words':out},ensure_ascii=False,indent=2))
print('Duração:',duration,'Palavras:',len(out))
