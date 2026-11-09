from pathlib import Path
import json,re,unicodedata,difflib,math
from PIL import ImageFont
r=Path(__file__).resolve().parents[1]
def norm(s):return re.sub('[^a-z0-9 ]','',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode())
words=json.loads((r/'transcript-reviewed.json').read_text())['words']
for i,w in enumerate(words):
 if i:w['start']=max(w['start'],words[i-1]['start']+.01)
 w['end']=max(w['end'],w['start']+.02)
 w['highlight']=norm(w['text']) in ['vidraceiro','vidraçaria','vidracaria','orcamento','orcamentos','whatsapp']
for i in range(len(words)-1):
 if (norm(words[i]['text']),norm(words[i+1]['text'])) in [('vender','mais'),('mais','barato'),('saiba','mais')]:words[i]['highlight']=True;words[i+1]['highlight']=True
phrases=['vidraceiro','voce ta cansado','de depender','so de indicacao','aqui na','ib midias','nos trabalhamos','com um metodo','mvp','onde ai trabalha','o marketing','venda','e o teu','posvenda','entao aqui','a gente consegue','fazer um marketing','qualificado','a gente tem','um script','de vendas','pra voce','vender mais','pros teus clientes','pra nao ficar','so pedindo','orcamento orcamento','ai a gente','vende mais','e o posvenda','onde a gente','faz toda','a qualificacao','pergunta como','e que ta','o produto','e a gente','qualifica voce','e o seu','lead','para fechar','entao se voce','quer ter esse','mesmo resultado','clica aqui','no saiba mais','e fala comigo']
phrases.sort(key=lambda s:-len(s.split()));caps=[];i=0;stop={'e','de','da','do','no','na','com','para','pelo','a','o','um','uma','seu','sua','que','ou'}
while i<len(words):
 n=0
 for phrase in phrases:
  tokens=phrase.split()
  if [norm(w['text']) for w in words[i:i+len(tokens)]]==tokens:n=len(tokens);break
 if not n:
  n=min(3,len(words)-i)
  for k in range(n):
   if re.search(r'[,?!.]$',words[i+k]['text']):n=k+1;break
  if n>1 and norm(words[i+n-1]['text']) in stop:n-=1
 for k in range(1,n):
  if words[i+k]['start']-words[i+k-1]['end']>.65:n=k;break
 group=words[i:i+n];caps.append({'start':group[0]['start'],'end':group[-1]['end'],'words':group});i+=n
for i,c in enumerate(caps):
 nxt=caps[i+1]['start'] if i+1<len(caps) else c['end']+.18;c['end']=min(nxt,c['end']+.18)
# The last spoken group remains briefly; no added outro or held empty-chair footage.
caps[-1]['end']=json.loads((r/'edit.json').read_text())['speechDuration']-.03
fontpath=r/'public/fonts/Montserrat-ExtraBold.ttf';ASS_FONT_FACTOR=1.562;BLUE='CD3101';LIGHT='E9A78C';GREEN='01FCB9';WHITE='FFFFFF';Y=1490
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\nYCbCr Matrix: TV.709\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Text,Montserrat ExtraBold,64,&H00CD3101,&H00E9A78C,&H00CD3101,&HFF000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\nStyle: Shape,Montserrat ExtraBold,1,&H00FFFFFF,&H00FFFFFF,&H00CD3101,&HFF000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
def time(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}'
def rect(w,h,radius=16):
 w,h=round(w),round(h);rr=min(radius,w//2,h//2);return f'm {rr} 0 l {w-rr} 0 b {w-rr//2} 0 {w} {rr//2} {w} {rr} l {w} {h-rr} b {w} {h-rr//2} {w-rr//2} {h} {w-rr} {h} l {rr} {h} b {rr//2} {h} 0 {h-rr//2} 0 {h-rr} l 0 {rr} b 0 {rr//2} {rr//2} 0 {rr} 0'
rows=[]
def event(layer,a,b,style,txt):
 if b-a>.005:rows.append(f'Dialogue: {layer},{time(a)},{time(b)},{style},,0,0,0,,{txt}')
for c in caps:
 texts=[w['text'].upper() for w in c['words']];size=64
 while True:
  f=ImageFont.truetype(str(fontpath),size);widths=[f.getlength(tx) for tx in texts];box=sum(widths)+20*(len(texts)-1)+60
  if box<=866 or size<=44:break
  size-=2
 assert box<=866,(texts,box);height=round(size*1.22+24);left=540-box/2;top=Y-height/2;c['fontSize']=size;c['box']={'x':left,'y':top,'width':box,'height':height}
 # Three tiny size steps produce a restrained pop, centered on the group.
 edges=[(c['start'],min(c['end'],c['start']+.033),.97),(c['start']+.033,min(c['end'],c['start']+.066),.985),(c['start']+.066,c['end'],1.)]
 for a,b,s in edges:
  bw,bh=box*s,height*s;x,y=540-bw/2,Y-bh/2
  event(0,a,b,'Shape',f'{{\\an7\\pos({x:.2f},{y+5:.2f})\\c&H000000&\\alpha&HDD&\\bord0\\blur3\\p1}}{rect(bw,bh)}{{\\p0}}')
  event(1,a,b,'Shape',f'{{\\an7\\pos({x:.2f},{y:.2f})\\c&H{WHITE}&\\alpha&H00&\\3c&H{BLUE}&\\bord3\\shad0\\p1}}{rect(bw,bh)}{{\\p0}}')
 x=left+30
 for w,tx,ww in zip(c['words'],texts,widths):
  cx=x+ww/2;start=max(c['start'],w['start']);end=c['end']
  if w['highlight']:event(2,start,end,'Shape',f'{{\\an7\\pos({x-7:.2f},{Y-size*.59:.2f})\\c&H{GREEN}&\\bord0\\shad0\\p1}}{rect(ww+14,size*1.18,9)}{{\\p0}}')
  def tag(color,at):
   elapsed=at-c['start'];scale=min(100,97+30*elapsed);remain=max(0,100-round(elapsed*1000));pop=f'\\fscx{scale:.2f}\\fscy{scale:.2f}\\t(0,{remain},\\fscx100\\fscy100)' if remain>0 else ''
   return f'{{\\an5\\pos({cx:.2f},{Y})\\fs{size*ASS_FONT_FACTOR:.3f}\\c&H{color}&\\bord0\\shad0{pop}}}'+tx.replace('{','').replace('}','')
  event(3,c['start'],min(start,end),'Text',tag(LIGHT,c['start']));event(3,start,end,'Text',tag(BLUE,start));x+=ww+20
(r/'captions.ass').write_text(header+'\n'.join(rows)+'\n');(r/'captions.json').write_text(json.dumps({'sourceTimeline':'Cortes editoriais em edit.json, sem mudança de velocidade','placement':{'centerX':540,'centerY':Y,'maxBoxWidth':866},'groups':caps},ensure_ascii=False,indent=2));print('CAPTIONS READY',len(words),'words',len(caps),'groups','duration',caps[-1]['end'])
