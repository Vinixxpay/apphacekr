# Ruby Lingerie — prévia de Natal vertical

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
