# iB Mídias — quatro vídeos com gravações originais

## Revisão 2 — falas completas e mensagem real da cliente

A entrega atual está em `../entregas/ib-midias-revisado-*.mp4`. As quatro versões incluem a mensagem original completa da cliente (20,095 s de áudio decodificado), sem aceleração e sem música durante o relato. Não há transcrição inventada da mensagem.

1. **Completo — 81,8 s:** IMG_2203 inteiro; mensagem inserida aos 16,1 s, em uma pausa.
2. **Direto — 40,87 s:** IMG_2200 inteiro; mensagem inserida aos 10,3 s, em uma pausa.
3. **Apresentação — 45,5 s:** IMG_2197 inteiro, mensagem e IMG_2196 inteiro.
4. **Depoimento — 37,63 s:** mensagem e IMG_2196 inteiro.

O apresentador retorna após a mensagem nas quatro versões. As gravações usadas nesta revisão preservam todas as falas, sem remover trechos internos. A versão completa ficou mais longa para manter a explicação e o convite. O player acompanha a energia do áudio real. `review-delivery.json` documenta a cobertura dos originais, os pontos de inserção e a comparação do áudio final com a mensagem original, incluindo início e fim.

Para reproduzir a revisão, após preparar os proxies integrais em `work/IMG_*-proxy.mp4` e a trilha com os scripts abaixo, mantenha também o M4A da cliente em `input/videos vda/`:

```bash
.venv/bin/python scripts/source_matting.py
.venv/bin/python scripts/review_data.py
node scripts/review_render.mjs render
.venv/bin/python scripts/review_compose.py
.venv/bin/python scripts/review_assemble.py
```

Os MP4s revisados são gerados em `out/review/`. A composição final usa H.264, AAC, 1080 × 1920, 30 fps, BT.709 e faststart. O áudio original e os arquivos intermediários não são publicados separadamente.

Quatro anúncios verticais em 1080 × 1920, H.264/AAC, 30 fps. A edição usa a voz e a imagem originais do usuário, com recorte de fundo quadro a quadro, enquadramento guiado pelo rosto, legendas por trecho, diagramas em perspectiva, tipografia com profundidade, player visual sincronizado com a energia do áudio e trilha instrumental original discreta.

## Primeira entrega — histórico

1. **Troca de agência:** gancho sobre trocar de gestor, alinhamento de expectativas, funil e convite para preencher o formulário.
2. **Demanda qualificada:** empresário de qualquer ramo, demanda qualificada, processo comercial e proposta.
3. **Caso da cliente:** relato feito pelo apresentador sobre uma cliente que vendeu tudo; a edição não cria voz, depoimento ou resultado adicional.
4. **Proposta sob medida:** proposta para a operação do empresário e chamada para o formulário.

Na primeira entrega, o áudio de cliente ainda não estava disponível em arquivo separado. Os cortes aproveitam a fala do apresentador e não simulam depoimento. Os gráficos são ilustrativos e não exibem métricas inventadas. As frases de chamada respeitam o botão “Saiba Mais” e o formulário mencionados na gravação. Não foi inserido um novo preço na fala.

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
