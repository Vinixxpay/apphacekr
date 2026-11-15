from pathlib import Path
import json,html,zipfile,shutil,hashlib
r=Path(__file__).resolve().parents[1];dest=r.parent/'IB_MIDIAS_PRONTO_PARA_POSTAR';release=r.parent/'entregas'/'ib-midias-12-reels';release.mkdir(parents=True,exist_ok=True)
cfg=json.loads((r/'campaign.json').read_text());reports=json.loads((r/'verification.json').read_text());assert len(reports)==12 and all(v['status']=='passed' for v in reports)
shutil.copy2(r/'verification.json',dest/'verificacao.json')
cards=[]
for v in cfg['videos']:
 folder=dest/v['slug'];assert {p.name for p in folder.iterdir()}=={'reel.mp4','capa.jpg','legenda.txt','legendas.srt'}
 for name in ['reel.mp4','capa.jpg','legenda.txt','legendas.srt']:assert (folder/name).stat().st_size>0
 rv=next(t for t in reports if t['id']==v['id']);slug=v['slug'];esc=html.escape
 cards.append(f'''<article><h2>{v['id']:02d} · {esc(v['title'])}</h2><video controls playsinline preload="none" poster="{slug}/capa.jpg" src="{slug}/reel.mp4"></video><p>{rv['duration_seconds']:.1f}s · {esc(v['cta'])}</p><nav><a download href="{slug}/reel.mp4">MP4</a><a download href="{slug}/capa.jpg">Capa</a><a download href="{slug}/legenda.txt">Texto do post</a><a download href="{slug}/legendas.srt">SRT</a></nav></article>''')
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>12 Reels · iB Mídias</title><style>*{box-sizing:border-box}body{margin:0;background:#edf1ff;color:#071643;font:16px system-ui,sans-serif}header{padding:40px max(24px,calc((100vw - 1200px)/2));background:#0131cd;color:white}h1{margin:0 0 14px;font-size:36px}header p{max-width:800px;line-height:1.6;margin:0}main{max-width:1248px;margin:auto;padding:30px 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}article{background:white;border-radius:20px;padding:18px;box-shadow:0 8px 28px #0131cd12}h2{font-size:20px;line-height:1.35;min-height:54px;margin:0 0 16px}video{width:100%;aspect-ratio:9/16;border-radius:12px;background:#0131cd;display:block}article p{line-height:1.5;font-size:14px}nav{display:flex;flex-wrap:wrap;gap:10px}a{color:#0131cd;background:#b9fc01;border-radius:8px;padding:10px 13px;text-decoration:none;font-weight:700;font-size:14px}</style><header><h1>iB Mídias · 12 Reels</h1><p>Vídeos, capas e textos para publicação manual. Escolha um vídeo para assistir e use os links para baixar os arquivos. Para os CTAs de WhatsApp, mantenha o contato disponível no link da bio.</p></header><main>'''+''.join(cards)+'''</main><script>document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()})))</script></html>'''
(dest/'index.html').write_text(page,encoding='utf-8')
manifest={str(p.relative_to(dest)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(dest.rglob('*')) if p.is_file()};(dest/'ARQUIVOS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
z=release/'IB_MIDIAS_12_REELS_PRONTOS.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in sorted(dest.rglob('*')):
  if p.is_file():out.write(p,Path(dest.name)/p.relative_to(dest))
with zipfile.ZipFile(z) as f:assert f.testzip() is None
z2=release/'ib-midias-12-reels-editavel.zip'
with zipfile.ZipFile(z2,'w',zipfile.ZIP_DEFLATED) as out:
 for p in sorted(r.rglob('*')):
  if p.is_file() and not any(q in p.relative_to(r).parts for q in ['node_modules','work','out','.venv','__pycache__']):out.write(p,Path(r.name)/p.relative_to(r))
with zipfile.ZipFile(z2) as f:assert f.testzip() is None
print('POST PACKAGE',z,z.stat().st_size,flush=True);print('EDITABLE PACKAGE',z2,z2.stat().st_size,flush=True)
