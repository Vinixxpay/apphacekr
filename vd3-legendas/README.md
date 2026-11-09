# vd3 — legendas dinâmicas e cortes necessários

Entrega: `entregas/ib-midias-vd3-legendas-e-cortes.mp4`, na raiz do repositório.

MP4 vertical 1080 × 1920, 60 fps, H.264 + AAC, 28 segundos. Mantém a imagem inteira, a velocidade e a voz da gravação. A única camada visual acrescentada é a legenda Montserrat ExtraBold, em grupos de 1 a 3 palavras, com caixa branca, contorno #0131CD, cantos arredondados, sombra suave, entrada discreta e leitura karaokê. Os destaques de vidraçaria, orçamento, WhatsApp e Saiba Mais usam #B9FC01.

Foram removidos a preparação inicial e o trecho após o encerramento. Todo o conteúdo falado foi mantido: a pergunta inicial, a apresentação, a explicação da conversão e a chamada para preencher o formulário. Não há repetição completa de tomada que justifique retirar uma frase. As pausas curtas foram preservadas para manter a voz natural.

A revisão usou reconhecimento em português, uma segunda passagem independente e janelas curtas para palavras ambíguas. Grafias e nomes corrigidos nas legendas: iB Mídias, orçamento, WhatsApp, Saiba Mais, reunião, alcançar. Os números e as afirmações são os da própria gravação.

`edit.json` registra os cortes em quadros e segundos; `transcript-reviewed.json` contém os tempos das palavras na fonte e na entrega. `verification.json` registra a verificação de resolução, duração, quadros, enquadramento das legendas, decodificação completa e correlação com a voz original.

## Reconstruir

Requer Python com Pillow e FFmpeg com libass/libx264. O original privado não é incluído no projeto.

```bash
python scripts/make_captions.py
CAPTION_SOURCE=/caminho/para/vd3.MOV python scripts/render.py
CAPTION_SOURCE=/caminho/para/vd3.MOV python scripts/verify.py
```

As palavras e os tempos já revisados permitem reconstruir as legendas sem executar novamente o reconhecimento de fala.
