# iB Mídias — edição de video2.MOV

## Revisão 2 — tentativas e movimentos de preparação removidos

Esta revisão substitui a entrega anterior para uso. A revisão anterior deixou passar uma primeira tentativa dos anúncios e um reposicionamento na cadeira. A leitura automática de trechos longos havia unido duas tentativas na mesma transcrição; conferir apenas os codecs e a correlação da fala com esse recorte não validava a montagem editorial.

O original foi novamente conferido em janelas curtas sobrepostas e por imagens nos pontos de interrupção. A montagem preserva uma única exposição completa dos anúncios: a tentativa completa com Instagram, Facebook e Google. Na frase de encerramento, usa a primeira parte correta e emenda a continuação “pode contratar você”, retirando o reinício e a aproximação para ajustar a gravação. Também retira a repetição antes de “pede o orçamento” e termina com o apresentador ainda sentado, após o convite completo.

A decodificação do vídeo é sequencial, sem saltos aproximados por quadro. `source-edit.json` identifica os trechos preservados; `editorial-review.json` registra as conferências específicas das emendas. O visual, as ilustrações e as cores permanecem os da edição solicitada.

Segunda gravação com o mesmo visual da edição anterior: vídeo vertical 1080 × 1920, 30 fps, animações SVG/React em Remotion nos 46% superiores e o apresentador original embaixo. As entregas ficam em `../entregas/ib-midias-vidracarias-video2-revisado.mp4` e `../entregas/ib-midias-vidracarias-video2-previa-10s.mp4`. A primeira gravação permanece preservada.

A duração completa é aproximadamente 1min17s. A edição mantém a voz e as pausas naturais, sem aceleração, clonagem, substituição de voz ou novas falas. A preparação inicial e a saída da cadeira após a fala foram retiradas. Foram retirados o reinício antes de “pede o orçamento”, as tentativas abandonadas dos anúncios e o reinício da frase de encerramento, usando a primeira parte correta e sua continuação.

## Sincronização e identidade

As legendas Montserrat ExtraBold usam de uma a três palavras, caixa branca, borda azul #0131CD e destaques #B9FC01 no instante da fala. A animação inclui as duas fachadas, box, espelho, porta de vidro, preços e propostas, etapas do serviço, caixa, acabamento, confiança, mapa, indicação e anúncios. A divisória é branca em papel rasgado, com a legenda sobreposta. O símbolo da iB Mídias aparece na área do apresentador e no CTA.

Este take diz “foi mais barato”, cita Instagram, Facebook e Google e encerra pedindo o preenchimento de um formulário. A mensagem do celular e o CTA acompanham essas falas; o WhatsApp aparece na explicação dos anúncios. Não há preços, números de resultados ou citações de clientes inventados. Os projetos, a instalação e a conversa de WhatsApp são ilustrados com SVG.

`source-edit.json` registra os cortes, os tempos das cenas e a revisão do trecho repetido. As transcrições longas haviam fundido tentativas; os trechos mantidos foram alinhados e conferidos separadamente. O arquivo também registra pequenas correções de transcrição, sem criar áudio novo. `edit-plan.json` e `src/data.ts` contêm o plano e os tempos finais.

A trilha original discreta já utilizada na iB Mídias foi sintetizada em `../edicoes-originais/scripts/music.py` e está incluída. A voz é normalizada para aproximadamente −16 LUFS e permanece à frente da trilha. Há fades de 3 ms nos cortes para evitar estalos.

## Reproduzir

Requer Node 22+, Chromium em `/usr/bin/chromium`, FFmpeg/FFprobe e Python. Coloque o original em `input/video2.MOV`. Os originais, proxies, áudio extraído e intermediários ficam ignorados pelo Git.

```bash
npm ci
python -m venv .venv
.venv/bin/pip install -r requirements.txt
mkdir -p work out public/video
ffmpeg -i input/video2.MOV -vf "fps=30,scale=1080:1920:flags=lanczos" -c:v libx264 -preset fast -crf 18 -threads 3 -c:a pcm_s16le work/source.mkv
.venv/bin/python scripts/inspect_source.py
.venv/bin/python scripts/make_edit.py
.venv/bin/python scripts/prepare_presenter.py
npm run typecheck
npm run render:preview
.venv/bin/python scripts/compose.py preview
npm run render:full
.venv/bin/python scripts/compose.py full
.venv/bin/python scripts/verify.py
```

O Whisper medium deve estar disponível no cache `HF_HOME`; o script reutiliza o modelo local. O original é 4K/60 fps com rotação; a orientação é aplicada automaticamente pelo FFmpeg, mantendo a velocidade real.

Para uma prévia reproduzível no Remotion Studio: `npm run dev`. As composições são `VidracariasVideo2`, com vídeo e áudio preparados, e `Stage`, com os SVGs, as legendas e a identidade visual. O pipeline da entrega renderiza a camada gráfica em Remotion e combina com a gravação original em FFmpeg. A composição completa também está disponível no projeto.

Os MP4s saem em `out/`. `verification.json` registra resolução, codecs, duração, quadros, decodificação, limites e tempos das legendas e comparação da fala no início, meio e fim do vídeo final.
