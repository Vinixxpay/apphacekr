# iB Mídias — vídeo 4, legendas e vinheta final

Entrega: `entregas/ib-midias-vd4-legendas-logo.mp4` na raiz do repositório.

MP4 vertical 1080 × 1920, 60 fps, H.264 + AAC. São 33 segundos da gravação, seguidos de 2,2 segundos de vinheta: 35,2 segundos no total.

Foram retirados a preparação anterior à primeira frase e o trecho posterior ao encerramento. A explicação do método MVP e a chamada “Saiba mais e fala comigo” são preservadas. A repetição expressiva de “orçamento” faz parte do argumento e foi mantida. A voz não foi acelerada; o enquadramento inteiro foi preservado.

Legendas: Montserrat ExtraBold, maiúsculas, grupos de 1 a 3 palavras, caixas brancas com borda #0131CD, cantos arredondados, sombra suave e entrada discreta. Palavras futuras ficam em azul claro e mudam para azul forte quando faladas. Termos principais recebem #B9FC01. A transcrição em português foi revisada com uma segunda passagem para termos como marketing, pós-venda, MVP, mesmo resultado e Saiba Mais.

A vinheta utiliza o SVG do símbolo oficial já disponível no projeto, em azul, com o nome iB Mídias. O movimento combina aproximação discreta e fade. Um whoosh suave e duas notas curtas foram sintetizados para esta entrega; não foi acrescentada música ou efeito durante a fala. O som começa apenas na vinheta.

`edit.json` registra os cortes e a duração da vinheta. `transcript-reviewed.json` contém os tempos de origem e de entrega das palavras. `verification.json` registra as verificações de duração, quadros, legendas, áudio preservado e presença do efeito final.

## Reconstruir

Requer Python com Pillow e FFmpeg com libass, libx264 e leitura de SVG. O vídeo original é privado e não é incluído no projeto.

```bash
python scripts/make_captions.py
python scripts/make_outro.py
CAPTION_SOURCE=/caminho/para/original.MOV python scripts/render.py
CAPTION_SOURCE=/caminho/para/original.MOV python scripts/verify.py
```
