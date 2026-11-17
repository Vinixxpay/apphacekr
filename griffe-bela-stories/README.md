# Griffe Bela — quatro anúncios em Stories

Produção em Remotion + React com as fotos e os dois áudios fornecidos pelo usuário. Grafia da marca confirmada: **Griffe Bela**. Saída 1080 × 1920, 30 fps, H.264 + AAC. Duas versões têm 17,07 segundos e duas 15,30 segundos; toda a fala dos áudios foi preservada.

## Direção

01 — Vitrine de festa: Natal, vinho e dourado, com o primeiro áudio.
02 — Várias combinações: composição clara em creme e champanhe, com o segundo áudio.
03 — Detalhes da coleção: direção editorial em vermelho/vinho, com o primeiro áudio e outras fotos.
04 — Do Natal à virada: sequência de Natal e Ano-Novo, com o segundo áudio.

A edição usa movimentos de câmera discretos nas fotos, composições de dois looks, aproximações de detalhes, transições suaves e cartelas finais com três fotos. As imagens originais são a base: não foram gerados novos corpos, rostos, roupas ou modelos. Não foram acrescentados preços, promoções, condições de compra ou promessa de resultado.

A voz original foi normalizada com filtragem suave, preservando velocidade e timbre. Somente pequenas margens sem fala no início/fim foram retiradas. Não houve substituição por TTS. A trilha instrumental e os efeitos foram compostos proceduralmente para esta edição e ficam abaixo da voz. As legendas foram alinhadas à gravação, com correções ortográficas e a grafia da marca confirmada pelo usuário.

O encerramento usa Peça o catálogo e Saiba mais. O destino do anúncio não foi informado; o botão real deve ser configurado para o canal escolhido pela marca. As versões permitem testar quatro direções visuais com as mensagens fornecidas.

## Renderizar

Requer Node 22+, FFmpeg e Chromium em `/usr/bin/chromium` (ajuste `scripts/render.mjs` se necessário).

```bash
npm ci
npm run typecheck
npm run stills
npm run render
```

As composições são `Story01` a `Story04` e `Cover01` a `Cover04`. Para uma seleção, use `node scripts/render.mjs video 1,2`. As saídas são escritas em `out/<slug>/`.

`campaign.json` contém a marca, as mensagens, as fotos de cada montagem e os tempos. `src/Film.tsx` contém as animações e o design; `public/captions.json` traz o alinhamento das legendas. As fontes Cormorant Garamond e Inter estão incluídas com suas licenças SIL OFL.

As fotos e gravações originais não foram publicadas separadamente no repositório. Para reproduzir a renderização, disponibilize os JPEGs selecionados em `public/photos/` com os números usados em campaign.json, e os áudios mixados em `public/audio/mix-1.wav` a `mix-4.wav`. Esses arquivos permanecem no workspace da edição; o pacote de entrega contém os vídeos finalizados, capas e legendas.

A preparação opcional de áudio e legendas está em `scripts/prepare.py` (Python, NumPy e FFmpeg), a trilha e mixagem em `scripts/mix.py`. Os arquivos de origem locais são os áudios 34.ogg e 35.ogg e as fotos numeradas do Drive. Não se devem reconstruir as falas a partir da transcrição: ela serve apenas ao alinhamento das legendas, e o áudio real continua sendo a fonte.

`scripts/verify.py` confere quadros, codecs, resolução, áudio incorporado, ausência de clipping, legendas e capas. `scripts/package.py` gera `GRIFFE_BELA_STORIES_PRONTOS/` e o ZIP de entrega, com uma página index.html reproduzível após a extração. Nenhum anúncio foi publicado automaticamente.
