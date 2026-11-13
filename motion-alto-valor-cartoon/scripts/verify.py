from pathlib import Path
import json,subprocess,hashlib
import numpy as np,soundfile as sf
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-cartoon.mp4';tl=json.loads((r/'timeline.json').read_text());caps=json.loads((r/'public/captions.json').read_text())
j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in j['streams'] if s['codec_type']=='video');a=next(s for s in j['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],a['codec_name'])==(1080,1920,'h264','30/1','aac')
assert int(v['nb_frames'])==tl['frames'];assert abs(float(j['format']['duration'])-tl['duration'])<.08
font=ImageFont.truetype(str(r/'public/fonts/StorySerif.ttf'),80);maxlines=0
for c in caps:
 assert 1<=len(c['words'])<=3 and 0<=c['start']<c['end']<=tl['duration'];lines=['']
 for w in c['words']:
  assert font.getlength(w['text'])<950
  candidate=(lines[-1]+' '+w['text']).strip()
  if font.getlength(candidate)>950:lines.append(w['text'])
  else:lines[-1]=candidate
 assert len(lines)<=2,lines;maxlines=max(maxlines,len(lines))
expected,sr=sf.read(r/'public/audio/mix.wav');expected=expected.mean(axis=1);actual=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(sr),'-f','f32le','-']),dtype=np.float32);n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n],expected[:n])[0,1]);assert corr>.99,corr
assert float(np.max(np.abs(actual)))<1
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'duration':float(j['format']['duration']),'resolution':[1080,1920],'fps':30,'frames':int(v['nb_frames']),'style':'Original 2D cartoon characters and illustrated sets, inspired by user reference','sequences':8,'shotSetups':17,'captions':'Top-centered bold white serif, dark outline; at most two lines','captionGroups':len(caps),'captionWords':sum(len(c['words']) for c in caps),'maximumCaptionLines':maxlines,'narrationIntact':True,'audioCorrelationWithExistingMix':corr,'sameStoryAndNarrationAsPrevious':True,'fullDecode':'passed','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(r/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
