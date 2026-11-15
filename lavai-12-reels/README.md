# Lavaí — campanha de 12 Reels para Meta Ads

Doze anúncios independentes em Remotion + React + SVG, com narração masculina sintética em português brasileiro, legendas incorporadas, ilustrações originais e trilha/efeitos originais. Saída vertical 1080 × 1920, 30 fps, H.264 + AAC.

## Abrir e renderizar

Requer Node 22+, FFmpeg e Chromium. O renderizador usa `/usr/bin/chromium`; ajuste `scripts/render.mjs` se necessário.

```bash
npm ci
npm run dev
npm run typecheck
npm run stills
npm run render
```

As composições são `Reel01` a `Reel12` e `Cover01` a `Cover12`. Para exportar uma seleção: `node scripts/render.mjs video 1,2,3`. Arquivos existentes são preservados; use `FORCE=1` para refazer. Áudios e fontes estão incluídos: não é necessário gerar voz novamente para renderizar.

## Roteiros, destino e oferta

`campaign.json` contém os 12 roteiros, textos principais para o Meta Ads, títulos, capas e `QUIZ_URL`. O destino permanece `QUIZ_URL` até ser informada a URL publicada. A URL não aparece dentro dos vídeos. O usuário deve configurar o botão real Saiba mais no Meta Ads e verificar no celular se o endereço abre na primeira pergunta do quiz.

Todos os anúncios terminam com a fala “Toque em Saiba mais e responda ao quiz do Lavaí.” e uma tela final de cerca de quatro segundos. Não há preço de assinatura, checkout, oferta, diagnóstico personalizado prometido ou nota do quiz. Os valores exibidos em demonstrações de lavagem, adicionais, comprovantes e relatórios são fictícios, conforme permitido no briefing.

A página https://lavai.shop/ foi bloqueada pela política de rede e não pôde ser auditada. As funções mostradas vêm exclusivamente do novo briefing fornecido: cadastro de cliente/veículo/serviço, adicionais por sujeira, tabela de valores, comprovantes com marca e compartilhamento em imagem/PDF, histórico por placa ou telefone, faturamento e ticket médio, ranking de serviços, registros por pagamento e dados separados por estabelecimento. As telas são **ilustrações de demonstração**, e não capturas do produto. Não são exibidos dados reais, conciliação bancária, acesso simultâneo de funcionários, consolidação de unidades ou troca instantânea de conta.

## Design e estrutura

- Amarelo #FFB800, azul-escuro #0F172A, apoio #1E293B e branco #F8FAFC.
- Títulos Poppins Bold; textos Inter SemiBold. Fontes incluídas com licença SIL OFL.
- Logo Lavaí preparada a partir da imagem fornecida anteriormente, exibida inteira com proporções preservadas.
- Margens essenciais de 120 px nas laterais, 220 px no topo e 340 px no rodapé.
- `src/Art.tsx`: personagens, carros, moto, SUV, balcão, recibos e telas ilustradas.
- `src/Scenes.tsx`: 12 sequências próprias de cenas, perguntas e demonstrações.
- `src/Film.tsx`: montagem, títulos, legendas, transições e tela final.
- `public/timings-aligned.json`: duração, movimento de boca e tempos de cenas.
- `public/captions-*.json` e `words-*.json`: fala canônica e tempos.
- `public/audio/01` a `12`: fala, voz, trilha, efeitos e mixagem final.

As referências da Dorami orientaram o ritmo e os recursos de edição. Nenhum trecho de vídeo, áudio, personagem ou marca da Dorami foi incluído.

## Narração e conferência

A voz é sintética, Kokoro `pm_santa` em português brasileiro, sem clonagem. A velocidade nativa é ajustada ao intervalo de duração de cada roteiro, sem alongar uma gravação pronta. A chamada final é gerada separadamente, com a mesma voz e cadência, e sincronizada à tela final. Os quizzes 03 e 09 contêm os dois segundos de pausa pedidos. Há pequenas pausas de leitura nos vídeos 04, 08 e 12 para acompanhar as demonstrações e perguntas.

Para regeneração opcional, instale `requirements-voice.txt`, disponibilize `kokoro.onnx` e `voices.bin` em `work/models/` e execute `scripts/audio.py`, `scripts/align.py` e `scripts/mix.py`. A regeneração invalida os tempos anteriores; após mudar falas, gere todos os tempos e legendas novamente. O alinhamento é feito com Whisper e o roteiro canônico; `speech-review.json` registra a grafia reconhecida pelo modelo, que pode diferir de nomes e contrações da escrita original.

`scripts/verify.py` confere resolução, codec, quadros, decodificação integral, áudio, legendas, capas, pausas, duração e CTA. `verification.json` registra o resultado.

## Entrega para publicação manual

Após renderizar e verificar:

```bash
python3 scripts/prepare-delivery.py
python3 scripts/package.py
```

A pasta `LAVAI_PRONTO_PARA_ANUNCIAR/`, ao lado do projeto, contém `reel.mp4`, `capa.jpg`, `legendas.srt` e `anuncio.txt` para cada Reel, além do índice com a pendência da URL. O ZIP inclui `index.html`: extraia e abra no navegador para assistir aos 12 vídeos. A publicação e a configuração dos anúncios permanecem com o usuário.
