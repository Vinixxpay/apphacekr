# Sacolas e bobinas — R$ 16/kg

Edição da gravação IMG_2485.MP4. Mantém voz, produtos e imagem originais. Duração de 16,1 segundos, com pausas encurtadas e retirada da hesitação e da voz externa perto do fim. Mantida a última frase da apresentadora, “bobina picotada”. Intervalos preservados documentados em `edit.json`.

Legendas dinâmicas, em grupos curtos, sincronizadas com as palavras. Um cartão opaco substitui o texto com erros que já estava gravado na imagem. Preço R$ 16/kg incluído conforme solicitação. Tratamento moderado de ruído, equalização, compressão e normalização da voz. Sem música, voz sintética ou alteração de velocidade.

Saída MP4 H.264 + AAC, vertical 1080 × 1920, 30 fps, faststart. O original tem 720 × 1280; a exportação é ampliada para Full HD, sem recuperar detalhes inexistentes na gravação.

## Exportar novamente

Requer Python com Pillow e FFmpeg com libass. Coloque o original em `input/IMG_2485.MP4` e execute nesta pasta:

```bash
python scripts/make_captions.py
python scripts/add_offer.py
python scripts/render.py input/IMG_2485.MP4 out/sacolas-bobinas-16-reais-kg.mp4
```

O arquivo original não está incluído. A fonte Inter acompanha a licença em `public/fonts/Inter-OFL.txt`.
