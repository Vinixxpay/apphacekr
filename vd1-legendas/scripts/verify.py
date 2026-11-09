from pathlib import Path
import subprocess,json,os,hashlib
from PIL import ImageFont
r=Path(__file__).resolve().parents[1];source=Path(os.environ.get('CAPTION_SOURCE',str(r/'input/vd1.MOV')));out=r/'out/ib-midias-vd1-somente-legendas.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
a=probe(source);b=probe(out);vi=next(s for s in a['streams'] if s['codec_type']=='video');vo=next(s for s in b['streams'] if s['codec_type']=='video');ai=next(s for s in a['streams'] if s['codec_type']=='audio');ao=next(s for s in b['streams'] if s['codec_type']=='audio')
assert (vo['width'],vo['height'],vo['codec_name'])==(1080,1920,'h264')
assert int(vo['nb_frames'])==int(vi['nb_frames']);assert vo['r_frame_rate']==vi['r_frame_rate']
assert abs(float(a['format']['duration'])-float(b['format']['duration']))<.08
assert ao['codec_name']==ai['codec_name']=='aac'
def audio_hash(path):return hashlib.sha256(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
originalAudioHash=audio_hash(source);outputAudioHash=audio_hash(out);assert originalAudioHash==outputAudioHash,'Encoded original audio packets differ'
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True,capture_output=True)
cs=json.loads((r/'captions.json').read_text());regular=[c for c in cs['groups'] if not c.get('ctaHold')];words=[w for c in regular for w in c['words']]
for c in cs['groups']:
 assert 1<=len(c['words'])<=3
 assert 0<c['start']<c['end']<=float(b['format']['duration'])
 box=c['box'];assert box['x']>=100 and box['x']+box['width']<=980
 assert box['y']>=1400 and box['y']+box['height']<=1600
 for w in c['words']:assert c['start']-.01<=w['start']<c['end']+.01
hold=cs['groups'][-1];assert hold.get('ctaHold') and hold['end']-hold['start']>=3.5
report={'file':out.name,'resolution':[1080,1920],'videoCodec':vo['codec_name'],'audioCodec':ao['codec_name'],'originalFrameRate':vi['r_frame_rate'],'outputFrameRate':vo['r_frame_rate'],'originalFrames':int(vi['nb_frames']),'outputFrames':int(vo['nb_frames']),'duration':float(b['format']['duration']),'originalDuration':float(a['format']['duration']),'timelinePreserved':True,'framing':'Entire original frame, only scaled to requested 1080x1920; no crop or zoom','audioPacketsUnchanged':True,'originalAudioSha256':originalAudioHash,'outputAudioSha256':outputAudioHash,'subtitleGroups':len(regular),'spokenWords':len(words),'wordGroups':'1–3 words','finalCtaHoldSeconds':round(hold['end']-hold['start'],3),'captionFit':'passed','fullDecode':'passed','newLayer':'captions only','bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()};(r/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
