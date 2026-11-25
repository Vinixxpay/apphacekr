# Ruby — Black Friday / Reels

Edição vertical da gravação `VID_20261125_203137.mp4`, fornecida pelo usuário via Drive. Abertura da cadeira acelerada, cortes de enquadramento em pontos de ênfase, legendas dinâmicas, rosa e preto em referência à placa original, chamadas para a oferta e zoom final na placa real.

A voz original permanece na velocidade natural. A edição encurta duas pausas e comprime a abertura sem fala. O final de três segundos utiliza um frame real capturado aos 32,9 s da gravação, com aproximação progressiva de 1× a 1,8×, recentrada na placa, e breve permanência para leitura. Não altera o texto “em breve” da placa nem inventa datas ou condições da promoção. A oferta “a partir de R$ 1” vem da fala original.

Trilha e efeitos instrumentais sintetizados localmente pelo script `music.py`, sem amostras externas, em volume reduzido sob a voz. Áudio da gravação recebe redução leve de ruído, equalização, compressão e normalização.

## Exportar

Requer FFmpeg com libass e libx264; Python com Pillow, NumPy e SoundFile. Coloque a gravação original em `input/original.mp4`. Os cortes, palavras revisadas, legendas, frame da placa e áudio instrumental estão incluídos; o vídeo original não está publicado.

```bash
python scripts/make_captions.py
python scripts/add_graphics.py
python scripts/music.py
python scripts/render.py input/original.mp4 out/ruby-black-friday-reels.mp4
```

Exportação: H.264 + AAC, 1080 × 1920, 30 fps, BT.709, yuv420p, faststart. `edit.json` documenta os cortes, as escalas e os tempos; `transcript-reviewed.json` contém a fala e os tempos por palavra. `prepare.py` documenta a preparação inicial usando a transcrição de trabalho e não é necessário para exportar novamente.

Fonte Inter distribuída com a licença em `public/fonts/Inter-OFL.txt`.
