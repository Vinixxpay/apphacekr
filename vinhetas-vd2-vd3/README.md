# Vinheta final nos vídeos 2 e 3

Os dois arquivos enviados foram conferidos por SHA-256 e são idênticos às entregas originais já presentes no repositório. A mesma vinheta aprovada no vídeo 4 foi acrescentada após o fim de cada vídeo: logo oficial iB Mídias animada e assinatura sonora, com 2,2 segundos.

A imagem dos vídeos e suas legendas foram copiadas sem nova compressão, zoom ou corte. A voz completa foi mantida; o efeito sonoro entra somente depois do fim do arquivo original. O áudio foi concatenado e codificado em AAC para evitar problemas de sincronização entre os arquivos.

Entregas em `entregas/`, na raiz do repositório:

- `ib-midias-vd2-com-final-logo.mp4`: 32,63 segundos.
- `ib-midias-vd3-com-final-logo.mp4`: 30,2 segundos.

Ambos: MP4, H.264 + AAC, vertical 1080 × 1920, 60 fps.

`verification.json` registra duração, quadros, decodificação completa e igualdade dos pixels em amostras do começo, meio e fim da gravação. Todos os quadros originais foram mantidos.

Para reconstruir, com FFmpeg instalado e os dois arquivos originais presentes em `entregas/`:

```bash
# Gerar novamente a vinheta compartilhada, se necessário:
python vd4-legendas/scripts/make_outro.py
python vinhetas-vd2-vd3/scripts/append.py
```

É possível informar os anexos equivalentes usando `VD2_INPUT` e `VD3_INPUT`. O script confere que correspondem às versões originais aprovadas.
