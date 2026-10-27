# iB Mídias — Anúncio para vidraçarias

Motion vertical de 42 segundos, 1080 × 1920, 30 fps. Identidade azul-marinho, azul e branco; logo oficial em apresentação monocromática. Painéis de vidro construídos em camadas 3D CSS, reflexos animados, perspectiva, tipografia cinética e fluxo gráfico de anúncio até orçamento. Os elementos são ilustrativos, sem métricas ou garantia de fechamento.

## Assistir e exportar

O ZIP inclui `out/ib-midias-motion.mp4` e `preview.html`. Abra o HTML para assistir sem instalar nada.

Para editar, use Node.js 22+, FFmpeg e Chromium:

```bash
npm ci
npm run dev
npm run typecheck
npm run render
```

O comando de render usa Chromium em `/usr/bin/chromium`; ajuste o caminho no package.json se necessário. A saída é H.264, YUV420p/BT.709, áudio AAC, 30 fps, com faststart. `node scripts/stills.mjs` captura as seis cenas.

## Roteiro

- 0–5s: Vidraceiro, serviço bom não pode depender só de indicação.
- 5–11s: Há procura local por box, espelhos e fachadas.
- 11–18s: iB Mídias apresenta anúncios direcionados para a região.
- 18–25s: Fluxo anúncio, WhatsApp e orçamento; negociação de novos contratos.
- 25–33s: Oferta de R$ 600 para uma estratégia de anúncios.
- 33–42s: Convite para preencher o formulário e falar com a iB Mídias.

O valor é exibido como R$ 600, sem acrescentar periodicidade nem condições comerciais não informadas.

## Narração

Voz masculina sintética pt-BR (Piper Faber), com ritmo ágil e preservação do tom. O áudio pronto está em `public/audio/mix.wav`, junto à trilha instrumental original. O texto e a duração de cada fala estão em `public/audio/narracao.json`. Licença do modelo em `public/audio/VOICE-MODEL-CARD.txt`.

Para regenerar a voz: `bash scripts/prepare-voice.sh`. A geração exige Python, uv e o modelo Piper; o render funciona com o áudio pronto sem baixar pesos. Não há dependência de serviço pago. Fontes Inter locais com licença em public/.

## Versão mais dinâmica

Após `npm run render`, execute `node scripts/fast-export.mjs`. A pós-produção acelera vídeo e áudio em 12%, preserva o tom da voz, aplica dissoluções de 180 ms entre as seis cenas e interpola os movimentos para 60 fps. A duração passa de 42 para aproximadamente 36,6 segundos. Saída: `out/ib-midias-vidraceiros-dinamico.mp4`. A oferta e a chamada final permanecem legíveis.
