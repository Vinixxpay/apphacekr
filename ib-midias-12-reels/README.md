# iB Mídias — campanha de 12 Reels

Doze composições independentes em Remotion + React + SVG, com roteiros integrais do briefing, narração masculina sintética em PT-BR, legendas sincronizadas, ilustrações próprias, trilha e efeitos sonoros originais. Formato 1080 × 1920, 30 fps, H.264 + AAC.

## Reproduzir e exportar

Requer Node 22+, FFmpeg e Chromium. O renderizador usa `/usr/bin/chromium`; ajuste o caminho em `scripts/render.mjs` caso necessário.

```bash
npm ci
npm run dev
npm run typecheck
npm run stills
npm run render
```

As composições são `Reel01` a `Reel12` e `Cover01` a `Cover12`. Os vídeos e capas são escritos em `out/<slug>/`. Para exportar apenas alguns vídeos:

```bash
node scripts/render.mjs video 1,2,3
```

Arquivos já renderizados são preservados; para refazer, use `FORCE=1 node scripts/render.mjs video 1`. O áudio já está incluído, portanto não é necessário gerar a voz novamente para renderizar.

## Estrutura e edição

- `campaign.json`: títulos, textos de capa, legendas dos posts, roteiros, CTA e indicação de oferta.
- `src/Art.tsx`: tipografia, personagens, box, janela deslizante, portão, guarda-corpo, casa, mapa e componentes gráficos.
- `src/Scenes.tsx`: cenas próprias dos 12 assuntos, incluindo diálogos, demonstrações, quizzes e checklists.
- `src/Film.tsx`: montagem, transições, legendas e margem segura.
- `public/timings-aligned.json`: duração, cenas e movimento de boca alinhados à voz.
- `public/captions-*.json` e `words-*.json`: texto canônico e tempos das palavras.
- `public/audio/01` a `12`: fala isolada, voz com duração final, trilha, efeitos e mixagem.
- `scripts/prepare-delivery.py`: monta a pasta de postagem com MP4, capa JPG, legenda do post e SRT.
- `scripts/verify.py`: verifica exportação, decodificação integral, áudio, legendas, capa e pausas dos quizzes.

O azul é #0131CD, o branco #FFFFFF e o verde-lima #B9FC01. Elementos essenciais ficam a 120 px das laterais, 220 px do topo e 340 px do rodapé. A logo SVG local é a marca fornecida anteriormente; a versão branca conserva seus caminhos e proporções. A Montserrat ExtraBold está incluída com sua licença.

## Voz e sincronização

A voz é sintética, Kokoro `pm_santa`, em português brasileiro, sem clonagem. `scripts/audio.py` gera a fala em velocidade nativa 0,93 e insere os 2 segundos de pausa dos quizzes sem narrar as instruções entre colchetes. A pronúncia das letras A e B pode ser especificada foneticamente como á e bê; o roteiro e as legendas conservam as letras originais.

`scripts/align.py` alinha a transcrição de Whisper ao roteiro canônico e respeita os intervalos sem fala dos quizzes. `speech-review.json` registra o reconhecimento automático, que pode diferir da escrita original em contrações e nomes. Os roteiros e o texto das legendas não são substituídos pela grafia reconhecida.

A regeneração opcional de áudio requer Python, kokoro-onnx, onnxruntime, NumPy, SoundFile e faster-whisper, além dos modelos Kokoro ONNX e `voices.bin` em `work/models/`. Esses modelos não fazem parte do pacote editável. Depois de mudar um roteiro, regenere a voz, os tempos e a mixagem antes de renderizar; editar apenas o JSON não altera uma gravação já gerada.

Os tempos aproximados do briefing foram adaptados à duração natural de cada fala integral, com três segundos de encerramento após a voz e dois segundos de espera nos quizzes. Não foram usados longos intervalos sem fala para completar artificialmente os tempos de referência.

## Referências e conteúdo comercial

Os 12 vídeos Dorami indicados no briefing orientaram a montagem: personagem → palavra-chave → explicação; cartões; quizzes; aproximações; encerramento de marca. Nenhum trecho de vídeo, áudio, personagem ou marca da Dorami foi incorporado. `briefing.md` preserva o pedido original.

A oferta exibida nos vídeos 01, 04, 05 e 06 é **Gestão por R$ 650/mês**, com **verba de anúncios à parte**. Os CTAs são orgânicos: WhatsApp pelo link da bio, salvar, comentar ou direct. Não há botão fictício de anúncio. As conversas são identificadas como Simulação; não há depoimentos, números de resultado ou garantias inventadas.

Os arquivos de postagem são preparados para publicação manual; nenhum vídeo foi publicado automaticamente em redes sociais.

## Pasta pronta para postagem

Depois de renderizar e verificar os 12 arquivos, execute:

```bash
python3 scripts/prepare-delivery.py
python3 scripts/package.py
```

A pasta `IB_MIDIAS_PRONTO_PARA_POSTAR/`, ao lado do projeto, reúne as quatro entregas de cada Reel e um índice. O pacote ZIP completo inclui `index.html`: após extrair, abra esse arquivo no navegador para assistir aos 12 vídeos e acessar os arquivos de cada post. O projeto editável é empacotado separadamente.
