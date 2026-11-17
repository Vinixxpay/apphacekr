# iB Mídias — revisão de voz e animações (v2)

Dois comerciais em motion graphics, com perguntas diretas, narração masculina sintética em português brasileiro, trilha eletrônica original crescente, impactos, legendas e texto animado. Exportação 1080 × 1920, 30 fps, MP4 H.264 + AAC. Duração: cerca de 28,5 segundos por vídeo.

## Arquivos finais

- IB_Midias_Black_Friday_Pagou_Caro.mp4
- IB_Midias_Black_Friday_Orcamento.mp4

A primeira pergunta está presente no quadro zero. O preço R$ 650 fica no centro por mais de dois segundos. O arco acelera e congela no início da palavra “vinte”, na frase “vinte e quatro horas”, com 24H em verde-lima. O botão Saiba Mais permanece estável até o fim; somente a seta pulsa discretamente. A última tela reapresenta gestão por R$ 650 e primeiros anúncios no ar em até 24h, de modo legível sem áudio. Não há contagem regressiva de encerramento da promoção.

A oferta é o valor da gestão, sem periodicidade acrescentada. A linha “Verba de anúncios à parte” conserva a condição usada no briefing anterior da iB Mídias, esclarecendo a separação entre gestão e mídia. O prazo de 24 horas refere-se à entrada dos primeiros anúncios no ar, e não a vendas ou resultados. Não há métricas inventadas; relatórios e orçamentos são ilustrações originais sem valores fictícios.

Não foram encontradas artes estáticas específicas de Black Friday no workspace. A direção foi criada com azul #0131CD, branco, verde-lima #B9FC01 e grafite. Foi usada a logo oficial branca já disponível. A tipografia é Barlow Condensed ExtraBold, com Inter para textos auxiliares; fontes e licenças estão incluídas.

## Voz e som

Voz sintética masculina Kokoro `pm_alex`, em PT-BR, sem clonagem. A marca foi escrita foneticamente como “i bê Mídias” na geração da voz; a legenda preserva “iB Mídias”. As velocidades nativas variam entre blocos para dar energia à apresentação da Black Friday e articulação ao preço e ao prazo. Não houve alteração de pitch em uma gravação pronta.

A narração completa e os tempos constam em `campaign.json` e `public/timings-aligned.json`. Os cinco blocos gravados de cada vídeo estão em `public/audio/1` e `2`, com voz completa, trilha, efeitos e mixagem separados. A pausa antes do preço e sua permanência em tela são intencionais. `speech-review.json` registra o alinhamento automático com o roteiro canônico; grafias reconhecidas pelo ASR podem divergir de contrações e nomes sem substituir o texto aprovado.

A trilha e os efeitos foram sintetizados originalmente para a campanha. O impacto do valor coincide com a entrada visual do preço, 0,2s antes de ser falado, durante a pausa. O som do relógio e seu arco param no cue de “vinte”. A voz fica em primeiro plano.

## Renderização

Requer Node 22+, FFmpeg e Chromium em `/usr/bin/chromium` (ajuste em scripts/render.mjs).

```bash
npm ci
npm run typecheck
npm run stills
npm run render
```

As composições são `BlackFriday01`, `BlackFriday02`, `Cover01` e `Cover02`. Para exportar um só: `node scripts/render.mjs video 1`. Os arquivos saem em `out/`. Os áudios já estão incluídos; não é necessário gerar voz para renderizar novamente.

`src/Art.tsx` reúne as cenas, o relógio, preço e CTA; `src/Film.tsx` monta os cortes a partir dos tempos. `src/Person.tsx` contém a ilustração original do empresário. `scripts/audio.py`, `align.py` e `mix.py` documentam geração e sincronização. Para regeneração opcional, são necessários os pacotes de requirements-voice.txt e os modelos Kokoro ONNX/voices.bin em work/models; esses pesos não estão incluídos.

`scripts/verify.py` verifica codecs, quadros, áudio integral sem clipping, texto completo das legendas, preço por pelo menos dois segundos, CTA por pelo menos três e o cue do relógio. A revisão visual usa quadros do gancho, preço, relógio e encerramento de cada vídeo. Nenhum anúncio foi publicado automaticamente.

## Revisão solicitada

Esta versão preserva a oferta e os roteiros, troca o timbre por outra voz masculina brasileira e controla os fonemas de Instagram e Black Friday. A preparação fonética usa “Instagrã” para tonicidade e nasalização finais e “Blék Fráidei” para a leitura correta de Friday. A fala é sintetizada diretamente a partir desses fonemas, sem alteração de pitch nem alongamento posterior. As grafias normais permanecem em todos os textos e legendas. O nome da agência continua sendo pronunciado i bê Mídias.

Foram acrescentados: balão de dúvida no celular; folhas de relatório em camadas; máscara de revelação da Black Friday; nova entrada escalonada das plataformas; halo e moldura de impacto no preço; pontos orbitais e confirmação no relógio; linha de assinatura e brilho de borda no CTA. O arco completa três voltas antes de parar, mantendo continuidade de posição na parada. O botão permanece estável.

As versões anteriores e seus arquivos de entrega são preservados. Os novos exports ficam em entregas/ib-black-friday-v2 para que o download use um endereço novo e não reapresente áudio antigo em cache.
