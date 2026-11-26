# Ruby — moeda somente na primeira oferta e cartaz recriado

Revisão do Reels aprovado. A moeda 3D aparece somente na primeira fala de “um real”, aos 10,627 s. A segunda entrada da moeda e seus sons foram removidos. Brilhos laterais, voz, legendas, oferta e abertura permanecem.

O encerramento parte da placa real. A arte recriada surge alinhada à área impressa durante a aproximação; o cenário desaparece gradualmente e o cartaz ocupa o quadro, seguindo o mesmo zoom e mantendo breve aproximação suave para leitura. Duração final aproximada de 31 s.

A arte foi gerada a partir do frame real do cartaz, preservando megafone rosa, fundo escuro, faixas e texto “SUPER OFERTAS DE BLACK FRIDAY / EM BREVE!”. Não foram adicionadas datas, preços ou informações ao cartaz. A geração é uma recriação visual, não o arquivo gráfico original.

## Reprodução

Executar da raiz do repositório. FFmpeg com libx264 e Python são necessários. Os ativos dos projetos anteriores são reutilizados, mantendo todas as entregas antigas.

```bash
python ruby-black-friday-cartaz/scripts/outro.py
python ruby-black-friday-cartaz/scripts/render.py
```

A composição intermediária da aproximação usa resolução ampliada para preservar a nitidez da arte digital. Saída final H.264 + AAC estéreo, 1080 × 1920, 30 fps, faststart.
