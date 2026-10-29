from pathlib import Path
import subprocess,json,time,wave,math
import numpy as np
from scipy.signal import correlate
r=Path(__file__).resolve().parents[1];out=r/'out/review';data=json.loads((r/'work/review-data.json').read_text());counts={f['id']:f['frames'] for f in data['films']};counts['r2-client']=data['client']['frames']
def ready(p,n):
 try:
  x=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(p)],stderr=subprocess.DEVNULL));return int(x['streams'][0]['nb_frames'])==n
 except Exception:return False
for name,n in counts.items():
 while not ready(out/f'{name}.mp4',n):time.sleep(2)
plans=[
 {'id':'01-completo','name':'Gravação completa com áudio da cliente','parts':[('r2-2203',0,483),('r2-client',0,counts['r2-client']),('r2-2203',483,counts['r2-2203'])]},
 {'id':'02-direto','name':'Versão direta com áudio da cliente','parts':[('r2-2200',0,309),('r2-client',0,counts['r2-client']),('r2-2200',309,counts['r2-2200'])]},
 {'id':'03-apresentacao','name':'Apresentação, áudio da cliente e convite','parts':[('r2-2197',0,counts['r2-2197']),('r2-client',0,counts['r2-client']),('r2-2196',0,counts['r2-2196'])]},
 {'id':'04-depoimento','name':'Áudio da cliente e convite completo','parts':[('r2-client',0,counts['r2-client']),('r2-2196',0,counts['r2-2196'])]}
]
# Original recordings are retained from the beginning to the end; insertions are in measured silence.
audit={}
for code,t in [('2203',16.1),('2200',10.3)]:
 with wave.open(str(r/'public/video'/f'r2-{code}-voice.wav')) as w:
  sr=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float).reshape(-1,w.getnchannels()).mean(1)/32768
 z=a[round((t-.12)*sr):round((t+.12)*sr)];db=20*np.log10(np.sqrt(np.mean(z*z))+1e-12);assert db < -40,(code,db);audit[code]={'insertionSeconds':t,'pauseRmsDb':round(float(db),2)}
clientwav=r/'public/video/r2-client-voice.wav';clientoriginal=next((r/'input').rglob('*.m4a'))
original=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(clientoriginal),'-ar','48000','-ac','1','-f','f32le','-']),np.float32)
with wave.open(str(clientwav)) as w: normalizedSamples=w.getnframes()
assert len(original)==normalizedSamples,(len(original),normalizedSamples)
ref=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(clientwav),'-ar','8000','-ac','1','-f','f32le','-']),np.float32).astype(float)
for plan in plans:
 target=out/f"revisado-{plan['id']}.mp4";args=['ffmpeg','-v','error','-y','-filter_complex_threads','1'];filters=[];links=[];frames=0;parts=[]
 for i,(name,a,b) in enumerate(plan['parts']):
  args+=['-threads','1','-i',str(out/f'{name}.mp4')]
  duration=(b-a)/30;filters += [f'[{i}:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,setsar=1[v{i}]',f'[{i}:a]atrim=start={a/30}:end={b/30},asetpts=PTS-STARTPTS,apad,atrim=duration={duration}[a{i}]'];links.append(f'[v{i}][a{i}]')
  parts.append({'source':name,'sourceStartFrame':a,'sourceEndFrame':b,'outputStartFrame':frames,'frames':b-a})
  if name=='r2-client':clientStart=frames/30
  frames+=b-a
 plan['frames']=frames;plan['duration']=frames/30;plan['clientStartSeconds']=clientStart;plan['parts']=parts
 if not target.exists():
  filters+=[''.join(links)+f'concat=n={len(parts)}:v=1:a=1[v][a]']
  args+=['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','19','-threads','3','-pix_fmt','yuv420p','-r','30','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(target)]
  subprocess.run(args,check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)]));v=next(z for z in info['streams'] if z['codec_type']=='video');assert int(v['nb_frames'])==frames;assert v['width']==1080 and v['height']==1920;assert abs(float(info['format']['duration'])-frames/30)<.12
 # Compare the beginning, middle and final words of the full client message with the encoded delivery.
 captureStart=max(0,clientStart-.12)
 cap=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(captureStart),'-i',str(target),'-t',str(data['client']['audioDuration']+.3),'-ar','8000','-ac','1','-f','f32le','-']),np.float32).astype(float)
 assert len(cap)>=len(ref)
 cross=correlate(cap,ref,mode='valid',method='fft');lag=int(np.argmax(cross));sample=cap[lag:lag+len(ref)]
 def similarity(a,b):return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12))
 scores={'full':similarity(sample,ref),'beginning':similarity(sample[:24000],ref[:24000]),'end':similarity(sample[-24000:],ref[-24000:])}
 assert min(scores.values())>.90,(plan['id'],scores)
 offset=captureStart+lag/8000-clientStart;assert abs(offset)<.08,(plan['id'],offset)
 plan['audioVerification']={'originalDecodedSamples48k':len(original),'normalizedSamples48k':normalizedSamples,'fullMessagePreserved':True,'alignmentOffsetSeconds':round(offset,5),'correlation':scores}
 print(plan['id'],round(frames/30,2),'s','mensagem inteira conferida',scores,flush=True)
manifest={'revision':2,'clientAudioSeconds':data['client']['audioDuration'],'pauseAudit':audit,'videos':plans}
(r/'review-delivery.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('QUATRO VERSÕES REVISADAS CONCLUÍDAS',flush=True)
