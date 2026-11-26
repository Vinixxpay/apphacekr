from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1];root=r.parent;base=root/'entregas/ruby-black-friday/ruby-black-friday-reels.mp4';out=root/'entregas/ruby-black-friday-v3/ruby-black-friday-cartaz.mp4';out.parent.mkdir(parents=True,exist_ok=True)
f=[]
f.append('[2:v]trim=duration=2.3,format=rgba,fade=t=in:d=0.18:alpha=1,fade=t=out:st=1.8:d=0.5:alpha=1,split=2[g1][g2]')
f.append('[g1]setpts=PTS-STARTPTS+10.45/TB[gg1]');f.append('[g2]setpts=PTS-STARTPTS+20.45/TB[gg2]')
f.append('[0:v][gg1]overlay=0:0:eof_action=pass:repeatlast=0[v1]');f.append('[v1][gg2]overlay=0:0:eof_action=pass:repeatlast=0[v2]')
f.append('[1:v]scale=300:300:flags=lanczos,format=rgba,fade=t=out:st=1.65:d=0.35:alpha=1,setpts=PTS-STARTPTS+10.6266666667/TB[coin]')
u='(t-10.6266666667)';y=f'if(lt({u},0.36),40+1050*pow({u}/0.36,2),1090-100*abs(sin(({u}-0.36)*9))*exp(-2.6*({u}-0.36)))'
f.append(f"[v2][coin]overlay=x=715:y='{y}':eof_action=pass:repeatlast=0[composite]")
f.append('[composite]trim=end_frame=808,setpts=PTS-STARTPTS,setsar=1,format=yuv420p[head]')
f.append('[4:v]setpts=PTS-STARTPTS,setsar=1,format=yuv420p[outro]')
f.append('[head][outro]concat=n=2:v=1:a=0[v]')
f.append('[0:a][3:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=0:latency=1,apad,atrim=duration=30.9333333333[a]')
(r/'render-filter.txt').write_text(';\n'.join(f))
subprocess.run(['ffmpeg','-hide_banner','-y','-filter_complex_threads','1','-i',str(base),'-i',str(root/'ruby-black-friday-moeda/public/coin-3d.mov'),'-loop','1','-framerate','30','-i',str(root/'ruby-black-friday-moeda/public/lateral-glow.png'),'-i',str(r/'public/coin-first-fx.wav'),'-i',str(r/'public/outro-cartaz.mp4'),'-filter_complex_script',str(r/'render-filter.txt'),'-map','[v]','-map','[a]','-t','30.9333333333','-c:v','libx264','-preset','fast','-crf','18','-maxrate','8M','-bufsize','16M','-threads','4','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-progress','/tmp/ruby-cartaz-progress.txt',str(out)],check=True)
