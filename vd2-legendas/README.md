# vd2 — legendas dinâmicas e cortes necessários

Entrega: `entregas/ib-midias-vd2-legendas-e-cortes.mp4` na raiz do repositório.

Vídeo vertical 1080 × 1920, H.264, áudio AAC, 60 fps, cerca de 30,43 segundos. Mantém o enquadramento inteiro e a voz na velocidade original. A única camada visual acrescentada é a legenda Montserrat ExtraBold: caixa branca, borda azul #0131CD, pop discreto, palavras futuras em azul claro, palavras faladas em azul e destaques #B9FC01.

Revisão editorial: a primeira tentativa incompleta de “Aqui na iB Mídias nós…” foi retirada, preservando a segunda fala completa. Foram retirados a preparação inicial, o trecho depois da chamada final e parte do silêncio entre “orçamentos diários” e “pedidos diários”. Não foram cortadas frases de conteúdo nem aplicada aceleração. Os intervalos exatos constam em `edit.json`; os tempos das palavras no original e na entrega constam em `transcript-reviewed.json`.

O áudio foi transcrito em português com duas passagens de reconhecimento e uma revisão em janela curta do reinício, que a transcrição longa uniu incorretamente. Grafias corrigidas nas legendas: indicação, iB Mídias, Saiba Mais. Os números e as afirmações são apenas os da gravação, sem informação acrescentada.

## Renderizar

Requer Python com Pillow, FFmpeg com libass/libx264 e o arquivo original privado, que não é incluído no projeto.

```bash
python scripts/make_captions.py
CAPTION_SOURCE=/caminho/para/vd2.mp4 python scripts/render.py
CAPTION_SOURCE=/caminho/para/vd2.mp4 python scripts/verify.py
```

Os tempos revisados em `transcript-reviewed.json` permitem reconstruir as legendas sem executar novamente o reconhecimento de fala.
