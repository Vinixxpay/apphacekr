from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];s=(r/'captions.ass').read_text();kept=json.loads((r/'edit.json').read_text())['keptSourceIntervals']
def ts(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}'
def mt(t):
 o=0
 for a,b in kept:
  if a<=t<=b:return o+t-a
  o+=b-a
 return o
# Remove old badge events when regenerating.
s='\n'.join(line for line in s.splitlines() if not line.startswith('Dialogue: 5,'))+'\n'
for a,b,tx in [(0,3.2,'LAVAÍ  •  GESTÃO NA PRÁTICA'),(11.8,16.65,'RELATÓRIOS E FATURAMENTO'),(26.65,29.1,'A IDENTIDADE DA SUA EMPRESA'),(47.4,52.9,'ACESSO PARA SUA EQUIPE'),(58.65,60.5,'ANDROID + iOS')]:
 s+=f'Dialogue: 5,{ts(mt(a))},{ts(mt(b))},Text,,0,0,0,,{{\\an5\\move(540,308,540,290,0,220)\\fad(150,150)\\fs46\\c&H00B8FF&\\3c&H2A170F&\\bord14\\shad0}}{tx}\n'
(r/'captions.ass').write_text(s)
