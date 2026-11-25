from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];e=json.loads((r/'edit.json').read_text());s=(r/'captions.ass').read_text()
def ts(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02d}:{n//100%60:02d}.{n%100:02d}'
def ev(a,b,tx):return f'Dialogue: 7,{ts(a)},{ts(b)},Text,,0,0,0,,{tx}\n'
def title(a,b,tx,y,size=85):
 return ev(a,b,f'{{\\an5\\pos(540,{y})\\fs{size}\\c&HFFFFFF&\\3c&H241622&\\bord7\\shad0\\fscx92\\fscy92\\t(0,150,\\fscx100\\fscy100)\\fad(60,100)}}'+tx)
s+=title(.15,1.46,'DEU A LOUCA!',1280,88)
def mp(t):
 for x in e['segments']:
  if x['start']<=t<=x['end']:return x['outputStart']+(t-x['start'])/x['speed']
for a,b in [(13.56,14.4),(24.1,24.9)]:
 s+=title(mp(a),mp(b),'A PARTIR DE',360,52)
 s+=title(mp(a),mp(b),'R$ 1',470,130)
s+=title(e['outroStart']+.15,e['duration'],'BLACK FRIDAY',230,76)
s+=title(e['outroStart']+.15,e['duration'],'RUBY',335,48)
s+=title(e['outroStart']+.65,e['duration'],'PEÇAS A PARTIR DE R$ 1',1560,53)
(r/'captions.ass').write_text(s)
