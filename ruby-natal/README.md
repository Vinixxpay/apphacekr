# Ruby Lingerie — Natal vertical

## Revisão atual — apresentadora e TV no mesmo quadro

Entrega: `../entregas/ruby-lingerie-natal-tv-mesma-cena.mp4`, aproximadamente 38 s, vertical Full HD. Mantém o cochilo antes da abdução. Aos 22,4 s, abre uma composição com a apresentadora adormecida à esquerda no sofá e a televisão à direita. A composição permanece por um momento antes de iniciar o feixe de luz; o recorte então flutua na direção da TV e diminui uniformemente até entrar na tela. A câmera se aproxima da televisão para a passagem ao filme.

O fundo é uma imagem real do sofá vazio no primeiro quadro do take horizontal enviado. A apresentadora e o lençol são recortados do próprio take do cochilo, com máscara e bordas suavizadas. A TV vem do vídeo original e é posicionada em perspectiva; a perspectiva afeta somente a televisão. Não são criados rosto, corpo ou roupas. É uma composição de takes originais, e não uma gravação simultânea dos dois ângulos. A parte de divulgação falada continua aguardando o arquivo original.

Após preparar e renderizar as revisões anteriores:

```bash
python scripts/prepare_same_scene.py
python scripts/render_same_scene.py
python scripts/verify_same_scene.py
```

O render preserva os primeiros 672 quadros da revisão com cochilo. Os registros são `edicao-mesma-cena.json` e `verificacao-mesma-cena.json`.

## Revisão — cochilo antes da abdução

Entrega atual: `../entregas/ruby-lingerie-natal-cochilo-abducao.mp4`, 35 segundos, 1080 × 1920, 30 fps. Após o controle, o take original do cochilo entra aos 16,5 s. A abdução começa aos 22,4 s usando o recorte da mesma pose adormecida; luz, partículas e um movimento para cima conduzem a apresentadora para a televisão. O filme vem depois, seguido pela assinatura da Ruby. A pose do efeito é extraída do próprio vídeo, sem criar uma pessoa ou alterar proporções do rosto e corpo.

A primeira prévia permanece disponível. O vídeo e áudio da divulgação falada continuam pendentes; esta revisão altera a sequência e o efeito solicitados.

Após reproduzir a primeira prévia, execute:

```bash
python scripts/prepare_abduction.py
python scripts/render_abduction.py
python scripts/verify_abduction.py
```

O render reaproveita os primeiros 495 quadros da primeira prévia e reconstrói a sequência a partir do cochilo. O áudio instrumental é remontado integralmente para sincronizar o crescimento da trilha e os sinos com o novo momento da abdução. Os dados estão em `edicao-abducao.json` e `verificacao-abducao.json`.

Prévia de 34,13 segundos, 1080 × 1920, 9:16, 30 fps, H.264/AAC. Cenas 1–3 montadas com os quatro vídeos enviados, tratamento quente, dissoluções, recorte da apresentadora, luz e partículas na entrada na televisão, sonho e assinatura temporária bordô/dourado do Amigo Calcinha.

**Pendente:** o vídeo da divulgação falada do Amigo Calcinha não foi incluído nos quatro anexos. O take da xícara/controle não tem faixa de áudio. As outras faixas são do filme na TV e ambiente; o take do sonho não contém a divulgação. A prévia não inventa a voz nem as falas da apresentadora. A cena 4 e suas legendas aguardam esse vídeo com o áudio original. A assinatura temporária entra após o sonho para permitir avaliar a identidade visual.

Os takes horizontais do sofá são reenquadrados para o retrato sem distorcer proporções. Na televisão, usa-se a imagem completa sobre um fundo desfocado derivado do mesmo take. O sonho mantém o ambiente e a imagem originais. O portal usa um recorte de uma pose do take do controle, com escala uniforme e deslocamento. Não há geração de rosto, corpo, roupa ou ambiente. A prévia começa após a entrada em que a câmera original cortava a cabeça, preservando os momentos de sentar, usar o lençol, tomar chocolate e ligar a TV.

A trilha é instrumental original sintetizada, com sinos e efeito de transição no portal. Ela substitui os áudios do filme na TV e do ambiente nesta prévia; nenhuma fala promocional foi removida. As fontes têm resolução de WhatsApp (640 × 368, 848 × 480 e 368 × 656); a exportação Full HD não recupera detalhes inexistentes.

## Reproduzir

Requer Python, NumPy, OpenCV, ONNX Runtime, Pillow e FFmpeg/FFprobe. Instale com `python -m pip install -r requirements.txt`. O render usa DejaVu Serif e Sans em `/usr/share/fonts/truetype/dejavu/`.

Coloque os quatro MP4s originais em `input/`, mantendo os horários dos nomes. Baixe o modelo RVM MobileNetV3 FP32 de https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx para `work/rvm.onnx`.

```bash
mkdir -p work entrega
python scripts/prepare.py
python scripts/render_vertical.py
python scripts/verify.py
```

Também é possível definir `RUBY_INPUT` como a pasta dos originais e `RUBY_RVM` como o caminho do modelo. A saída é `entrega/ruby-lingerie-natal-previa-vertical.mp4`. `edicao-vertical.json` registra a linha do tempo; `verificacao-vertical.json` registra a checagem do MP4. Os originais e intermediários não são publicados.
