# iB Mídias — projetos de maior valor

Anúncio criado do zero para profissionais de vidros, portões de alumínio e esquadrias, com narração masculina sintética em português brasileiro, ilustrações SVG em perspectiva, tipografia cinética, gráficos e legendas palavra por palavra.

A adaptação mantém a ideia do roteiro: agenda cheia não significa retorno proporcional; atrair também quem valoriza projetos maiores, sem abandonar os serviços pequenos; apresentar a estratégia da iB Mídias e levar a conversa ao WhatsApp. A comparação de quatro serviços com um projeto maior é apresentada como uma hipótese, sem resultados, preços ou depoimentos inventados.

O vídeo tem aproximadamente 57 segundos, em 1080 × 1920, 30 fps, MP4 H.264 + AAC. São oito cenas com cores #0131CD, #FFFFFF e #B9FC01, o símbolo oficial e uma chamada final legível. A voz foi gerada localmente com Kokoro, voz masculina brasileira `pm_alex`, velocidade nativa 1,06; não é uma gravação humana nem clonagem da voz do usuário. Há uma cama instrumental original discreta e a assinatura sonora da marca após a última frase.

`roteiro.json` contém a adaptação; `timeline.json` contém os tempos medidos; `public/captions.json` contém as palavras sincronizadas. A fala foi conferida com reconhecimento em português em cada cena; `speech-review.json` registra a revisão, incluindo uma diferença de reconhecimento de “valha”, sem alteração do texto falado ou criação de resultados.

As prévias das oito cenas foram renderizadas e conferidas antes da exportação. O render final é verificado por resolução, duração, quadros, decodificação integral, presença da faixa de áudio e correlação com a mixagem do projeto.

## Prévia e exportação

Requer Node, FFmpeg e Chromium em `/usr/bin/chromium`.

```bash
npm ci
npm run dev
npm run typecheck
npm run stills
npm run render
```

A composição é `AltoValor`. O MP4 sai em `out/ib-midias-alto-valor.mp4`. O áudio e os tempos já gerados estão incluídos; não é necessário refazer a síntese para renderizar o projeto.

Para regenerar a narração, o ambiente precisa de Python, uv e FFmpeg:

```bash
bash scripts/setup-voice.sh
```

Os pesos são obtidos da distribuição Kokoro ONNX, em https://github.com/thewh1teagle/kokoro-onnx, com vozes do modelo https://huggingface.co/hexgrad/Kokoro-82M. Eles não são incluídos no repositório. A fonte Montserrat acompanha sua licença em `public/FONT-LICENSE.txt`. O símbolo oficial vem do material já fornecido pelo usuário. A trilha e a assinatura sonora são sintetizadas para os vídeos da iB Mídias.
