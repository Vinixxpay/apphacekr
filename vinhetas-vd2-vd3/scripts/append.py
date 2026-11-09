from pathlib import Path
import subprocess,json,hashlib,concurrent.futures,os
r=Path(__file__).resolve().parents[1];repo=r.parent;outro=repo/'vd4-legendas/work/outro.mp4';sound=repo/'vd4-legendas/public/logo-sound.wav'
sources={n:Path(os.environ.get(f'VD{n}_INPUT',str(repo/f'entregas/ib-midias-vd{n}-legendas-e-cortes.mp4'))) for n in [2,3]}
outro_video=r/'work/outro-video.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(outro),'-map','0:v:0','-c:v','copy','-an',str(outro_video)],check=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def render(n):
 src=sources[n];old=repo/f'entregas/ib-midias-vd{n}-legendas-e-cortes.mp4';assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(old.read_bytes()).digest()
 p=probe(src);v=next(t for t in p['streams'] if t['codec_type']=='video');frames=int(v['nb_frames']);duration=frames/60
 video_only=r/f'work/vd{n}-video.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-map','0:v:0','-c:v','copy','-an',str(video_only)],check=True)
 lst=r/f'work/vd{n}.ffconcat';lst.write_text(f"ffconcat version 1.0\nfile '{video_only}'\nduration {duration:.12f}\nfile '{outro_video}'\nduration 2.2\n")
 dest=repo/f'entregas/ib-midias-vd{n}-com-final-logo.mp4'
 cmd=['ffmpeg','-v','warning','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(src),'-i',str(sound),'-filter_complex_threads','1','-filter_complex',f'[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=mono[a0];[2:a]atrim=duration=2.2,asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=mono[a1];[a0][a1]concat=n=2:v=0:a=1[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)]
 subprocess.run(cmd,check=True)
 q=probe(dest);ov=next(t for t in q['streams'] if t['codec_type']=='video')
 assert (ov['width'],ov['height'],ov['codec_name'])==(1080,1920,'h264')
 assert int(ov['nb_frames'])==frames+132
 assert abs(float(q['format']['duration'])-(duration+2.2))<.05
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(dest),'-f','null','-'],check=True)
 # Compare decoded pixels before the outro at three points, including the last speaking frame.
 def md5(path,t):return subprocess.check_output(['ffmpeg','-v','error','-threads','2','-ss',str(t),'-i',str(path),'-frames:v','1','-an','-f','md5','-']).decode().strip()
 for t in [.5,round(duration/2,3),round(duration-.2,3)]:assert md5(src,t)==md5(dest,t),(n,t)
 result={'file':dest.name,'inputUploadVerified':True,'resolution':[1080,1920],'fps':60,'originalDuration':duration,'finalDuration':float(q['format']['duration']),'originalFrames':frames,'finalFrames':int(ov['nb_frames']),'mainVideo':'Stream copy, no re-encoding, cropping, or timeline changes','decodedFrameSamples':'identical','voice':'Original voice in full; sound added only after the original ends','outroSeconds':2.2,'outro':'Same official iB Mídias logo animation and sonic signature as approved video 4','fullDecode':'passed','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size}
 print(json.dumps(result,ensure_ascii=False),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(render,[2,3]))
(r/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
