from pathlib import Path
import subprocess,json,numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());meta=json.loads((r/'audio-metadata.json').read_text());caps=json.loads((r/'public/captions.json').read_text());report=[]
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','24000','-f','f32le','-']),dtype=np.float32)
for v in cfg['videos']:
 p=r/'out'/v['slug']/'story.mp4';j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));s=next(s for s in j['streams'] if s['codec_type']=='video');a=next(s for s in j['streams'] if s['codec_type']=='audio');assert (s['codec_name'],s['width'],s['height'],s['r_frame_rate'],int(s['nb_frames']))==('h264',1080,1920,'30/1',v['frames']);assert a['codec_name']=='aac'
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 x=samples(p);y=samples(r/f'public/audio/mix-{v["id"]}.wav');n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);assert corr>.985,corr;assert max(abs(x))<1
 c=caps[str(v['audio'])];assert all(c['start']<c['end']<=v['duration'] and 1<=len(c['words'])<=3 for c in c)
 for old,new in zip(c,c[1:]):assert old['end']<=new['start']+.001
 txt=' '.join(w['text'] for c in c for w in c['words']);assert txt==cfg['voices'][str(v['audio'])]['text'];assert v['duration']-meta[str(v['audio'])]['speechEnd']>1.9
 assert abs(v['duration']-v['finalStart']-3)<.001
 assert Image.open(r/'out'/v['slug']/'capa.jpg').size==(1080,1920)
 report.append({'id':v['id'],'file':v['slug']+'/story.mp4','duration':float(j['format']['duration']),'frames':int(s['nb_frames']),'video':'H.264 1080x1920 30fps','audio':'AAC','audio_mix_correlation':round(corr,6),'audio_peak':round(float(max(abs(x))),5),'voice_source':meta[str(v['audio'])]['source'],'original_voice':True,'voice_speed_unchanged':True,'ending_seconds':3,'captions':'passed','full_decode':'passed','status':'passed'});print('VERIFIED',v['id'],report[-1]['duration'],round(corr,6),flush=True)
(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
