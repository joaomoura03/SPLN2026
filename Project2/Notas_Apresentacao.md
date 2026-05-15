# Guia de apresentação — TP2 Parte 2
**Manning (2022) · "Human Language Understanding & Reasoning"**


## Slide 1 · Capa (~30s)

Boa tarde. Vou apresentar o ensaio do **Christopher Manning** publicado na *Dædalus* em 2022, intitulado **"Human Language Understanding & Reasoning"**.

Não é um paper experimental — é um ensaio reflexivo, escrito por uma das figuras-chave do NLP, e que faz três coisas em paralelo: traça a história do campo, explica a viragem dos foundation models, e discute filosoficamente se estes modelos compreendem mesmo a linguagem.

---

## Slide 2 · Sobre o autor (~50s)

Manning é professor em Stanford, dirige o Stanford AI Lab, foi presidente da ACL. É co-autor do livro *Foundations of Statistical NLP* — basicamente um dos manuais que estabeleceu o paradigma anterior.

A razão pela qual escolhi este artigo é precisamente esta: quando alguém com este percurso escreve um ensaio numa revista da Academia Americana de Artes e Ciências — não num venue técnico — vale a pena ouvir. Ele resume aquilo que a comunidade vê como sendo o estado da arte e o futuro.

---

## Slide 3 · A tese central (~50s)

A tese principal está aqui: a última década produziu avanços dramáticos e *surpreendentes* — Manning insiste nessa palavra — através de redes neuronais simples, mas a uma escala enorme.

E o que daí emergiu — BERT, GPT-3 — são, segundo ele, os primeiros indícios de uma forma mais geral de inteligência artificial: os **foundation models**.

Três palavras-chave guiam o ensaio: **escala**, **auto-supervisão** e **generalização**. Vou desenvolver cada uma.

---

## Slide 4 · As quatro eras do NLP (~70s)

Manning organiza a história em quatro eras:

- **1950–1969**: tradução automática rudimentar, com dicionários e regras morfológicas. Pouquíssimo conhecimento sobre a estrutura da língua.
- **1970–1992**: sistemas baseados em regras, todos feitos à mão — SHRDLU, LUNAR. Inteligentes mas frágeis.
- **1993–2012**: a viragem empírica. Aparecem corpora anotados, treebanks, ML estatístico. É a era em que o livro do Manning foi escrito.
- **2013 em diante**: deep learning. Word2Vec, depois Transformer em 2017, depois BERT em 2018.

**Aqui está a tese revisionista:** Manning argumenta que, em retrospectiva, a verdadeira ruptura não foi o deep learning em 2013 — foi a auto-supervisão massiva a partir de 2018. É um detalhe importante.

---

## Slide 5 · A viragem de 2018 (~60s)

Concretamente, o que mudou?

Antes: aprendizagem supervisionada, com recursos anotados à mão, um modelo por tarefa, pipelines complexas.

Depois: o modelo aprende sozinho a partir de texto cru, biliões de palavras, e *um único modelo* serve muitas tarefas.

A mecânica é simples: o modelo cria os seus próprios desafios — esconde uma palavra, tenta adivinhá-la, aprende com o erro. Repete isto biliões de vezes. E disso emerge conhecimento geral sobre língua e sobre o mundo.

---

## Slide 6 · Transformers & atenção (~70s)

Não posso explicar transformers em 1 minuto, mas a ideia essencial é esta: cada palavra calcula três vectores — **query, key, value**.

A query é comparada com as keys de todas as outras posições para decidir *quanto peso dar a cada uma*. Depois faz uma combinação ponderada dos values.

Isto repete-se em camadas (BERT tem 12) e biliões de vezes em treino. No exemplo do artigo, o modelo consegue prever que a palavra mascarada entre "Judiciary" e "Annual Report" é "committee".

Para nós aqui em SPLN o ponto é: é exactamente esta arquitectura que está por baixo do BERT que vamos usar para o QA extractivo na Parte 1 do trabalho.

---

## Slide 7 · Aplicações (~70s)

Três aplicações que Manning destaca:

1. **Tradução automática** — Google Translate passou a transformer em 2020. Um único modelo treinado em todas as línguas em simultâneo, com um token a indicar a língua de entrada. A qualidade está próxima do humano.

2. **Question Answering** — aparece o UnifiedQA, um modelo que lida com vários formatos de pergunta sem treino específico para cada um. Curiosamente, é exactamente o paradigma que estamos a implementar na Parte 1 do nosso TP2.

3. **Sumarização clínica** — gerar a "impressão" de um relatório de radiologia. Aqui Manning chama a atenção para o problema da *correcção factual*, não basta ser fluente.

---

## Slide 8 · Foundation models (~60s)

O conceito de **foundation models** foi proposto pelo grupo de Stanford em 2021, e Manning é um dos autores.

A definição: modelos com milhões — agora biliões — de parâmetros, treinados em massa via auto-supervisão, e que podem ser facilmente adaptados a inúmeras tarefas.

E o conceito está a expandir-se em três frentes: linguagem (já estabelecida), multimodal (texto + imagem, com modelos tipo DALL·E), e outros domínios — visão, robótica, bioinformática.

---

## Slide 9 · Mas... entendem mesmo? (~70s)

E aqui chegamos à parte filosoficamente mais interessante. *Estes modelos compreendem mesmo a linguagem?*

**Os cépticos** — Emily Bender e Alexander Koller, num paper famoso de 2020 — dizem que não. Defendem uma semântica denotacional: o significado é a ligação ao mundo, a objectos reais. Como os modelos só vêem texto, sem ligação a referentes, são apenas máquinas de padrões.

**Manning discorda.** Para ele, o significado emerge da rede de conexões — entre palavras, entre palavras e objectos. Não é tudo-ou-nada. Se um modelo tem uma rede rica de conexões, então tem alguma compreensão real. Incompleta, sim, mas genuína.

É um argumento subtil — não é dizer que os modelos compreendem como nós, é dizer que o nosso conceito de compreensão é ele próprio gradual.

---

## Slide 10 · Limitações e riscos (~50s)

Manning não é evangelizador. Fecha o ensaio com cautelas claras:

- **Concentração de poder**: só algumas organizações treinam estes modelos.
- **Biases**: quem usa, herda os preconceitos do corpus.
- **Segurança opaca**: difícil saber se um modelo é seguro num contexto específico.
- **Raciocínio limitado**: continuam a falhar em raciocínio lógico e causal cuidadoso.

Este último ponto é central — *sabem* muito, *raciocinam* pouco.

---

## Slide 11 · Em três frases (~40s)

Resumindo:

1. A história do NLP teve quatro eras, e a quarta ainda está a começar. A ruptura real foi a auto-supervisão, não o deep learning.

2. Foundation models são a forma pela qual vamos ter os primeiros vislumbres de IA mais geral — um modelo, muitas tarefas.

3. Mas "compreensão" continua a ser um conceito disputado, e o raciocínio é o calcanhar de Aquiles. Os modelos sabem muito; ainda raciocinam pouco. E os riscos sociais são reais.

Obrigada. Abertos a discussão.

---

## Possíveis perguntas para discussão

- Como liga este ensaio ao trabalho que estamos a fazer no TP2 Parte 1 (RAG, QA)?
- Concordas mais com Bender ou com Manning sobre o que é compreender?
- Em 2026, achas que Manning estava certo sobre a "convergência num pequeno número de foundation models"?
- O que o Manning não previu em 2022 que aconteceu depois?
