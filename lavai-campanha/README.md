# Lavaí — três anúncios em motion design 2D

Três filmes independentes, com protagonistas e aberturas diferentes, narração masculina sintética em português brasileiro, animação SVG/React, trilha instrumental e efeitos sincronizados. Formato 1080 × 1920, 30 fps, MP4 H.264 + AAC.

| Filme | Duração | Gancho |
| --- | --- | --- |
| video_01_lavai.mp4 | 30,5 s | Quanto você realmente faturou? |
| video_02_lavai.mp4 | 31,3 s | Ainda usa papel e calculadora? |
| video_03_lavai.mp4 | 34,0 s | Dono ou refém do negócio? |

## Abrir e exportar

Requer Node 22+, FFmpeg e Chromium. O renderizador usa `/usr/bin/chromium`; ajuste `browserExecutable` em `scripts/render.mjs` se necessário.

```bash
npm ci
npm run dev
npm run typecheck
npm run render:1
npm run render:2
npm run render:3
```

Os vídeos são escritos em `out/`. As composições são `Video01Lavai`, `Video02Lavai` e `Video03Lavai`. Todos os áudios, a fonte e a logo estão incluídos: não é necessário gerar a voz novamente para renderizar.

## Personalização

`campaign.json` reúne preço, período de cobrança, CTA, cores e roteiros. Alterações apenas visuais de preço/CTA são aplicadas no render; mudanças na fala exigem regenerar a narração e recalcular a sincronização. `src/Actors.tsx` contém os personagens, `src/Art.tsx` as ilustrações e interfaces, e `src/Film.tsx` as três montagens. `timings.json` e `public/captions-*.json` guardam os tempos alinhados à fala.

A identidade usa #FFB300, #071321 e branco. A logo foi preparada em PNG a partir da imagem enviada na conversa; é exibida inteira, com proporções preservadas. A fonte Montserrat ExtraBold e sua licença estão em `public/fonts/`.

## Áudio e fidelidade ao produto

A voz é sintética, Kokoro `pm_santa` em português brasileiro, sem clonagem. Os arquivos separados de fala, trilha e efeitos e a mixagem final estão em `public/audio/v1`, `v2` e `v3`. `scripts/audio.py`, `align.py` e `mix.py` documentam a geração e sincronização; dependem de Kokoro ONNX, seus modelos locais, faster-whisper, NumPy, SoundFile e FFmpeg.

As telas são ilustrativas e exibem cadastro de clientes, registro de serviços, recibos PDF/PNG e compartilhamento pelo WhatsApp. Não há promessa de aumento garantido de faturamento. O teste gratuito não é anunciado, pois sua disponibilidade não foi confirmada. No roteiro 2, “cadastrar cada veículo” foi ajustado para “cadastrar cada cliente”, conforme as funções confirmadas no briefing.

`briefing.md` preserva o pedido original; `speech-review.json` documenta o alinhamento da narração. `verification.json`, quando presente, registra as verificações dos MP4s finais.
