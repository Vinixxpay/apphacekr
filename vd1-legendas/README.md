# vd1 — somente legendas dinâmicas

Entrega: `../entregas/ib-midias-vd1-somente-legendas.mp4`, vertical 1080 × 1920. Usa o original inteiro do link indicado, sem os cortes, reenquadramentos, aproximações, marca adicional, trilha ou ajustes de áudio das edições anteriores. A taxa original de 60 fps é mantida. O áudio AAC é copiado sem recodificação.

A única camada adicionada é a legenda: Montserrat ExtraBold em maiúsculas, caixa branca de largura variável, borda #0131CD, cantos arredondados e sombra leve. Cada grupo tem uma a três palavras, com pop discreto. As palavras futuras ficam em azul claro e passam ao azul forte quando faladas. Os destaques #B9FC01 entram no instante dos termos principais. A legenda fica centralizada em y=1490, acima da área inferior dos controles, sem cobrir o rosto.

Os tempos foram revistos em janelas curtas de áudio, com correção da grafia de termos como box, vidro e indicações. As repetições e pausas da gravação permanecem no vídeo e na transcrição; esta edição não corrige a montagem do original. Após a fala, “SAIBA MAIS”, já dito na gravação, permanece legível por aproximadamente quatro segundos no mesmo estilo de legenda.

`transcript-reviewed.json` contém as palavras e seus tempos na linha original. `captions.json` contém grupos, destaques e caixas; `captions.ass` é a camada incorporada pelo FFmpeg. A fonte está incluída com sua licença. O tamanho ASS é calibrado para a métrica da fonte, mantendo o tamanho visual e a medição das caixas consistentes.

## Reproduzir

Requer Python com Pillow e FFmpeg/FFprobe compilado com libass. Coloque o original em `input/vd1.MOV`; também é possível definir `CAPTION_SOURCE` para seu caminho completo. Os originais e intermediários ficam ignorados pelo Git.

```bash
mkdir -p work out input
python -m pip install -r requirements.txt
python scripts/make_captions.py
python scripts/render.py
python scripts/verify.py
```

Não é necessário alterar a transcrição para exportar novamente. A orientação original do MOV é aplicada pelo FFmpeg antes da redução de resolução. O áudio não passa por filtros, normalização, aceleração ou mixagem. O arquivo usa H.264, áudio original AAC e faststart. `verification.json` confere todos os quadros, taxa, duração, decodificação e igualdade dos pacotes AAC originais, além da posição e duração das legendas.
