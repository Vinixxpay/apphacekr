# iB Mídias — Vidraçarias de Pernambuco

Anúncio vertical 1080 × 1920, identidade azul/branco e logo oficial. A versão final tem aproximadamente 30,3 segundos, H.264, AAC e 60 fps. Inclui painéis de vidro em 3D CSS, reflexos, radar, fluxo anúncio/WhatsApp/orçamento e mapa de Pernambuco com pontos animados ilustrativos. Oferta: R$ 600, sem periodicidade ou composição da verba inventadas.

## Editar, assistir e exportar

Requer Node.js 22+, FFmpeg e Chromium em `/usr/bin/chromium` (ajuste o caminho em package.json se necessário).

```bash
npm ci
npm run dev
npm run typecheck
npm run render
node scripts/punch-export.mjs
```

O Remotion renderiza uma base de 51 segundos. A finalização corta os intervalos entre as falas usando `public/audio/narracao.json`, preserva 80 ms antes e 120 ms depois, aplica transições de 80 ms e acelera em 12% sem mudar o tom. Saída final: `out/ib-midias-vidraceiros-cinema.mp4`. `preview.html` reproduz esse arquivo. `node scripts/stills.mjs` gera sete capturas.

## Roteiro e áudio

A abertura pergunta: “Você, vidraceiro: sabia que pode estar deixando dinheiro na mesa?” A peça mostra o risco de depender só de indicação, propõe combinar indicação com anúncios, destaca procura em Pernambuco, visibilidade, orçamentos, oferta de R$ 600 e formulário. O roteiro completo está em public/audio/narracao.json.

A narração masculina sintética pt-BR usa Piper Faber. Trilha instrumental original e voz prontas em `public/audio/mix.wav`. Para regenerar: `bash scripts/prepare-voice.sh`. Licença do modelo em `public/audio/VOICE-MODEL-CARD.txt`; fontes Inter e licença em public/.

O contorno do estado foi simplificado de uma malha geográfica. Fonte em `public/MAP-SOURCE.txt`, vetor em `src/pernambuco.ts`. Os pontos não representam contagem ou localização de clientes reais. Não há métricas inventadas nem garantia de fechamento.

Versões anteriores de MP4 permanecem em entregas/. `scripts/fast-export.mjs` também permite exportar a base acelerada com pausas; a entrega atual usa `punch-export.mjs`.

## Personagens e direção 3D

Os três personagens, celulares, palcos e painéis foram modelados e renderizados em Blender/Cycles, com luz principal, recorte azul e preenchimento quente. Doze ângulos em public/characters/ são interpolados em React para dar movimento à câmera. Não são pessoas reais nem depoimentos. Para recriar os assets com Blender 4.3+: `blender -b -t 4 --python scripts/characters-3d.py`. O arquivo .blend é salvo em out/, junto aos renders ignorados. Os PNGs prontos dispensam Blender no render do Remotion.

Há gráfico animado de dois canais convergindo, conexões no mapa, moedas em perspectiva, feixes de luz e aproximações por cena.
