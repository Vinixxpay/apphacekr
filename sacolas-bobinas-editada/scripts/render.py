from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parents[1];e=json.loads((r/'edit.json').read_text());source=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.parent.mkdir(parents=True,exist_ok=True)
f=[];labels=[]
for i,(a,b) in enumerate(e['keptSourceIntervals']):
 f.append(f'[0:v]trim=start_frame={round(a*30)}:end_frame={round(b*30)},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1[v{i}]')
 f.append(f'[0:a]atrim=start={a:.8f}:end={b:.8f},asetpts=PTS-STARTPTS,afade=t=in:d=0.007,afade=t=out:st={b-a-.007:.8f}:d=0.007[a{i}]')
 labels.append(f'[v{i}][a{i}]')
f.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=1[vcat][acat]')
f.append(f"[vcat]ass=filename={r/'captions.ass'}:fontsdir={r/'public/fonts'}[v]")
f.append('[acat]highpass=f=75,afftdn=nf=-40:nr=5:tn=1,equalizer=f=280:t=q:w=0.8:g=-1.5,equalizer=f=2800:t=q:w=0.8:g=1.5,acompressor=threshold=0.1:ratio=2:attack=15:release=180:makeup=1.5,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000[a]')
(r/'render-filter.txt').write_text(';\n'.join(f))
cmd=['ffmpeg','-hide_banner','-y','-filter_complex_threads','1','-i',str(source),'-filter_complex_script',str(r/'render-filter.txt'),'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','19','-maxrate','8M','-bufsize','16M','-threads','4','-pix_fmt','yuv420p','-r','30','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-c:a','aac','-b:a','192k','-movflags','+faststart','-progress','/tmp/sacolas-render-progress.txt',str(dest)]
subprocess.run(cmd,check=True)
