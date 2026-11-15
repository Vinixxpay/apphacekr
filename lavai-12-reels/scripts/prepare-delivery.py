from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());tl=json.loads((r/'public/timings-aligned.json').read_text());dest=r.parent/'LAVAI_PRONTO_PARA_ANUNCIAR';dest.mkdir(exist_ok=True)
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
index=['# Lavaí — 12 vídeos para anúncios','', '**Destino:** anúncio → botão Saiba mais → primeira pergunta do quiz do Lavaí.','', '**QUIZ_URL:** `'+cfg['QUIZ_URL']+'`','', '**'+cfg['destinationStatus']+'**','', 'Os arquivos de vídeo estão finalizados. A ativação dos anúncios e a configuração do destino no Meta Ads ficam com o usuário. Não use a página de apresentação como substituta do quiz. Quando a URL publicada estiver disponível, teste no celular se a primeira tela é a primeira pergunta.','', 'Todos os vídeos incluem a fala final “Toque em Saiba mais e responda ao quiz do Lavaí.” e uma tela final de aproximadamente quatro segundos, com logo, convite ao quiz e Saiba mais. Não há preço de assinatura, oferta comercial ou link de checkout nos vídeos.','', 'As telas são demonstrações ilustradas, com cadastro e dados fictícios, baseadas no briefing fornecido. A página lavai.shop foi bloqueada pela política de rede nesta execução e não foi auditada. Valores de serviços, faturamento, ticket, ranking e pagamentos são exemplos, sem indicação de resultados reais ou lucro.','', '| Ordem | Tema / vídeo | Duração | Destino | Situação |','| --- | --- | --- | --- | --- |']
for v in cfg['videos']:
 t=next(t for t in tl if t['id']==v['id']);folder=dest/v['slug'];folder.mkdir(exist_ok=True);src=r/'out'/v['slug']
 for name in ['reel.mp4','capa.jpg']:
  if not (src/name).exists():raise FileNotFoundError(src/name)
  shutil.copy2(src/name,folder/name)
 text=f"TEXTO PRINCIPAL\n{v['primaryText']}\n\nTÍTULO\n{v['adTitle']}\n\nBOTÃO\nSaiba mais\n\nDESTINO\n{cfg['QUIZ_URL']}\n\nESTADO DO DESTINO\n{cfg['destinationStatus']}\n\nFluxo: anúncio → Saiba mais → primeira pergunta do quiz. O botão real e a URL são configurados no Meta Ads.\n"
 (folder/'anuncio.txt').write_text(text,encoding='utf-8')
 caps=json.loads((r/f'public/captions-{v["id"]:02d}.json').read_text());srt=[]
 for n,c in enumerate(caps,1):srt.append(f"{n}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{' '.join(w['text'] for w in c['words'])}\n")
 (folder/'legendas.srt').write_text('\n'.join(srt),encoding='utf-8')
 index.append(f"| {v['id']:02d} | [{v['title']}]({v['slug']}/reel.mp4) | {t['duration']:.2f} s | QUIZ_URL | Vídeo conferido; URL do quiz pendente |")
index+=['','## Arquivos','', 'Cada pasta contém reel.mp4 (1080×1920, H.264, 30 fps, AAC), capa.jpg (1080×1920), legendas.srt e anuncio.txt. O vídeo já contém as legendas incorporadas. O SRT é uma alternativa editável.','', 'Depois de extrair o pacote, abra index.html para assistir aos 12 Reels e acessar os arquivos de cada anúncio. As vozes são sintéticas em português brasileiro, com trilha e efeitos originais. Nenhum anúncio foi publicado automaticamente.']
(dest/'INDICE.md').write_text('\n'.join(index)+'\n',encoding='utf-8');print(dest)
