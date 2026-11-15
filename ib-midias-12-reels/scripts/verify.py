from pathlib import Path
import subprocess,json,re,os,numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());tl=json.loads((r/'public/timings-aligned.json').read_text());report=[]
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','24000','-f','f32le','-']),dtype=np.float32)
for v in cfg['videos']:
 if os.environ.get('ONLY_IDS') and v['id'] not in {int(i) for i in os.environ['ONLY_IDS'].split(',')}:continue
 t=next(t for t in tl if t['id']==v['id']);p=r/'out'/v['slug']/'reel.mp4';j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));vs=next(s for s in j['streams'] if s['codec_type']=='video');a=next(s for s in j['streams'] if s['codec_type']=='audio')
 assert (vs['width'],vs['height'],vs['codec_name'],vs['r_frame_rate'])==(1080,1920,'h264','30/1')
 assert vs['pix_fmt'] in ['yuv420p','yuvj420p'] and int(vs['nb_frames'])==t['frames'] and a['codec_name']=='aac'
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 source=samples(r/f'public/audio/{v["id"]:02d}/mix.wav');actual=samples(p);n=min(len(source),len(actual));corr=float(np.corrcoef(source[:n],actual[:n])[0,1]);assert corr>.985,corr
 peak=float(max(abs(actual)));assert peak<1,peak
 caps=json.loads((r/f'public/captions-{v["id"]:02d}.json').read_text());assert all(1<=len(c['words'])<=3 and 0<=c['start']<c['end']<=t['duration'] for c in caps)
 expected=re.sub(r'\s+',' ',v['narration'].replace('[pausa de 2 segundos]','')).strip();captxt=' '.join(w['text'] for c in caps for w in c['words']);assert captxt==expected
 for c,nxt in zip(caps,caps[1:]):assert c['end']<=nxt['start']+.001,(v['id'],c,nxt)
 assert t['duration']-t['speechEnd']>=2.99
 for pause in t['pauses']:
  assert abs(pause['end']-pause['start']-2)<.001
  assert not any(c['start']<pause['end'] and c['end']>pause['start'] for c in caps)
  raw=samples(r/f'public/audio/{v["id"]:02d}/voice.wav');sil=raw[round((pause['start']+.02)*24000):round((pause['end']-.02)*24000)];assert max(abs(sil))<.001
 cover=r/'out'/v['slug']/'capa.jpg';assert Image.open(cover).size==(1080,1920)
 assert t['scenes'][-1]['layout'] in ['offer','final'] and t['duration']-t['scenes'][-1]['start']>=3
 entry={'id':v['id'],'slug':v['slug'],'duration_seconds':float(j['format']['duration']),'video':f"H.264 / {vs['pix_fmt']} / 1080x1920 / 30 fps",'audio':'AAC','frames':int(vs['nb_frames']),'audio_correlation':round(corr,6),'audio_peak':round(peak,5),'caption_groups':len(caps),'full_narration_in_captions':True,'full_decode':'passed','cover':'1080x1920','quiz_pause_seconds':2 if t['pauses'] else None,'ending_hold_after_voice_seconds':round(t['duration']-t['speechEnd'],3),'status':'passed'};report.append(entry);print('VERIFIED',v['id'],entry['duration_seconds'],'audio',round(corr,6),flush=True)
(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
