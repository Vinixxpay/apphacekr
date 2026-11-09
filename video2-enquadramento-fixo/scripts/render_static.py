from pathlib import Path
import json,subprocess,os
r=Path(__file__).resolve().parents[1];repo=r.parent;plan=json.loads((r/'edit-plan.json').read_text());src=Path(os.environ.get('STATIC_SOURCE',repo/'vidracarias-sticker-video2/work/source.mkv'));parts=plan['parts'];f=['[0:v]split=3[s0][s1][s2]']
for i,p in enumerate(parts):f.append(f"[s{i}]trim=start_frame={round(p['start']*30)}:end_frame={round(p['end']*30)},setpts=PTS-STARTPTS[v{i}]")
f.append('[v0][v1][v2]concat=n=3:v=1:a=0,crop=984:944:0:520,scale=1080:1036:flags=lanczos,setsar=1[v]')
cmd=['ffmpeg','-v','warning','-y','-threads','3','-i',str(src),'-filter_complex_threads','2','-filter_complex',';'.join(f),'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','3','-pix_fmt','yuv420p','-r','30','-frames:v',str(plan['frames']),'-movflags','+faststart','-progress',str(r/'work/presenter-progress.txt'),'-nostats',str(r/'work/presenter-static.mp4')]
(r/'static-framing.json').write_text(json.dumps({'reference':'ib-midias-vidracarias-video2.mp4 — original 1min22s version','frames':plan['frames'],'fps':30,'crop':{'x':0,'y':520,'width':984,'height':944},'sourceDimensions':[1080,1920],'panelDimensions':[1080,1036],'tracking':False,'animatedZoom':False,'scale':'Fixed for every frame and every cut','parts':parts},ensure_ascii=False,indent=2));subprocess.run(cmd,check=True);print('STATIC PRESENTER READY',flush=True)
