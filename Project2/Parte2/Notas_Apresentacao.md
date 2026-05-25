# Guião de apresentação — TP2 Parte 2
**Christopher D. Manning (2022) — "Human Language Understanding & Reasoning"**
*Dædalus, 151(2): 127–138*

---

## SLIDE 2 · Sobre o autor · ⏱ 45s

**🎯 O que dizer:**
> "Manning é professor em Stanford, dirige o laboratório de IA de lá, foi presidente da ACL — a principal associação da área — e co-escreveu o *Foundations of Statistical NLP*, que foi um dos manuais que definiu o paradigma anterior ao deep learning. Escolhi este artigo precisamente por causa disto: não é um paper experimental, é um ensaio numa revista da Academia Americana de Artes e Ciências. Quando alguém com este percurso resume o estado da arte para um público não-técnico, vale a pena ouvir — ele faz três coisas: traça a história do NLP, explica a viragem recente, e discute se estes modelos compreendem mesmo."

**📌 Âncora:** secção "About the Author", p. 136.

**⚠️ Cuidado:** O percurso (Stanford, SAIL, ACL, livros) é do artigo. O "porquê escolhi este" é enquadramento teu — está perfeitamente bem dizê-lo como opinião, mas não o atribuas ao Manning.

---

## SLIDE 3 · A tese central · ⏱ 50s

**🎯 O que dizer:**
> "A tese está logo no resumo. Cito a ideia: a última década produziu avanços *dramáticos e surpreendentes* — o Manning sublinha 'surpreendentes' — através de redes neuronais simples, mas a uma escala enorme e treinadas com quantidades enormes de dados. E o que daí emergiu — BERT, GPT-3 — são, segundo ele, os primeiros indícios de uma forma mais geral de inteligência artificial. Três palavras-chave atravessam o ensaio inteiro: **escala**, **auto-supervisão** e **generalização**. Vou desenvolver cada uma."

**📌 Âncora:** abstract, p. 127.

**⚠️ Cuidado:** Os três chips (escala / auto-supervisão / generalização) são uma síntese minha para estruturar a apresentação — são fiéis ao artigo, mas a tripla não aparece formulada assim no texto. Não digas "o Manning identifica três pilares"; diz "podemos resumir em três ideias".

---

## SLIDE 4 · As quatro eras do NLP · ⏱ 75s

Este é um dos slides densos. Não te percas em datas — conta a *história*.

**🎯 O que dizer:**
> "O Manning organiza a história em quatro eras. **Primeira, 1950 a 69**: tradução automática rudimentar, dicionários e regras à mão, quase nada se sabia sobre a estrutura da língua. **Segunda, 1970 a 92**: sistemas baseados em regras, sofisticados mas todos construídos manualmente — o SHRDLU, o LUNAR. **Terceira, 1993 a 2012**: a viragem empírica — aparece texto digital em abundância, corpora anotados, machine learning estatístico. É a era do livro do próprio Manning. **Quarta, 2013 até hoje**: deep learning — Word2Vec, depois o Transformer em 2017, depois o BERT em 2018.
>
> E aqui está o ponto mais subtil do slide: o Manning argumenta que, *em retrospectiva*, a verdadeira ruptura não foi o deep learning em 2013 — foi a **auto-supervisão em larga escala** a partir de 2018. Ele chega a dizer que a terceira era talvez se devesse estender até 2017."

**📌 Âncora:** pp. 128–130. Eras: 128 (1ª e 2ª), 129 (3ª e 4ª), 130 (a observação revisionista, "in hindsight... the third era might be extended until 2017").

**⚠️ Cuidado:** O argumento revisionista é genuinamente do Manning e é o que distingue este ensaio de um resumo genérico — vale a pena enfatizá-lo. Se te perguntarem "porquê 2018 e não 2017?", a resposta está no slide seguinte.

---

## SLIDE 5 · A viragem de 2018 · ⏱ 60s

**🎯 O que dizer:**
> "Concretamente, o que mudou em 2018? Antes: aprendizagem supervisionada — precisavas de dados anotados à mão, um modelo por tarefa, pipelines complexas. Depois: o modelo aprende sozinho a partir de texto cru, biliões de palavras, e *um único modelo* serve muitas tarefas.
>
> O mecanismo é simples e está aqui em baixo: o modelo cria os seus próprios desafios — esconde uma palavra e tenta adivinhá-la, ou prevê a palavra seguinte. Aprende com o erro. Repete biliões de vezes. E disto **emerge** conhecimento sobre a língua e sobre o mundo, sem ninguém ter rotulado nada."

**📌 Âncora:** p. 129 ("Everything changed in 2018... the first major success of very large scale self-supervised neural network learning"); p. 130 (um modelo adaptável via fine-tuning ou prompting).

**⚠️ Cuidado:** Não confundas auto-supervisão com não-supervisionado. O Manning é cuidadoso: o modelo *cria os seus próprios rótulos* a partir do texto — não é "sem supervisão", é "supervisão gerada pelo próprio sinal". Se alguém perguntar a diferença, esta é a resposta.

---

## SLIDE 6 · Transformers & atenção · ⏱ 75s

O slide mais técnico. Não tentes ensinar transformers — explica a *intuição*.

**🎯 O que dizer:**
> "Não vou explicar transformers em detalhe, mas a ideia central é a **atenção**. Cada palavra calcula três vectores: uma *query*, uma *key* e um *value*. A query de uma palavra é comparada com as keys de todas as outras posições para decidir *quanto peso dar a cada uma* — daí o nome 'atenção'. Depois faz-se uma média ponderada dos values, e isso dá uma nova representação da palavra que já tem em conta o contexto.
>
> Isto repete-se em camadas — o BERT tem 12 — e biliões de vezes durante o treino. No exemplo do próprio artigo, o modelo consegue prever que a palavra escondida entre 'Judiciary' e 'Annual Report' é 'committee'. Para nós, aqui em SPLN, o ponto prático é: é esta a arquitectura por baixo do BERT que vamos usar no QA extractivo da Parte 1 do trabalho."

**📌 Âncora:** pp. 130–131. Q/K/V e atenção: p. 130. Figura 1 e o exemplo "committee": p. 131.

**⚠️ Cuidado:** A ligação ao TP2 Parte 1 é enquadramento teu, não do Manning — mas é um gancho legítimo e bom para a turma. Diz "para nós" / "no nosso trabalho", deixando claro que é a tua leitura, não uma afirmação do artigo. Se alguém pedir mais detalhe sobre Q/K/V, não inventes matemática — remete para o paper original (Vaswani et al., 2017, "Attention is all you need", que está na nota 7).

---

## SLIDE 7 · Aplicações · ⏱ 70s

**🎯 O que dizer:**
> "O Manning dá três aplicações onde isto já funciona. **Tradução automática**: o Google Translate passou a transformer em 2020 — em vez de sistemas par-a-par entre línguas, um único modelo treinado em todas as línguas em simultâneo, com um token a indicar a língua de entrada. **Question Answering**: aparece o UnifiedQA, um modelo que responde a vários formatos de pergunta sem treino específico para cada um — e isto é exactamente o paradigma da Parte 1 do nosso TP2. **Sumarização clínica**: gerar a 'impressão' de um relatório de radiologia a partir das observações — e aqui o Manning chama a atenção para um problema que não é fluência mas **correcção factual**."

**📌 Âncora:** pp. 132–133. Tradução: 132. QA (exemplo do Samsung Galaxy): 133. Radiologia: 133–134.

**⚠️ Cuidado:** Se te pedirem o exemplo concreto do QA, está no artigo: o modelo responde a perguntas sobre o Samsung Galaxy Note 20 Ultra ("How expensive is it?" → "$1,300 for the 128GB version"; "20x optical zoom?" → "no"). Tê-lo na manga mostra que leste o artigo a sério.

---

## SLIDE 8 · Foundation models · ⏱ 55s

**🎯 O que dizer:**
> "O conceito de **foundation models** foi proposto pelo grupo de Stanford em 2021, e o Manning é um dos autores. A definição: modelos com milhões — hoje biliões — de parâmetros, treinados em massa via auto-supervisão, e facilmente adaptáveis a inúmeras tarefas. E o conceito está a expandir-se em três frentes: **linguagem**, que já está estabelecida; **multimodal** — texto e imagem aprendidos em conjunto, modelos tipo DALL·E que produzem uma imagem a partir de texto; e **outros domínios** — visão, robótica, bioinformática, grafos de conhecimento."

**📌 Âncora:** p. 135. Definição e referência (Bommasani et al., 2021, nota 19). DALL·E como exemplo multimodal: p. 135.

**⚠️ Cuidado:** "Foundation models" é o termo que o próprio Manning ajudou a cunhar — vale a pena dizer isso, dá peso. Não confundas com "fundação" no sentido de organização; é "modelo-fundação", a base sobre a qual se constrói.

---

## SLIDE 9 · Mas... entendem mesmo? · ⏱ 75s

O coração filosófico. Não corras este slide.

**🎯 O que dizer:**
> "E chegamos à pergunta mais interessante: *estes modelos compreendem mesmo a linguagem?* Há duas posições. **Os cépticos** — e o Manning aponta para o Bender e o Koller, num artigo famoso de 2020 — defendem uma semântica denotacional: o significado é a ligação ao mundo real, a objectos e situações. Como os modelos só vêem texto, não há verdadeira compreensão, só padrões.
>
> **O Manning discorda.** Para ele, o significado não é tudo-ou-nada — emerge da *rede densa de conexões* entre uma palavra e outras coisas, sejam objectos ou outras palavras. E dá um exemplo óptimo: a palavra *shehnai*, um instrumento indiano. Mesmo que eu nunca tenha visto um, se me disserem 'é como um oboé tradicional indiano', já tenho *algum* significado — conexões à Índia, a instrumentos de palheta, a música. O significado constrói-se por camadas. A conclusão dele é forte: com esta definição, *não há dúvida* de que os modelos pré-treinados aprendem significados — embora incompletos."

**📌 Âncora:** pp. 134–135. Semântica denotacional vs distribucional: 134. Bender & Koller: nota 17. Exemplo do shehnai: 134–135. "There can be no doubt that pretrained language models learn meanings": 135.

**⚠️ Cuidado:** É uma distinção subtil — o Manning **não** está a dizer que os modelos compreendem como os humanos. Está a dizer que o nosso próprio conceito de "compreender" é gradual, e que por essa medida os modelos têm *alguma* compreensão genuína. Se simplificares para "o Manning acha que os modelos entendem como nós", estás a deturpar o argumento. Esta é a armadilha mais fácil de cair na discussão.

---

## SLIDE 10 · Limitações e riscos · ⏱ 50s

**🎯 O que dizer:**
> "O Manning não é um evangelizador — fecha com cautelas claras. **Concentração de poder**: só algumas organizações têm recursos para treinar estes modelos. **Biases**: quem usa, herda os preconceitos do corpus de treino. **Segurança opaca**: é difícil saber se um modelo é seguro num contexto, porque é grande demais para inspeccionar. E o mais importante: **raciocínio limitado** — mesmo os melhores modelos ainda falham em raciocínio lógico e causal cuidadoso. A frase que resume tudo: estes modelos *sabem* muito, mas ainda *raciocinam* pouco."

**📌 Âncora:** pp. 135–136. Riscos da convergência: 136. "Lacking a human-level ability for careful logical or causal reasoning": 136.

**⚠️ Cuidado:** "Sabem muito, raciocinam pouco" é uma formulação minha que condensa o argumento — é fiel, mas se quiseres ser rigorosa diz "por outras palavras" antes. O ponto do *reasoning* liga-se ao título do ensaio (*Understanding & Reasoning*): a compreensão avançou muito, o raciocínio nem por isso.

---

## SLIDE 11 · Em três frases · ⏱ 40s

**🎯 O que dizer:**
> "Para terminar, em três frases. **Um**: a história do NLP teve quatro eras, e a quarta ainda está a começar — a ruptura real foi a auto-supervisão, não o deep learning em si. **Dois**: os foundation models são a forma como vamos ter os primeiros vislumbres de uma IA mais geral — um modelo, treinado uma vez, adaptado a inúmeras tarefas, incluindo multimodais. **Três**: mas 'compreensão' continua a ser um conceito disputado, e o raciocínio é o calcanhar de Aquiles. E os riscos sociais são reais. Obrigada — fico aberta a perguntas."

**📌 Âncora:** frase de encerramento do artigo, p. 136 ("they will give people in the coming decade their first glimpses of a more general form of artificial intelligence").

---

## PERGUNTAS PROVÁVEIS NA DISCUSSÃO — e como responder

**"Como liga este ensaio ao nosso TP2?"**
> A Parte 1 é literalmente um sistema de QA com retriever — exactamente o paradigma do UnifiedQA que o Manning descreve no slide 7. O QA extractivo usa um BERT (a arquitectura do slide 6); o abstractivo é prompting a um LLM (a capacidade de generalização do slide 3).

**"Concordas mais com Bender ou com Manning?"**
> (É uma pergunta de opinião — podes responder, mas mantém-te factual sobre as posições.) O argumento do Manning é que o conceito de compreensão é gradual; o de Bender é que sem referência ao mundo não há semântica. Uma resposta segura: depende do que se entende por "compreender" — e é precisamente esse o ponto em disputa, não há consenso na área.

**"O artigo é de 2022. O que mudou desde então?"**
> O Manning não podia prever a explosão dos LLMs conversacionais nem o salto em capacidades de raciocínio (chain-of-thought, modelos de raciocínio). A previsão dele sobre "convergência num pequeno número de foundation models" confirmou-se largamente. A limitação do raciocínio que ele aponta foi parcialmente atacada depois — mas continua a ser debatida.

**"Porquê 2018 e não o Transformer de 2017?"**
> Porque o Transformer (2017) é a *arquitectura*; a viragem (2018, BERT) foi aplicá-la em auto-supervisão a escala massiva. O Manning é explícito: a arquitectura sozinha não foi a ruptura, foi o paradigma de treino.

**"O que é exactamente um foundation model?"**
> Modelo grande, treinado uma vez via auto-supervisão em dados gerais, depois adaptado a muitas tarefas via fine-tuning ou prompting. BERT e GPT-3 são os primeiros exemplos. Termo cunhado pelo grupo de Stanford (do qual o Manning faz parte) em 2021.

