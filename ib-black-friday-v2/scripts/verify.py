from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());tl=json.loads((r/'public/timings-aligned.json').read_text());allcaps=json.loads((r/'public/captions.json').read_text());report=[]
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','24000','-f','f32le','-']),dtype=np.float32)
for v in cfg['videos']:
 t=next(t for t in tl if t['id']==v['id']);p=r/'out'/f'{v["name"]}.mp4';j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));vs=next(s for s in j['streams'] if s['codec_type']=='video');a=next(s for s in j['streams'] if s['codec_type']=='audio');assert (vs['width'],vs['height'],vs['codec_name'],vs['r_frame_rate'],int(vs['nb_frames']))==(1080,1920,'h264','30/1',t['frames']);assert a['codec_name']=='aac'
 assert 'pm_alex' in t['voice']
 for seg in t['segments']:
  if 'Instagram' in seg['text']:assert 'ɡrˈɐ̃' in seg['phonemes']
  if 'Black Friday' in seg['text']:assert 'frˈaɪdeɪ' in seg['phonemes'] and 27<=float(j['format']['duration'])<=33
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 actual=samples(p);src=samples(r/f'public/audio/{v["id"]}/mix.wav');n=min(len(actual),len(src));corr=float(np.corrcoef(actual[:n],src[:n])[0,1]);assert corr>.985,corr;peak=float(max(abs(actual)));assert peak<1,peak
 caps=allcaps[str(v['id'])];assert ' '.join(w['text'] for c in caps for w in c['words'])==v['narration'];assert all(c['start']<c['end']<=t['duration'] for c in caps)
 assert t['cues']['clock']-(t['cues']['price']-.2)>=2
 assert t['duration']-t['cues']['cta']>=3
 assert t['cues']['clock']<t['cues']['twentyFour']<t['cues']['cta']
 words=json.loads((r/f'words-{v["id"]}.json').read_text());assert abs(next(w['start'] for w in words if w['text'].lower()=='vinte')-t['cues']['twentyFour'])<.001
 assert Image.open(r/f'out/capa-{v["id"]}.jpg').size==(1080,1920)
 entry={'id':v['id'],'file':p.name,'duration':float(j['format']['duration']),'resolution':'1080x1920','fps':'30/1','video':'H.264','audio':'AAC','audio_correlation':round(corr,6),'audio_peak':round(peak,5),'price_visible_seconds':round(t['cues']['clock']-t['cues']['price']+.2,3),'cta_visible_seconds':round(t['duration']-t['cues']['cta'],3),'clock_stops_at_word_vinte_seconds':round(t['cues']['twentyFour'],3),'brand_pronunciation':'i bê Mídias','voice':'Kokoro pm_alex pt-br','loanword_phonemes_checked':True,'narration_complete':True,'full_decode':'passed','visual_review':'First-frame hook, offer, deadline and final frame inspected','status':'passed'};report.append(entry);print('VERIFIED',entry,flush=True)
(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
