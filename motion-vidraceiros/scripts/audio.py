"""Narração local Piper pt-BR + trilha instrumental original. Sem API paga."""
import json, subprocess, wave, os
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/audio'; RAW=OUT/'raw'; RAW.mkdir(parents=True,exist_ok=True)
MODEL=Path(os.environ.get('PIPER_MODEL',str(ROOT/'.cache/piper/pt_BR-faber-medium.onnx')))
PYTHON=ROOT/'.venv/bin/python'
scenes=[
(0,5,'Você, vidraceiro, sabia que pode estar deixando dinheiro na mesa?'),
(5,6,'Se você depende só de indicação, o que acontece quando as indicações param?'),
(11,9,'Que tal combinar indicação com anúncios? Em Pernambuco, tem gente procurando box, espelhos e fachadas.'),
(20,7,'Mas, se você não aparece, perde oportunidades de orçamento. Faça sua vidraçaria ser encontrada.'),
(27,7,'A i bê Mídias coloca seus serviços na frente de quem procura, com anúncios para sua região.'),
(34,8,'Por apenas seiscentos reais, tenha uma estratégia de anúncios para buscar novos contratos.'),
(42,9,'Pare de esperar a próxima indicação. Preencha o formulário e fale com a i bê Mídias. Sua vidraçaria merece ser vista.')]
rate=48000; voice=np.zeros(rate*51,dtype=np.float64); manifest=[]
for i,(start,slot,words) in enumerate(scenes):
 raw=RAW/f'{i+1}.wav'; text=RAW/f'{i+1}.txt';text.write_text(words,encoding='utf-8')
 scale=1.08
 subprocess.run([str(PYTHON),'-m','piper','--model',str(MODEL),'--input-file',str(text),'--output-file',str(raw),'--length-scale',str(scale),'--sentence-silence','0.18','--noise-scale','0.45','--noise-w-scale','0.55'],check=True,stdout=subprocess.DEVNULL)
 with wave.open(str(raw)) as w: dur=w.getnframes()/w.getframerate()
 # Conservar a fala inteira: acelerar apenas o necessário para caber na janela.
 available=slot-.48; tempo=1.0
 if dur>available: raise RuntimeError(f'Cena {i+1}: ajustar janela visual para fala natural de {dur:.2f}s.')
 if tempo>1.30: raise RuntimeError(f'Cena {i+1}: voz rápida demais ({tempo:.2f}), revisar o texto.')
 fitted=RAW/f'{i+1}-fit.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-af','afade=t=in:d=0.008','-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(fitted)],check=True)
 with wave.open(str(fitted)) as w: audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
 offset=round((start+.20)*rate);voice[offset:offset+len(audio)]+=audio
 manifest.append({'scene':i+1,'start':start+.20,'spoken_seconds':round(len(audio)/rate,3),'speed':round(tempo,3),'text':words})
 print(f'Cena {i+1}: {dur:.2f}s -> {len(audio)/rate:.2f}s / janela {slot}s',flush=True)
# Cama original: pad suave, arpejo discreto e pulsação de 100 BPM.
t=np.arange(rate*51)/rate; music=np.zeros_like(t)
chords=[(130.8128,164.8138,195.9977),(110.,130.8128,164.8138),(87.3071,110.,130.8128),(97.9989,123.4708,146.8324)]
for n in range(15):
 start=n*3.6; stop=min(51,start+4.1); ids=(t>=start)&(t<stop);u=t[ids]-start;env=np.minimum(1,u/.7)*np.minimum(1,(stop-start-u)/.8)
 for hz in chords[n%4]:music[ids]+=.023*env*(np.sin(2*np.pi*hz*u)+.15*np.sin(2*np.pi*2*hz*u))
for b in range(85):
 st=b*.6; ids=(t>=st)&(t<st+.45);u=t[ids]-st
 hz=chords[(b//6)%4][b%3]*2
 music[ids]+=.032*np.sin(2*np.pi*hz*u)*np.exp(-u*12)*np.minimum(1,u/.012)
# A cama baixa nas cenas de fala; transições recebem um sopro discreto.
music*=np.minimum(1,t/1.2)*np.minimum(1,(51-t)/1.7)
rng=np.random.default_rng(42)
for at in [5,11,20,27,34,42]:
 st=at-.16;ids=(t>=st)&(t<at+.12);u=t[ids]-st
 noise=rng.normal(0,.008,len(u));smooth=np.convolve(noise,np.ones(17)/17,mode='same');music[ids]+=smooth*np.sin(np.pi*u/.28)**2
mix=voice*.83+music
peak=np.max(np.abs(mix));mix*=min(1.,.86/max(peak,1e-8))
with wave.open(str(RAW/'mix-pre.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((mix*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(RAW/'mix-pre.wav'),'-af','loudnorm=I=-15:TP=-1.8:LRA=9','-ar',str(rate),'-ac','2','-c:a','pcm_s16le',str(OUT/'mix.wav')],check=True)
(OUT/'narracao.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
