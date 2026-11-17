# Lavaí — demonstração editada

Gravação original de 60,89 s editada para 49,57 s, em 1080 × 1920 a 30 fps. Voz original mantida, sem alteração de velocidade ou de tom.

Oito cortes removem pausas longas e a segunda apresentação repetida da equipe. Os intervalos exatos constam em `edit.json`. Foram preservadas as explicações sobre painel, vendas, relatórios, preços, identidade visual, comprovante, permissões da equipe e Android/iOS. A imagem da demonstração mantém o enquadramento original.

Áudio: filtro de graves, redução moderada de ruído, equalização leve, compressão e normalização para alvo de −16 LUFS e teto de −1,5 dBTP. Não foi adicionada música para preservar a inteligibilidade.

Legendas em Inter ExtraBold, caixa clara, texto azul-escuro e destaques amarelos. Grupos curtos com mudança de cor sincronizada às palavras. Cinco chamadas superiores discretas com entrada suave destacam as funções sem cobrir a tela do aplicativo. Sem números ou resultados comerciais inventados.

## Reprodução e exportação

O original não é publicado. Coloque a gravação em `input/original.mp4`. Instale FFmpeg com libass e Python com Pillow; a fonte Inter está em `public/fonts`, com licença.

As legendas e os cortes revisados já estão prontos. Para regenerar e exportar, a partir da raiz deste projeto:

```bash
python scripts/make_captions.py
python scripts/add_badges.py
python scripts/render.py input/original.mp4 out/lavai-demonstracao-editada.mp4
```

`transcript-reviewed.json` contém palavras e tempos ajustados à edição; `captions.json` contém os grupos e a posição. `scripts/prepare.py` documenta a preparação original a partir da transcrição de trabalho; não é necessário executá-lo para exportar.

Formato final: MP4, H.264, AAC estéreo 48 kHz, 30 fps, yuv420p, BT.709 e faststart para reprodução na web.
