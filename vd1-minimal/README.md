# iB Mídias — vd1, edição em tela cheia

Entrega: `../entregas/ib-midias-vd1-editado.mp4`, aproximadamente 1min16s, vertical 1080 × 1920, 30 fps, H.264/AAC.

Esta versão segue a orientação mais recente: gravação em tela cheia, sem tela dividida, legendas corridas ou ilustrações. Há apenas a marca discreta no canto superior esquerdo, em azul #0131CD, branco #FFFFFF e verde-lima #B9FC01. A fala permanece original, sem aceleração, com pausas naturais e trilha original muito baixa.

O `vd1.MOV` é o primeiro original da pasta, renomeado. A identidade do arquivo foi conferida pelo tamanho e pela leitura de um trecho remoto, comparado com o original já disponível. `source-validation.json` registra essa conferência sem divulgar o link do original.

`edit-plan.json` registra os cortes: preparação inicial, uma tentativa abandonada antes de “no seu bolso”, uma pergunta com tropeço na dicção e a sobra após a fala final. Mantém “Quer vender mais?” e o convite completo ao Saiba Mais. A câmera usa recortes uniformes com aproximações moderadas; não há geração ou deformação de rosto ou corpo. A imagem recebe ajuste leve de contraste, saturação e luminosidade. A voz já revisada do mesmo original foi reaproveitada nesta entrega.

## Reproduzir

Requer Node 22+, Python, FFmpeg/FFprobe e Chromium em `/usr/bin/chromium`. Os originais, áudios extraídos, proxies e intermediários não são publicados. Coloque o original em `input/vd1.MOV`.

```bash
npm ci
python -m venv .venv
.venv/bin/pip install -r requirements.txt
mkdir -p work out public/video
ffmpeg -i input/vd1.MOV -vf "fps=30,scale=1080:1920:flags=lanczos" -c:v libx264 -preset fast -crf 18 -threads 3 -c:a pcm_s16le work/source.mkv
.venv/bin/python scripts/prepare.py
npm run brand
npm run typecheck
.venv/bin/python scripts/compose.py
.venv/bin/python scripts/verify.py
```

Também é possível definir `VD1_PROXY` para reutilizar o proxy de 1080 × 1920 e 30 fps do mesmo original. A marca é renderizada em Remotion/React com transparência; a edição e a composição final usam FFmpeg. Para uma prévia reproduzível em Remotion Studio: `npm run dev`, composição `VD1`.

O MP4 usa BT.709, faststart, AAC a 192 kbps e vídeo com CRF 20 limitado a 8 Mbps para uma entrega Full HD adequada a redes sociais. A trilha foi sintetizada originalmente para a iB Mídias em `../edicoes-originais/scripts/music.py`; está incluída e não exige licença musical de terceiros. A fonte Montserrat e sua licença estão em `public/`.

`verification.json` registra codecs, quadros, duração, leitura completa, cores da marca e comparação da fala preservada no início, meio e fim.
