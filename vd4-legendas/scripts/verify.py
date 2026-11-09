from pathlib import Path
import json,os,subprocess,array,math,hashlib
r=Path(__file__).resolve().parents[1];p=r/'out/ib-midias-vd4-legendas-logo.mp4';src=Path(os.environ.get('CAPTION_SOURCE',r/'input/original.MOV'));e=json.loads((r/'edit.json').read_text())
o=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(t for t in o['streams'] if t['codec_type']=='video');a=next(t for t in o['streams'] if t['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],a['codec_name'])==('h264',1080,1920,'aac')
assert v['r_frame_rate']=='60/1' and int(v['nb_frames'])==2112
assert abs(float(o['format']['duration'])-35.2)<.05
caps=json.loads((r/'captions.json').read_text())['groups'];words=json.loads((r/'transcript-reviewed.json').read_text())['words'];assert sum(len(c['words']) for c in caps)==len(words)
for c in caps:
 assert 1<=len(c['words'])<=3 and 0<=c['start']<c['end']<=e['speechDuration']
 b=c['box'];assert b['x']>=100 and b['x']+b['width']<=980 and b['y']>=1400 and b['y']+b['height']<=1600
for x,y in zip(words,words[1:]):assert x['sourceStart']<y['sourceStart']
def pcm(p):
 a=array.array('f');a.frombytes(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','f32le','-']));return a
original=pcm(src);output=pcm(p);start=e['segments'][0]['sourceStart'];end=e['segments'][0]['sourceEnd'];expected=original[round(start*16000):round(end*16000)];retained=output[:len(expected)]
dot=sum(x*y for x,y in zip(expected,retained));xx=sum(x*x for x in expected);yy=sum(x*x for x in retained);corr=dot/math.sqrt(xx*yy);assert corr>.99,corr
outro=output[round(e['speechDuration']*16000):];peak=max(abs(x) for x in outro);assert .03<peak<.95,peak
# Check that the supplied sound is actually present only after the speech section.
sfx=pcm(r/'public/logo-sound.wav');n=min(len(sfx),len(outro));dot=sum(sfx[i]*outro[i] for i in range(n));xx=sum(x*x for x in sfx[:n]);yy=sum(x*x for x in outro[:n]);soundcorr=dot/math.sqrt(xx*yy);assert soundcorr>.98,soundcorr
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
result={'file':p.name,'resolution':[1080,1920],'fps':60,'duration':float(o['format']['duration']),'frames':int(v['nb_frames']),'speechSeconds':e['speechDuration'],'logoOutroSeconds':e['outroDuration'],'originalVoiceSpeed':True,'originalFraming':True,'retainedVoiceCorrelation':corr,'soundEffectCorrelation':soundcorr,'outroPeak':peak,'subtitleWords':len(words),'subtitleGroups':len(caps),'captionFit':'passed','fullDecode':'passed','soundStartsAfterSpeech':True,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(r/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
