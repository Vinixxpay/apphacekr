# iB Mídias — Reels animado de projetos de maior valor

Projeto editável em Remotion + React + SVG, construído a partir do briefing enviado. Formato 1080 × 1920, 30 fps, MP4 H.264 + AAC. A duração medida é de 64,4 segundos, dentro do alvo de 60 a 75 segundos.

A direção visual segue a orientação escrita de cartoon 2D. A referência anexada foi utilizada para ritmo, mudanças de enquadramento e linguagem narrativa. Os desenhos são originais e mantêm a aparência do profissional brasileiro de vidros e esquadrias, com uniforme azul, ferramentas e expressões que vão do cansaço à confiança.

## O que está incluído

- Sete cenas animadas e roteiro completo do briefing, com tempos ajustados à duração real da fala.
- Personagem correndo entre demandas, ferramentas em movimento e telefone tocando.
- Quatro clientes, relógio acelerado e contraste entre trabalho, dinheiro e despesas.
- Congelamento da ação e balança animada comparando quatro serviços pequenos com um projeto maior, como hipótese e sem preços inventados.
- Atendimento a serviços pequenos, projeto premium, cuidado e valorização do acabamento.
- Pesquisa no celular, anúncio e conversa de WhatsApp claramente ilustrativa.
- Jornada Anúncio → Cliente interessado → WhatsApp → Orçamento → Negociação.
- Distinção entre anúncios e oportunidades pela iB Mídias e atendimento e fechamento pela empresa.
- CTA, símbolo oficial animado e encerramento legível.
- Narração masculina em português brasileiro, trilha instrumental original discreta e 26 eventos sonoros sincronizados de telefone, ferramentas, dinheiro, relógio, notificações e interface.

A voz é sintética, gerada localmente com Kokoro `pm_alex`; não é clonagem. O texto completo é preservado, inclusive o convite final. A comparação de serviços é apresentada como possibilidade, sem garantia de faturamento. Os pedidos de orçamento são exemplos visuais, não depoimentos ou resultados de clientes reais.

## Abrir e renderizar

Requer Node, FFmpeg e Chromium em `/usr/bin/chromium`.

```bash
npm ci
npm run dev
npm run typecheck
npm run stills
npm run render
```

A composição se chama `ReelsProjetos`. O resultado sai em `out/ib-midias-reels-projetos.mp4`. A narração, a trilha e os efeitos já estão incluídos; não é preciso instalar modelos de voz para renderizar o projeto.

## Ajustar o conteúdo

- `briefing.md`: solicitação completa enviada pelo usuário.
- `roteiro.json`: narração de cada cena. “i bê” é apenas a grafia de pronúncia para a síntese; a legenda mostra iB Mídias.
- `timeline.json` e `public/timeline.json`: duração e início de cada cena.
- `public/captions.json`: palavras e tempos das legendas.
- `src/Drawings.tsx`: personagem, cenários, produtos, ferramentas e celular.
- `src/Film.tsx`: ações, balança, jornada, títulos, transições e CTA.
- `sound-events.json` e `scripts/effects.py`: sons e momentos de entrada.

Para gerar novamente a narração com Python e uv:

```bash
bash scripts/setup-voice.sh
```

O modelo é obtido da distribuição https://github.com/thewh1teagle/kokoro-onnx, com vozes de https://huggingface.co/hexgrad/Kokoro-82M, sem inclusão dos pesos no pacote. O script também regenera a sincronização de palavras, os valores de boca por quadro e os efeitos sonoros.

Fontes e licenças: `public/FONT-LICENSE.txt`. O símbolo é o oficial já fornecido pelo usuário. A trilha e os efeitos foram sintetizados para este projeto.

`verification.json` registra resolução, quadros, duração, integridade da narração, ajuste dos textos e decodificação completa da entrega. `speech-review.json` registra a conferência da narração em português.
