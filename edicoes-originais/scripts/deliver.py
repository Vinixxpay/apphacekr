from pathlib import Path
import json,subprocess,shutil
root=Path(__file__).resolve().parents[1];dest=root.parent/'entregas'
films=json.loads((root/'work/prepared.json').read_text())
names=['ib-midias-01-troca-de-agencia.mp4','ib-midias-02-demanda-qualificada.mp4','ib-midias-03-caso-da-cliente.mp4','ib-midias-04-proposta-sob-medida.mp4']
manifest=[]
for film,name in zip(films,names):
 p=root/'out'/f"{film['id']}.mp4"
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
 expected=json.loads((root/'work'/f"{film['id']}-frames.json").read_text())['frames']
 assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v['pix_fmt'],int(v['nb_frames']))==('h264',1080,1920,'30/1','yuv420p',expected),(film['id'],v)
 assert a['codec_name']=='aac';assert abs(float(data['format']['duration'])-expected/30)<.12
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 shutil.copy2(p,dest/name)
 manifest.append({'video':name,'seconds':float(data['format']['duration']),'size':int(data['format']['size']),'frames':expected})
 print(name,data['format']['duration'],'s',flush=True)
frames=[16,5,9,9]
for film,t in zip(films,frames):
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(root/'out'/f"{film['id']}.mp4"),'-frames:v','1','-vf','scale=270:480',str(root/'out'/f"{film['id']}-poster.jpg")],check=True)
args=['ffmpeg','-v','error','-y']
for film in films:args+=['-i',str(root/'out'/f"{film['id']}-poster.jpg")]
args+=['-filter_complex','[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|270_0|0_480|270_480[v]','-map','[v]','-frames:v','1',str(dest/'ib-midias-quatro-videos-previa.jpg')]
subprocess.run(args,check=True)
(root/'delivery.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Quatro MP4s e prévia validados.')
