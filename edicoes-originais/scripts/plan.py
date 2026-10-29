from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
def seg(file,a,b,theme,caption):return dict(file=file,start=a,end=b,theme=theme,caption=caption)
plans=[
 dict(id='01-gestor',name='Pare de trocar de agência',segments=[seg('IMG_2203',2.30,8.35,'swap','De gestor em gestor?'),seg('IMG_2203',25.75,33.15,'expectation','Expectativas alinhadas.'),seg('IMG_2203',33.40,41.90,'funnel','Melhore seu funil de vendas.'),seg('IMG_2203',50,54.35,'proposal','Uma proposta só para você.'),seg('IMG_2203',54.60,58.85,'cta','Saiba Mais • Preencha o formulário')]),
 dict(id='02-demanda',name='Demanda qualificada',segments=[seg('IMG_2197',.35,3.20,'people','Para empresários de qualquer ramo.'),seg('IMG_2203',8.78,13.25,'demand','Demanda qualificada.'),seg('IMG_2203',32.12,41.90,'funnel','Alinhamento e processo comercial.'),seg('IMG_2203',50,54.35,'proposal','Uma proposta só para você.'),seg('IMG_2203',54.60,58.85,'cta','Agende uma conversa.')]),
 dict(id='03-cliente',name='O caso da cliente',segments=[seg('IMG_2200',.25,6.98,'swap','Cansado de trocar de gestor?'),seg('IMG_2200',11.95,15.25,'sold','Ela vendeu tudo.'),seg('IMG_2200',15.59,19.85,'cta','Fale direto comigo no Saiba Mais.')]),
 dict(id='04-proposta',name='Uma proposta sob medida',segments=[seg('IMG_2196',10.55,14.42,'people','Você é empresário?'),seg('IMG_2203',33.40,35.70,'funnel','Melhore o funil de vendas.'),seg('IMG_2203',50,54.35,'proposal','Uma proposta idealizada para você.'),seg('IMG_2196',7.72,10.40,'cta','Preencha o formulário.')])]
for plan in plans:
 t=0
 for s in plan['segments']:
  s['from']=round(t,4);s['duration']=round(s['end']-s['start'],4);t+=s['duration']
 plan['speechDuration']=round(t,4);plan['duration']=round(t+.7,4)
(root/'plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2))
print([(p['id'],p['duration']) for p in plans])
