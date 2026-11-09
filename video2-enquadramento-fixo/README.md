# Vídeo 2 — enquadramento fixo

Revisão visual da versão `ib-midias-vidracarias-video2.mp4`, de 1min22s, indicada pelo usuário. A montagem, a duração, as palavras das legendas, as ilustrações e o áudio dessa versão são preservados.

A mudança está na área do apresentador: o recorte agora é constante, sem aproximações por frase, transições de escala, acompanhamento automático do rosto ou movimentos digitais de câmera. O recorte da fonte 1080 × 1920 é 984 × 944 em (0, 520), redimensionado para o painel 1080 × 1036. As animações explicativas continuam na área superior.

O áudio AAC é copiado diretamente da versão aprovada, sem nova codificação ou alteração. A composição gráfica e os tempos foram recuperados do mesmo código da entrega citada. Esta revisão não altera as edições posteriores dos outros vídeos.

Entrega: `entregas/ib-midias-vidracarias-video2-estatico.mp4`, na raiz do repositório, em 1080 × 1920, 30 fps, H.264 + AAC.

## Reconstruir

Requer Node, dependências Remotion do `package.json`, Chromium em `/usr/bin/chromium`, Python e FFmpeg. O proxy original `vidracarias-sticker-video2/work/source.mkv` é privado e não é incluído no Git. Pode ser informado em outro caminho com `STATIC_SOURCE`.

```bash
python scripts/render_static.py
node scripts/render.mjs full
python scripts/compose_static.py
python scripts/verify.py
```

O estágio de composição conserva os SVGs, as cores e as legendas originais. `static-framing.json` registra o recorte fixo e os intervalos da montagem. `verification.json` registra os quadros, a duração, a decodificação completa e a igualdade do áudio com o MP4 de referência.

## Correção da tentativa interrompida por volta dos 57 segundos

Entrega: `entregas/ib-midias-vidracarias-video2-estatico-corrigido.mp4`, com 1min16,6s.

Retira os quadros 1581–1753 da versão estática anterior (52,7–58,4667s), que continham a primeira tentativa dos anúncios e a interrupção de gravação. Mantém uma única exposição completa com Instagram, Facebook e Google. São removidos 173 quadros; o restante da montagem conserva a mesma sequência e o enquadramento fixo aprovado.

A região gráfica dos anúncios foi recomposta com as legendas já revisadas para a tentativa completa, pois a transcrição longa anterior havia fundido as duas tentativas. A recomposição usa o mesmo painel estático e a camada gráfica revisada disponível em `vidracarias-sticker-video2/out/stage-full.mp4`. A partir de 60,8s, retorna à composição original, já sem legenda ativa na emenda. A voz é mantida com a edição correspondente, sem alteração de velocidade, e fades de 3 ms evitam estalos no corte.

```bash
python scripts/correct_ads.py
python scripts/verify_corrected.py
```

`ads-correction.json` registra os pontos da correção, e `corrected-verification.json` registra a duração, os quadros, a correlação do áudio com os trechos mantidos e a decodificação integral.
