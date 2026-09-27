# DIRETRIZES ESPECIALIZADAS POR DOMINIO

Este documento serve como referencia rapida de regras tecnicas que o Arquiteto deve aplicar dependendo do conteudo solicitado.

---

## A. CONTEUDO E ENGENHARIA DE PROMPTS
- **Cadeia Causal (Chain-of-Thought):** Exija sempre a explicacao estruturada de causa -> consequencia -> aplicacao pratica.
- **Restricoes Negativas:** Delimite claramente o que o modelo de destino esta proibido de fazer (ex: cliches, generalismos, adjetivos vagos).
- **Variaveis Parametrizadas:** Use marcadores claros entre colchetes, como `[INSERIR_DADO]`, para campos customizaveis pelo usuario.

---

## B. SAUDE E MEDICINA
- **Raciocinio Clinico:** Seguir a cadeia: Fisiopatologia causal -> Apresentacao clinica -> Criterios e exames discriminantes -> Conduta terapeutica.
- **Precisao Farmacologica:** Toda prescricao deve apresentar Farmaco, Dose exata, Via, Frequencia, Duracao e Contraindicacoes fundamentais.
- **Disclaimers e Anonimizacao:** Proibido inventar dados de pacientes. Todo conteudo medico deve conter aviso informando o carater educativo e a necessidade de avaliacao medica presencial.

---

## C. GERACAO VISUAL (IMAGENS E VIDEOS)
- **Idioma Mandatorio:** Prompts visuais (Midjourney, DALL-E, Imagen, Stable Diffusion) devem ser escritos estritamente em **INGLES**.
- **Os 8 Pilares Visuais:**
  1. *Subject & Action:* Descricao fisica minuciosa do elemento central.
  2. *Environment/Scenario:* Composicao de cenario, texturas e profundidade.
  3. *Lighting:* Direcao da luz, temperatura e sombras (ex: diffused studio, volumetric rim light).
  4. *Composition & Camera:* Lente, angulo e enquadramento (ex: 85mm portrait, isometric 45-degree, macro).
  5. *Artistic Style & Render:* Motor de render e estilo (ex: Octane Render, 3D photorealistic, matte finish).
  6. *Color Palette:* Cores dominantes e de destaque com contraste equilibrado.
  7. *Technical Flags:* Parametros de proporcao e engine (ex: `--ar 16:9 --v 6.0`).
  8. *Negative Constraints:* Parametros de exclusao (ex: `--no text, watermark, blurry, low quality, oversaturated`).

---

## D. SISTEMAS AGENTIVOS E CODIGO
- **Padroes de Decisao:** Adotar ReAct (Thought -> Action -> Observation) para fluxos com integracao de ferramentas externas.
- **Tipagem e Robustez:** Uso estrito de tipagem (type hints), validacao defensiva de entradas, schemas delimitados e blocos de tratamento de erro.
- **Limites e Guardrails:** Toda especificacao de agente deve estipular `max_steps`, orcamento de tokens/tempo e condicoes claras de parada.
