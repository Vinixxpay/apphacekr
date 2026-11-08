# iB Mídias — duas vidraçarias na mesma cidade

Vídeo em Remotion/React, com ilustrações vetoriais em SVG. Saída vertical 1080 × 1920, 30 fps, H.264/AAC. A prévia de 10 segundos e a exportação completa ficam em `../entregas/`.

## Composição

- Animação branca nos 46% superiores, traços e letreiros #0131CD e destaques #B9FC01.
- Fachadas A e B na mesma rua, produtos revelados com a fala, comparação de propostas, medição, material, instalação, caixa, acabamento, escudo de confiança, mapa, indicação e anúncios.
- Parte inferior com imagem e voz originais, enquadramento guiado pelo rosto e aproximações nos trechos de ênfase.
- Divisória branca em papel rasgado e legendas Montserrat ExtraBold em grupos de uma a três palavras. O azul claro antecede a fala; o azul forte e os destaques verdes entram no tempo de cada palavra.
- Marca no canto superior esquerdo da área do apresentador e no CTA. `public/logo.svg` é uma versão monocromática obtida do símbolo da própria iB Mídias já fornecido, sem criar um símbolo novo.

A gravação menciona Google, além de Instagram e Facebook; os três canais aparecem no anúncio ilustrado. As mensagens e os projetos são desenhos demonstrativos, sem números de resultados, citações ou depoimentos fabricados. A instalação dentro do celular é ilustrada com SVG; não foi adicionado vídeo de obra de terceiros.

## Revisão da gravação

`edit-plan.json` registra os trechos mantidos e os cortes. A edição elimina a preparação inicial, a tentativa “no seu lucro” antes da correção “no seu bolso”, uma pergunta com tropeço na dicção e a sobra após o encerramento. Mantém “Quer vender mais?”, o convite ao Saiba Mais, a voz natural e as pausas internas das tomadas, sem aceleração nem voz sintética. As correções de ortografia do reconhecimento incluem “box”, “vidro” e “indicações”.

A trilha discreta foi sintetizada originalmente para a iB Mídias em `../edicoes-originais/scripts/music.py`; o arquivo está incluído e não exige licença musical de terceiros. A voz é normalizada para aproximadamente −16 LUFS e permanece à frente da trilha. Os pequenos fades de 3 ms nos cortes evitam estalos.

## Reproduzir

Requer Node 22+, Chromium em `/usr/bin/chromium`, FFmpeg/FFprobe e Python. Os originais, proxies e áudios privados não são publicados. Coloque o MOV em `input/`, mantendo a extensão `.MOV`.

```bash
npm ci
python -m venv .venv
.venv/bin/pip install -r requirements.txt
mkdir -p work out public/video
ffmpeg -i "input/IMG_2393 3.MOV" -vf "fps=30,scale=1080:1920:flags=lanczos" -c:v libx264 -preset fast -crf 18 -threads 3 -c:a pcm_s16le work/source.mkv
.venv/bin/python scripts/inspect_source.py
.venv/bin/python scripts/make_edit.py
.venv/bin/python scripts/prepare_presenter.py
npm run typecheck
npm run render:preview
.venv/bin/python scripts/compose.py preview
npm run render:full
.venv/bin/python scripts/compose.py full
.venv/bin/python scripts/verify.py
```

O Whisper medium deve estar no cache do Hugging Face (`HF_HOME`), pois o script foi configurado para reutilizar o modelo local. O arquivo original possui 4K/60 fps com rotação; o FFmpeg aplica a orientação automaticamente. A duração final é definida pelos trechos preservados, não por alteração de velocidade.

Para abrir a prévia reproduzível no Remotion Studio: `npm run dev`. As composições são `Vidracarias` (vídeo completo, com o apresentador e áudio) e `Stage` (camada gráfica). O pipeline da entrega renderiza a camada SVG com Remotion e combina com a imagem original em FFmpeg, evitando uma nova decodificação do vídeo 4K a cada quadro do navegador. A composição completa permanece disponível no projeto.

O MP4 principal sai em `out/ib-midias-vidracarias.mp4`; a prévia sai em `out/ib-midias-vidracarias-previa-10s.mp4`. A verificação confere duração, codec, resolução, quadros, limites das legendas, integridade da decodificação e preservação do áudio da fala.
