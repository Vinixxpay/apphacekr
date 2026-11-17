from pathlib import Path
import json,shutil,zipfile,html
r=Path(__file__).resolve().parents[1];cfg=json.loads((r/'campaign.json').read_text());tl=json.loads((r/'public/timings-aligned.json').read_text());caps=json.loads((r/'public/captions.json').read_text());report=json.loads((r/'verification.json').read_text());assert len(report)==2 and all(v['status']=='passed' for v in report)
dest=r.parent/'entregas'/'ib-black-friday-v2';dest.mkdir(parents=True,exist_ok=True)
def stamp(t):
 m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
index=['# iB Mídias — Black Friday','', 'Dois anúncios verticais em motion graphics, com voz masculina em português brasileiro, trilha eletrônica e efeitos originais. MP4 H.264 + AAC, 1080 × 1920, 30 fps, cerca de 28,5 s cada.','', '| Vídeo | Duração | Preço legível | CTA visível |','| --- | --- | --- | --- |'];cards=[]
for v in cfg['videos']:
 name=v['name'];rv=next(x for x in report if x['id']==v['id']);shutil.copy2(r/f'out/{name}.mp4',dest/f'{name}.mp4');shutil.copy2(r/f'out/capa-{v["id"]}.jpg',dest/f'{name}.jpg')
 srt=[]
 for j,c in enumerate(caps[str(v['id'])],1):srt.append(f"{j}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{' '.join(w['text'] for w in c['words'])}\n")
 (dest/f'{name}.srt').write_text('\n'.join(srt),encoding='utf-8');index.append(f"| [{v['title']}]({name}.mp4) | {rv['duration']:.2f} s | {rv['price_visible_seconds']:.2f} s | {rv['cta_visible_seconds']:.2f} s |")
 cards.append(f'<article><h2>{html.escape(v["title"])}</h2><video controls playsinline preload="none" src="{name}.mp4" poster="{name}.jpg"></video><nav><a download href="{name}.mp4">Baixar MP4</a><a download href="{name}.jpg">Capa</a><a download href="{name}.srt">SRT</a></nav></article>')
index+=['','A oferta apresentada é **gestão dos anúncios por R$ 650**, com **verba de anúncios à parte**. O prazo **de até 24 horas** se refere aos primeiros anúncios no ar. Não há contagem regressiva de encerramento da promoção, métricas inventadas ou promessa de vendas.','', 'As legendas já estão incorporadas ao MP4 e também estão disponíveis como SRT. A logo oficial branca foi usada. A voz é sintética em PT-BR, com a marca pronunciada como i bê Mídias.','', 'A pergunta está visível no primeiro quadro. Preço, prazo e CTA podem ser compreendidos sem som. O botão fica estável; somente a seta pulsa.','', 'Extraia o ZIP e abra index.html para assistir aos dois vídeos. Configure o destino real de Saiba Mais no gerenciador de anúncios. Nenhum anúncio foi publicado automaticamente.']
(dest/'LEIA-ME.md').write_text('\n'.join(index)+'\n',encoding='utf-8');shutil.copy2(r/'verification.json',dest/'verificacao.json')
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>iB Mídias · Black Friday</title><style>*{box-sizing:border-box}body{margin:0;background:#10141c;color:white;font:16px system-ui,sans-serif}header{padding:36px 24px;background:#0131cd;text-align:center}h1{margin:0 0 12px;font-size:34px}header p{margin:0;line-height:1.5}main{max-width:1000px;margin:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;padding:30px 24px}article{background:#182132;border:1px solid #31496b;border-radius:16px;padding:18px}h2{font-size:22px;min-height:60px;margin:0 0 16px;line-height:1.4}video{display:block;width:100%;aspect-ratio:9/16;background:black;border-radius:10px}nav{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}a{background:#b9fc01;color:#10141c;padding:12px 16px;border-radius:7px;text-decoration:none;font-weight:700}</style><header><h1>iB Mídias · Black Friday</h1><p>Gestão por R$ 650 · Primeiros anúncios no ar em até 24h</p></header><main>'''+''.join(cards)+'''</main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})))</script></html>'''
(dest/'index.html').write_text(page,encoding='utf-8');z=dest/'IB_Midias_Black_Friday_Pacote.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in sorted(dest.iterdir()):
  if p.is_file() and p.suffix.lower()!='.zip':out.write(p,Path('IB_MIDIAS_BLACK_FRIDAY')/p.name)
with zipfile.ZipFile(z) as f:assert f.testzip() is None
srczip=dest/'IB_Midias_Black_Friday_Projeto_Editavel.zip'
with zipfile.ZipFile(srczip,'w',zipfile.ZIP_DEFLATED) as out:
 for p in sorted(r.rglob('*')):
  if p.is_file() and not any(s in p.relative_to(r).parts for s in ['node_modules','work','out','__pycache__']):out.write(p,Path(r.name)/p.relative_to(r))
with zipfile.ZipFile(srczip) as f:assert f.testzip() is None
print('PACKAGE',z,z.stat().st_size,flush=True);print('SOURCE',srczip,srczip.stat().st_size,flush=True)
