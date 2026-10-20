# iB Mídias — Motion design com narração

Peça vertical de 45 segundos, 1080 × 1920, 30 fps, em preto/grafite/branco e verde-limão `#C6FF00`. Marca em texto, sem símbolo inventado. As sete cenas seguem os tempos pedidos: 0–6, 6–11, 11–16, 16–24, 24–32, 32–37 e 37–45 segundos.

O painel usa traços no lugar de métricas. O contato em movimento é ilustrativo; não representa resultado ou depoimento. Os textos principais ficam entre x=84 e x=946, acima de y=1450, reservando espaço para a interface de anúncios. A chamada final está totalmente revelada a partir de aproximadamente 39,1 s e permanece até 45 s.

## Prévia e exportação

Requer Node.js 22+ e Chrome/Chromium. No ambiente usado para esta entrega, o Chromium está em `/usr/bin/chromium`.

```bash
cd motion-ib-midias
npm ci
npm run dev
```

A prévia interativa do Remotion permite navegar por todos os quadros e ouvir o áudio. Para exportar:

```bash
npm run render
```

Comando completo equivalente, executado e validado no ambiente:

```bash
npx remotion render src/index.ts IBMidias out/remotion-master.mp4 --codec=h264 --pixel-format=yuv420p --audio-codec=aac --browser-executable=/usr/bin/chromium --concurrency=2 --crf=20
node scripts/finalize.mjs
```

Para outro caminho do Chrome, ajuste `--browser-executable`. O render tem 1350 quadros. A finalização converte a saída do navegador para YUV420p/BT.709 de faixa limitada, preserva o AAC e aplica faststart para reprodução pela web. Requer `ffmpeg` no PATH. Depois de renderizar, abra `preview.html` para assistir ao MP4 com controles. O ZIP de entrega inclui o render e a imagem de capa dentro de `out/`, então a prévia também funciona sem instalar dependências.

```bash
npm run typecheck
npm run still
node scripts/stills.mjs
```

`stills.mjs` exporta um quadro de leitura de cada cena. A captura usa o navegador real e as fontes locais, sem depender de Google Fonts.

## Voz e trilha

A voz é sintética em português do Brasil, gerada localmente pelo Piper com o modelo `pt_BR-faber-medium`, sem clonagem e sem serviço pago. O cartão do modelo, com a licença CC0 do conjunto de voz, está em `public/audio/VOICE-MODEL-CARD.txt`. Fonte: https://huggingface.co/rhasspy/piper-voices/tree/main/pt/pt_BR/faber/medium

`public/audio/mix.wav` já contém narração, trilha instrumental original sintetizada para esta peça e sopros discretos nas transições. As falas e suas durações estão em `public/audio/narracao.json`. A voz foi encaixada por cena, sem truncar frases. Não é necessário baixar o modelo para renderizar o vídeo com esse áudio.

Para recriar a narração e a trilha após editar as falas em `scripts/audio.py`, com Python 3.12, `uv`, `curl`, `sha256sum` e `ffmpeg` disponíveis:

```bash
bash scripts/prepare-voice.sh
npm run render
```

O script baixa o modelo por HTTPS, verifica os hashes, instala as dependências locais e gera novamente o áudio. As fontes Inter e sua licença estão em `public/`. Os ícones de moto, localização, pagamento e conversa são vetores do projeto, não logos de terceiros.

## Estrutura

- `src/Film.tsx`: animações, grafismos e cenas.
- `src/Root.tsx`: composição de 45 segundos.
- `public/`: áudio, fontes locais e licenças.
- `scripts/`: geração opcional de voz e capturas para revisão.
- `preview.html`: reprodução do MP4 exportado.

O projeto é novo porque o checkout existente continha apenas os vídeos de entrega anteriores. Esses arquivos foram preservados.
