from pathlib import Path
import json,subprocess,hashlib
import numpy as np,soundfile as sf
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-reels-voz-brasileira.mp4';tl=json.loads((r/'timeline.json').read_text());caps=json.loads((r/'public/captions.json').read_text());review=json.loads((r/'speech-review.json').read_text());events=json.loads((r/'sound-events.json').read_text())
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in j['streams'] if t['codec_type']=='video');a=next(t for t in j['streams'] if t['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],a['codec_name'])==(1080,1920,'h264','30/1','aac')
assert 60<=float(j['format']['duration'])<=75 and abs(float(j['format']['duration'])-tl['duration'])<.08
assert int(v['nb_frames'])==tl['frames'] and len(tl['scenes'])==7
font=ImageFont.truetype(str(r/'public/fonts/Montserrat-ExtraBold.ttf'),68);maxlines=0
for c in caps:
 assert 1<=len(c['words'])<=3 and 0<=c['start']<c['end']<=tl['duration'];lines=['']
 for w in c['words']:
  assert font.getlength(w['text'])<940
  line=(lines[-1]+' '+w['text']).strip()
  if font.getlength(line)>940:lines.append(w['text'])
  else:lines[-1]=line
 assert len(lines)<=2,lines;maxlines=max(maxlines,len(lines))
expected,sr=sf.read(r/'public/audio/mix.wav');expected=expected.mean(axis=1);actual=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar',str(sr),'-ac','1','-f','f32le','-']),dtype=np.float32);n=min(len(expected),len(actual));corr=float(np.corrcoef(expected[:n],actual[:n])[0,1]);assert corr>.99,corr
peak=float(np.max(np.abs(actual)));assert peak<1,peak
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'resolution':[1080,1920],'fps':30,'duration':float(j['format']['duration']),'frames':int(v['nb_frames']),'sequences':7,'direction':'Cartoon 2D according to the supplied written brief','voice':'Brazilian Portuguese male, Kokoro pm_santa','script':'All seven narration passages included','captionWords':sum(len(c['words']) for c in caps),'captionGroups':len(caps),'maximumCaptionLines':maxlines,'effectsSynchronized':len(events),'audioCorrelationWithMix':corr,'peak':peak,'ctaVisibleSeconds':tl['scenes'][-1]['end']-tl['scenes'][-1]['start']-6.5,'holdAfterSpeechSeconds':tl['scenes'][-1]['end']-tl['scenes'][-1]['start']-tl['scenes'][-1]['speechDuration'],'comparison':'Hypothetical 4 small services versus 1 project, no invented prices','customerMessages':'Illustrative, labeled as such','roles':'Agency: ads and opportunities; company: service, negotiation and closing','fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
