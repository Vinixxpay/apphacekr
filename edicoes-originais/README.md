# iB Mídias — quatro vídeos com gravações originais

Quatro anúncios verticais em 1080 × 1920, H.264/AAC, 30 fps. A edição usa a voz e a imagem originais do usuário, com recorte de fundo quadro a quadro, enquadramento guiado pelo rosto, legendas por trecho, diagramas em perspectiva, tipografia com profundidade, player visual sincronizado com a energia do áudio e trilha instrumental original discreta.

## Versões

1. **Troca de agência:** gancho sobre trocar de gestor, alinhamento de expectativas, funil e convite para preencher o formulário.
2. **Demanda qualificada:** empresário de qualquer ramo, demanda qualificada, processo comercial e proposta.
3. **Caso da cliente:** relato feito pelo apresentador sobre uma cliente que vendeu tudo; a edição não cria voz, depoimento ou resultado adicional.
4. **Proposta sob medida:** proposta para a operação do empresário e chamada para o formulário.

O áudio de cliente mencionado em algumas gravações não veio em arquivo separado. Os cortes aproveitam a fala do apresentador e não simulam depoimento. Os gráficos são ilustrativos e não exibem métricas inventadas. As frases de chamada respeitam o botão “Saiba Mais” e o formulário mencionados na gravação. Não foi inserido um novo preço na fala.

## Reproduzir a edição

Requer Node.js 22+, FFmpeg/FFprobe, Chromium em `/usr/bin/chromium` e Python 3.12. Os originais e arquivos intermediários ficam ignorados em input/, work/, out/ e public/video/. Os quatro MOV fornecidos pelo usuário devem estar em `input/videos vda/`.

```bash
npm ci
uv venv .venv
UV_CACHE_DIR=/tmp/ib-uv-cache uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/transcribe.py
.venv/bin/python scripts/plan.py
.venv/bin/python scripts/prepare.py
.venv/bin/python scripts/music.py
.venv/bin/python scripts/data.py
npm run typecheck
npm run render
```

O modelo RVM deve estar em `work/rvm.onnx`: https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx . A inferência usa ONNX Runtime e não aplica substituição ou geração de rosto. O recorte é natural e pode manter pequenas variações nas bordas do cabelo e em movimentos rápidos. O modelo do primeiro teste PPHumanSeg não é usado na entrega final.

Para uma captura: `node scripts/render.mjs still Film01 90`. Para exportar apenas uma versão: `node scripts/render.mjs render Film01`. Os identificadores são Film01 a Film04. O bundler usa os PNGs dos personagens 3D gerados anteriormente no projeto da iB Mídias; esses personagens são ilustrativos. As fontes Inter e a licença estão em public/.

`plan.json` documenta os trechos exatos. `src/data.ts` contém os tempos e as legendas selecionadas. `scripts/data.py` corrige grafias óbvias do reconhecimento automático, como “Saiba Mais”. O player é parte da animação do vídeo, não um controle interativo. Sua forma de onda reage à energia da voz original; nenhum áudio foi acelerado ou clonado.

A trilha foi sintetizada para esta edição por `scripts/music.py` e pode ser usada nas quatro peças sem licença de música de terceiros. O render converte a saída do navegador para BT.709 de faixa limitada, aplica faststart e mantém os MP4s anteriores no repositório.
