from pathlib import Path
import os,json,subprocess
r=Path(__file__).resolve().parents[1];src=Path(os.environ.get('CAPTION_SOURCE',r/'input/vd3.mp4'))
if not src.exists():raise SystemExit('Defina CAPTION_SOURCE ou coloque o original em input/vd3.mp4')
e=json.loads((r/'edit.json').read_text());parts=e['segments'];f=[f'[0:v]scale=1080:1920:flags=lanczos,split={len(parts)}'+''.join(f'[src{i}]' for i in range(len(parts)))]
for i,s in enumerate(parts):
 a,b=s['sourceStart'],s['sourceEnd']
 f.append(f'[src{i}]trim=start_frame={round(a*60)}:end_frame={round(b*60)},setpts=PTS-STARTPTS[v{i}]')
 f.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]')
f.append(''.join(f'[v{i}][a{i}]' for i in range(len(parts)))+f'concat=n={len(parts)}:v=1:a=1[vc][a]')
f.append(f"[vc]ass=filename='{r/'captions.ass'}':fontsdir='{r/'public/fonts'}'[v]")
(r/'work/cache').mkdir(parents=True,exist_ok=True);(r/'out').mkdir(exist_ok=True);os.environ['XDG_CACHE_HOME']=str(r/'work/cache')
cmd=['ffmpeg','-v','warning','-y','-threads','4','-i',str(src),'-filter_complex_threads','2','-filter_complex',';'.join(f),'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','20','-maxrate','8M','-bufsize','16M','-threads','4','-pix_fmt','yuv420p','-r','60','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart','-progress',str(r/'work/progress.txt'),'-nostats',str(r/'out/ib-midias-vd3-legendas-e-cortes.mp4')]
(r/'render-command.json').write_text(json.dumps({'input':src.name,'filter':';'.join(f),'output':'ib-midias-vd3-legendas-e-cortes.mp4','speed':1,'originalFraming':True,'addedLayer':'Only dynamic subtitles','audio':'Original voice, only approved editorial trims and AAC encoding'},ensure_ascii=False,indent=2))
subprocess.run(cmd,check=True);print('RENDER READY',flush=True)
