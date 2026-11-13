# iB Mídias — versão cartoon

Releitura do anúncio de projetos de maior valor na linguagem do vídeo de referência enviado pelo usuário: animação 2D com personagens expressivos, cenários ilustrados que ocupam a tela, cortes entre planos abertos e closes e frases curtas brancas com fonte serifada no alto da imagem.

Os personagens e cenários são desenhos originais em SVG: profissional de vidros e esquadrias com uniforme azul, cliente, oficina, rua, agenda, carteira, projetos e celular. As expressões, piscadas, braços e mãos são animados. Nos planos de apresentação, a abertura da boca acompanha a energia da narração. A narrativa alterna 17 enquadramentos em oito sequências, mostrando o profissional sobrecarregado, a pressão por menor preço, a hipótese de projetos de maior valor e o papel dos anúncios e do WhatsApp.

A identidade da iB Mídias aparece no azul #0131CD, nos destaques verde-lima #B9FC01, na marca oficial e no encerramento. Os cenários também usam cores de pele, madeira e tons pastel para acompanhar a linguagem de cartoon da referência.

A narração masculina em português e a mixagem são as mesmas da versão anterior criada do zero: voz sintética Kokoro `pm_alex`, sem clonagem, trilha instrumental original discreta e assinatura sonora da marca no final. O roteiro, sua duração e o convite ao WhatsApp são preservados. A referência foi utilizada para a direção visual.

Entrega: `entregas/ib-midias-cartoon.mp4`, na raiz do repositório: MP4 H.264 + AAC, vertical 1080 × 1920, 30 fps, aproximadamente 57 segundos.

## Prévia reproduzível e exportação

Requer Node e Chromium em `/usr/bin/chromium`. As fontes, o áudio e os tempos já estão incluídos.

```bash
npm ci
npm run dev
npm run typecheck
npm run stills
npm run render
```

A composição se chama `Cartoon`. O MP4 sai em `out/ib-midias-cartoon.mp4`. Os estados principais dos 17 enquadramentos foram conferidos em imagens antes da renderização. `verification.json` registra a conferência de duração, quadros, legendas, áudio integral e decodificação do arquivo final.

As fontes acompanham suas licenças em `public/FONT-LICENSE.txt` e `public/STORY-FONT-LICENSE.txt`. O símbolo oficial é o já fornecido para a iB Mídias. Os arquivos `public/timeline.json`, `public/captions.json` e `public/mouth.json` contêm os tempos de cena, palavras e movimento de boca.
