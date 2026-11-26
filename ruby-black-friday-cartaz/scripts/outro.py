from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1];root=r.parent
u='min(on/54,1)';ease=f'pow({u},2)*(3-2*{u})';zoom=f'1+2.2*({ease})+0.03*min(max((on-54)/66,0),1)'
f=[]
f.append('[0:v]trim=duration=4,setpts=PTS-STARTPTS,scale=3240:5760:flags=lanczos,fade=t=out:st=0.5:d=1:color=0x211421[bg]')
f.append('[1:v]scale=984:1434:flags=lanczos,format=rgba,trim=duration=4,setpts=PTS-STARTPTS,fade=t=in:st=0.25:d=0.4:alpha=1[art]')
f.append('[bg][art]overlay=x=1065:y=1368:shortest=1[scene]')
f.append(f"[scene]zoompan=z='{zoom}':x='max(0,1620-63*({ease})-iw/(2*zoom))':y='max(0,2880-795*({ease})-ih/(2*zoom))':d=1:s=1080x1920:fps=30,format=yuv420p[v]")
(r/'outro-filter.txt').write_text(';\n'.join(f))
subprocess.run(['ffmpeg','-hide_banner','-y','-filter_complex_threads','1','-loop','1','-framerate','30','-i',str(root/'ruby-black-friday-reels/public/placa-original.jpg'),'-loop','1','-framerate','30','-i',str(r/'public/cartaz-recriado.png'),'-filter_complex_script',str(r/'outro-filter.txt'),'-map','[v]','-frames:v','120','-c:v','libx264','-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-an',str(r/'public/outro-cartaz.mp4')],check=True)
