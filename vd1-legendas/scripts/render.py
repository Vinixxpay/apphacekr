from pathlib import Path
import os,subprocess,json
r=Path(__file__).resolve().parents[1];source=Path(os.environ.get('CAPTION_SOURCE',str(r/'input/vd1.MOV')))
if not source.exists():raise SystemExit('Provide input/vd1.MOV or set CAPTION_SOURCE to the untouched original.')
(r/'out').mkdir(exist_ok=True);(r/'work/cache').mkdir(parents=True,exist_ok=True);os.environ['XDG_CACHE_HOME']=str(r/'work/cache')
p=r/'out/ib-midias-vd1-somente-legendas.mp4'
# No cuts, timeline changes, camera moves, grading, audio filters, logos or music.
cmd=['ffmpeg','-v','warning','-y','-i',str(source),'-map','0:v:0','-map','0:a:0','-vf',f"scale=1080:1920:flags=lanczos,ass=filename='{r/'captions.ass'}':fontsdir='{r/'public/fonts'}'",'-fps_mode','passthrough','-c:v','libx264','-preset','fast','-crf','20','-maxrate','8M','-bufsize','16M','-threads','4','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-metadata:s:v:0','rotate=0','-movflags','+faststart','-progress',str(r/'work/progress.txt'),'-nostats',str(p)]
(r/'render-command.json').write_text(json.dumps({'input':source.name,'videoFilters':'scale=1080:1920,ass=captions.ass','audio':'stream copy, no filters','timing':'passthrough original timestamps and frame rate','fullOriginal':True,'output':p.name},indent=2));subprocess.run(cmd,check=True);print('CAPTIONS-ONLY MP4 READY',str(p),flush=True)
