from pathlib import Path
import json,subprocess,sys
r=Path(__file__).resolve().parents[1];e=json.loads((r/'edit.json').read_text());source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True);segs=e['segments'];f=[]
f.append('[0:v]fps=30,split='+str(len(segs))+''.join(f'[s{i}]' for i in range(len(segs))))
labels=[]
for i,s in enumerate(segs):
 a,b,z=s['start'],s['end'],s['zoom'];dur=(b-a)/s['speed'];cw=round(1080/z/2)*2;ch=round(1920/z/2)*2
 f.append(f"[s{i}]trim=start={a}:end={b},setpts=(PTS-STARTPTS)/{s['speed']},crop={cw}:{ch}:(iw-ow)/2:(ih-oh)/2,scale=1080:1920:flags=lanczos,setsar=1,eq=contrast=1.025:saturation=1.04:brightness=0.003[v{i}]")
 if i==0:f.append(f'anullsrc=r=48000:cl=stereo,atrim=duration={dur},asetpts=PTS-STARTPTS[a{i}]')
 else:f.append(f'[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,afade=t=out:st={dur-.006}:d=0.006[a{i}]')
 labels.append(f'[v{i}][a{i}]')
zoom='1+0.8*pow(min(on/48,1),2)*(3-2*min(on/48,1))'
f.append(f"[1:v]zoompan=z='{zoom}':x='max(0,540-27*min(on/48,1)-iw/(2*zoom))':y='max(0,960-260*min(on/48,1)-ih/(2*zoom))':d=90:s=1080x1920:fps=30,setsar=1,eq=contrast=1.025:saturation=1.04[voutro]")
f.append('anullsrc=r=48000:cl=stereo,atrim=duration=3,asetpts=PTS-STARTPTS[aoutro]')
f.append(''.join(labels)+'[voutro][aoutro]'+f'concat=n={len(segs)+1}:v=1:a=1[vc][ac]')
f.append(f"[vc]ass=filename={r/'captions.ass'}:fontsdir={r/'public/fonts'}[v]")
f.append('[ac]highpass=f=75,afftdn=nf=-40:nr=5:tn=1,equalizer=f=250:t=q:w=1:g=-1,acompressor=threshold=0.13:ratio=2:attack=10:release=150,loudnorm=I=-16:TP=-2:LRA=9,aresample=48000[voice]')
f.append('[voice][2:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=0:latency=1[a]')
(r/'render-filter.txt').write_text(';\n'.join(f))
subprocess.run(['ffmpeg','-hide_banner','-y','-filter_complex_threads','1','-i',str(source),'-i',str(r/'public/placa-original.jpg'),'-i',str(r/'public/music-and-effects.wav'),'-filter_complex_script',str(r/'render-filter.txt'),'-map','[v]','-map','[a]','-c:v','libx264','-crf','19','-preset','fast','-maxrate','8M','-bufsize','16M','-threads','4','-pix_fmt','yuv420p','-r','30','-fps_mode','cfr','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-progress','/tmp/ruby-bf-progress.txt',str(out)],check=True)
