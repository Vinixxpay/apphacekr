# iB Mídias — Vidraçarias de Pernambuco

Anúncio vertical 1080 × 1920, identidade azul/branco e logo oficial. A versão final tem aproximadamente 35,4 segundos, H.264, AAC e 60 fps. Inclui painéis de vidro em 3D CSS, reflexos, radar, fluxo anúncio/WhatsApp/orçamento e mapa de Pernambuco com pontos animados ilustrativos. Oferta: R$ 600, sem periodicidade ou composição da verba inventadas.

## Editar, assistir e exportar

Requer Node.js 22+, FFmpeg e Chromium em `/usr/bin/chromium` (ajuste o caminho em package.json se necessário).

```bash
npm ci
npm run dev
npm run typecheck
npm run render
node scripts/punch-export.mjs
```

O Remotion renderiza uma base de 51 segundos. A finalização corta os intervalos entre as falas usando `public/audio/narracao.json`, preserva 80 ms antes e 120 ms depois, aplica transições de 80 ms e acelera em 12% sem mudar o tom. Saída final: `out/ib-midias-vidraceiros-pernambuco.mp4`. `preview.html` reproduz esse arquivo. `node scripts/stills.mjs` gera sete capturas.

## Roteiro e áudio

A peça aborda a dependência de indicações, procura por box/espelhos/fachadas, visibilidade em Pernambuco, anúncios locais, conversas e orçamentos, oferta de R$ 600 e formulário. A fala acrescentada é: “Tem gente em Pernambuco procurando seus serviços. Mas, se sua vidraçaria não aparece, você perde oportunidades. Deixe de depender só de indicações.”

A narração masculina sintética pt-BR usa Piper Faber. Trilha instrumental original e voz prontas em `public/audio/mix.wav`. Para regenerar: `bash scripts/prepare-voice.sh`. Licença do modelo em `public/audio/VOICE-MODEL-CARD.txt`; fontes Inter e licença em public/.

O contorno do estado foi simplificado de uma malha geográfica. Fonte em `public/MAP-SOURCE.txt`, vetor em `src/pernambuco.ts`. Os pontos não representam contagem ou localização de clientes reais. Não há métricas inventadas nem garantia de fechamento.

Versões anteriores de MP4 permanecem em entregas/. `scripts/fast-export.mjs` também permite exportar a base acelerada com pausas; a entrega atual usa `punch-export.mjs`.
