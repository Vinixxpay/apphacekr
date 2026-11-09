from pathlib import Path
import os,json,subprocess
r=Path(__file__).resolve().parents[1];src=Path(os.environ.get('CAPTION_SOURCE',r/'input/original.MOV'))
if not src.exists():raise SystemExit('Defina CAPTION_SOURCE para o original.')
e=json.loads((r/'edit.json').read_text());s=e['segments'][0];a,b=s['sourceStart'],s['sourceEnd'];outro=r/'work/outro.mp4'
if not outro.exists():raise SystemExit('Execute scripts/make_outro.py primeiro.')
f=[f'[0:v]trim=start_frame={round(a*60)}:end_frame={round(b*60)},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,ass=filename={r}/captions.ass:fontsdir={r}/public/fonts[v0]',f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a0]','[1:v]setpts=PTS-STARTPTS,setsar=1[v1]','[1:a]atrim=duration=2.2,asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a1]','[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]']
(r/'out').mkdir(exist_ok=True);(r/'work/cache').mkdir(parents=True,exist_ok=True);os.environ['XDG_CACHE_HOME']=str(r/'work/cache');p=r/'out/ib-midias-vd4-legendas-logo.mp4'
cmd=['ffmpeg','-v','warning','-y','-threads','4','-i',str(src),'-threads','2','-i',str(outro),'-filter_complex_threads','2','-filter_complex',';'.join(f),'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','20','-maxrate','8M','-bufsize','16M','-threads','4','-r','60','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-movflags','+faststart','-progress',str(r/'work/progress.txt'),'-nostats',str(p)]
(r/'render-command.json').write_text(json.dumps({'source':src.name,'filter':';'.join(f),'output':p.name,'voiceSpeed':1,'framing':'Entire original frame scaled to 1080x1920','outro':'Official logo + iB Mídias; original short sound after the speech'},ensure_ascii=False,indent=2));subprocess.run(cmd,check=True);print('FINAL MP4 READY',flush=True)
