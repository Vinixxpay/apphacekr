from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());tl=json.loads((r/'public/timings-aligned.json').read_text());dest=r.parent/'IB_MIDIAS_PRONTO_PARA_POSTAR';dest.mkdir(exist_ok=True)
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
index=['# iB Mídias — 12 Reels prontos para postar','', 'Vídeos orgânicos para vidraçarias, esquadrias e portões de alumínio. Produção em motion design 2D com voz masculina sintética em português brasileiro, legendas incorporadas e trilha/efeitos originais. Nenhuma publicação automática foi feita.','', 'As durações abaixo seguem a fala integral e incluem pelo menos 3 segundos de tela final após a narração. Os tempos aproximados do briefing foram ajustados à voz para evitar pausas longas sem fala. Nos quizzes 03 e 10, há uma pausa de 2 segundos antes da resposta.','', '| Ordem | Tema / vídeo | Duração | CTA | Situação |','| --- | --- | --- | --- | --- |']
for v in cfg['videos']:
 t=next(t for t in tl if t['id']==v['id']);folder=dest/v['slug'];folder.mkdir(exist_ok=True);src=r/'out'/v['slug']
 for name in ['reel.mp4','capa.jpg']:
  if not (src/name).exists():raise FileNotFoundError(src/name)
  shutil.copy2(src/name,folder/name)
 (folder/'legenda.txt').write_text(v['post']+'\n',encoding='utf-8')
 caps=json.loads((r/f'public/captions-{v["id"]:02d}.json').read_text());srt=[]
 for n,c in enumerate(caps,1):srt.append(f"{n}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{' '.join(w['text'] for w in c['words'])}\n")
 (folder/'legendas.srt').write_text('\n'.join(srt),encoding='utf-8')
 index.append(f"| {v['id']:02d} | [{v['title']}]({v['slug']}/reel.mp4) | {t['duration']:.2f} s | {v['cta']} | Pronto — com narração e legendas |")
index+=['','## Oferta e uso','', 'Nos vídeos 01, 04, 05 e 06, a tela final informa **Gestão por R$ 650/mês** e **Verba de anúncios à parte**. O CTA usa o WhatsApp pelo link da bio. Os demais vídeos usam salvar, comentar ou enviar mensagem com a palavra-chave indicada. Configure o link da bio para o WhatsApp antes de postar.','', 'Os diálogos estão identificados como Simulação. Ilustrações e cenários são próprios da iB Mídias. As referências da Dorami foram usadas para linguagem de montagem; não foram incorporadas aos arquivos finais. Não foram inventados resultados, depoimentos ou garantias de venda.','', 'Cada pasta contém reel.mp4, capa.jpg, legenda.txt e legendas.srt. Os MP4s têm 1080 × 1920, H.264, 30 fps e áudio AAC. O arquivo SRT serve como alternativa editável; as legendas já estão incorporadas ao vídeo.']
(dest/'INDICE.md').write_text('\n'.join(index)+'\n',encoding='utf-8');print(dest)
