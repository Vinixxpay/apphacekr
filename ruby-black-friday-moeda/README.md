# Ruby Black Friday — moeda 3D

Revisão do vídeo aprovado em `entregas/ruby-black-friday/ruby-black-friday-reels.mp4`. Preserva a montagem, a fala, as legendas e a aproximação final da placa.

Duas entradas de uma moeda 3D estilizada de R$ 1, com aro dourado e centro prateado, em 10,627 s e 20,633 s, sincronizadas com “um real”. A moeda cai, quica e gira ao lado da apresentadora; a entrada dura dois segundos e termina com transparência gradual. Os efeitos metálicos são sintetizados localmente e ficam sob a voz.

Brilhos rosa suaves aparecem apenas nas laterais do cenário durante a oferta, mantendo a região central do rosto livre. Não há remoção ou alteração do corpo da apresentadora.

## Renderizar

Requer FFmpeg com libx264. O vídeo da moeda com transparência e os efeitos já estão prontos em `public`.

```bash
python ruby-black-friday-moeda/scripts/render.py \
  entregas/ruby-black-friday/ruby-black-friday-reels.mp4 \
  entregas/ruby-black-friday-v2/ruby-black-friday-moeda-3d.mp4
```

A moeda foi modelada e renderizada no Blender 4.3.2, Cycles CPU, 60 quadros a 30 fps, 480 × 480, 24 amostras. O script `scripts/coin_blender.py` registra a construção, materiais, iluminação e giro. `scripts/assets.py` gera os brilhos e o áudio, usando Python com Pillow, NumPy e SoundFile. O render final usa o objeto reduzido para 300 × 300, sem cobrir as legendas.

Exportação: MP4, H.264 + AAC estéreo, 1080 × 1920, 30 fps, faststart.
