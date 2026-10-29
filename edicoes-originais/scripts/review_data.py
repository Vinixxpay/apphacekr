from pathlib import Path
import json,subprocess,math,wave
import numpy as np
r=Path(__file__).resolve().parents[1]
# Whole recordings. Only an insertion is made, inside a pause, for the complete client audio.
phase={
 '2203':[(0,'swap'),(8.4,'demand'),(13.5,'listen'),(16.1,'sold'),(25.7,'expectation'),(33.3,'funnel'),(42,'people'),(50,'proposal'),(54.6,'cta')],
 '2200':[(0,'swap'),(7.3,'listen'),(10.3,'sold'),(15.5,'cta')],
 '2197':[(0,'people'),(3.2,'listen')],
 '2196':[(0,'sold'),(7.6,'cta'),(10.5,'people'),(14.55,'cta')]}
films=[]
for code in ['2203','2200','2197','2196']:
 pid='r2-'+code;proxy=r/'work'/f'IMG_{code}-proxy.mp4';x=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration','-of','json',str(proxy)]));v=x['streams'][0];n=int(v['nb_frames']);dur=n/30
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(proxy),'-vn','-ar','16000','-ac','1','-f','f32le','-']),np.float32);step=640;wv=np.array([np.sqrt(np.mean(a[i:i+step]**2)) for i in range(0,len(a),step)]);wv=np.clip(wv/(np.percentile(wv,90)+1e-6)*.75,0,1)
 seg=[]
 for i,(start,theme) in enumerate(phase[code]):
  end=phase[code][i+1][0] if i+1<len(phase[code]) else dur
  seg.append({'from':start,'duration':end-start,'theme':theme})
 words=[]
 raw=json.loads((r/'work'/f'IMG_{code}-transcript.json').read_text())
 for segment in raw['segments']:
  for w in segment['words']:
   text=w['text'].strip();z=w['start']
   if code=='2203':
    if 45<=z<49.8:continue
    if 23.43<=z<23.54:text='vendeu'
    if 23.54<=z<23.66:continue
    if 29.47<=z<29.88 and text.strip(',.')=='é':continue
    if 32.25<=z<32.48:
     if z<32.34:text='alinha';w={**w,'end':32.48}
     else:continue
    if 32.48<=z<32.97:text='a expectativa.'
    if 57.53<=z<57.70:text='uma'
    if 57.89<=z<58.10:continue
   if code=='2200' and 2.58<=z<3.98:text='trocar'
   for bad,good in [('Seba','Saiba'),('Ceiba','Saiba'),('preste','preencha'),('IB','iB'),('lides','leads'),('milagroso.','milagrosos.'),('agente','agende')]:text=text.replace(bad,good)
   words.append({'start':w['start'],'end':w['end'],'text':text})
 cues=[];group=[]
 for w in words:
  if group and (len(group)>=4 or len(' '.join(x['text'] for x in group))+len(w['text'])>31 or w['start']-group[-1]['end']>.42):
   cues.append({'start':group[0]['start'],'end':group[-1]['end']+.12,'words':group});group=[]
  group.append(w)
 if group:cues.append({'start':group[0]['start'],'end':min(dur,group[-1]['end']+.15),'words':group})
 if code=='2203':cues.append({'start':45.1,'end':49.6,'words':[{'start':45.1,'end':49.6,'text':'Para empresários de diferentes ramos.'}]})
 cues.sort(key=lambda c:c['start'])
 for c,nextc in zip(cues,cues[1:]):c['end']=min(c['end'],nextc['start'])
 films.append({'id':pid,'source':'IMG_'+code,'frames':n,'duration':dur,'segments':seg,'wave':[round(float(q),3) for q in wv],'captions':cues})
# Client message is kept whole, including the ends of all words. No speculative transcript is displayed.
clientfile=next((r/'input').rglob('*.m4a'));wav=r/'public/video/r2-client-voice.wav'
if not wav.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(clientfile),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','pcm_s16le',str(wav)],check=True)
with wave.open(str(wav)) as w:
 rate=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype('float32').reshape(-1,w.getnchannels()).mean(1)/32768
samples=len(a);dur=samples/rate;n=math.ceil(dur*30);step=round(rate/25);wv=[round(min(1,float(np.sqrt(np.mean(a[i:i+step]**2)))*6),3) for i in range(0,len(a),step)]
client={'id':'r2-client','frames':n,'duration':n/30,'audioDuration':dur,'samples':samples,'wave':wv,'captions':[]}
(r/'src/review-data.ts').write_text('export const reviewFilms='+json.dumps(films,ensure_ascii=False,separators=(',',':'))+';\nexport const clientFilm='+json.dumps(client,separators=(',',':'))+';\n')
(r/'work/review-data.json').write_text(json.dumps({'films':films,'client':client},ensure_ascii=False))
print('Source frames',[(f['id'],f['frames']) for f in films],'client',n,dur)
