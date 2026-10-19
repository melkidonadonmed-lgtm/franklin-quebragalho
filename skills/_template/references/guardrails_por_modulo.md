# Checklist Mestre Transversal e Guardrails por Módulo de Domínio (Padrão 2026)

Este documento é a **Fonte Única de Verdade (SSOT)** para critérios de aceite transversais e guardrails específicos por tipo de skill no ecossistema Franklin Quebra-Galho. Ao criar, evoluir ou auditar uma skill, carregue apenas o **Checklist Transversal (Parte 1)** e o **Módulo de Domínio correspondente (Parte 2)**, eliminando a duplicação de regras entre skills.

---

## 📋 Parte 1: Checklist Transversal de Aceite (Obrigatório para Qualquer Skill)

### 1. Metadados e Roteamento (*Triggering & Discovery* — Tier 1)
- [ ] **Formato `SKILL.md` Válido**: Localizado exatamente na raiz da pasta (`skills/<slug>/SKILL.md`), codificado em UTF-8 sem BOM.
- [ ] **Nome Padronizado (`name`)**: Até 64 caracteres, letras minúsculas, números e hífens simples (`^[a-z0-9]+(-[a-z0-9]+)*$`), coincidindo com o nome da pasta.
- [ ] **Descrição Calibrada (`description`)**: Redigida em 3ª pessoa ($\le 300$ chars recomendado, máx. 1024), declarando explicitamente **o que faz**, **quando ativar** (*gatilhos positivos*) e **quando NÃO usar** (*exclusões e near-misses*).
- [ ] **Bateria de Testes de Gatilho (`evals/evals.json`)**: Contém casos funcionais e matriz de roteamento (`should_trigger` com variações de fraseado/typos e `should_not_trigger` com *near-misses* de skills vizinhas; meta de produção: $\ge 10$ positivas e $\ge 10$ negativas com $\text{Trigger Rate} \ge 0.90$ e $\text{False Trigger Rate} \le 0.05$).

### 2. Governança da Janela de Contexto (*Progressive Disclosure* — Tier 2 & Tier 3)
- [ ] **Orçamento Estrito (`< 500` Linhas / `< 5.000` Tokens)**: O corpo do `SKILL.md` mantém apenas o fluxo decisório nuclear e instruções causais baseadas no *"Porquê"* (*Lean Instructions*), evitando listas redundantes em caixa-alta (*over-constraining*).
- [ ] **Modularidade em Subpastas (Tier 3)**: Tabelas extensas, schemas JSON/Pydantic, templates e scripts executáveis residem em `references/`, `rules/`, `scripts/` e `evals/`, carregados sob demanda.
- [ ] **Seção de Armadilhas (*Gotchas*)**: Explicita exceções reais, limitações de ferramentas e comportamentos contraintuitivos observados em execuções anteriores.

### 3. Execução Determinística e Contrato de Dados
- [ ] **Desacoplamento Cognitivo vs. Determinístico**: Planejamento e interpretação semântica ficam no LLM; cálculos matemáticos, transformações rígidas, hashes e parsers condicionais são delegados a scripts testados em `scripts/` ou tools MCP.
- [ ] **Validação com Tipagem Forte**: Entradas e parâmetros utilizam esquemas fortemente tipados (`Pydantic v2` com `ConfigDict(extra="forbid")` ou `JSON Schema 2020-12` com `additionalProperties: false`).
- [ ] **Erros Acionáveis (*Actionable Errors*)**: Falhas retornam mensagens estruturadas informando o parâmetro incorreto, o tipo/schema esperado e `recovery_hint` para autocorreção do agente.

### 4. Segurança e Defesa em Profundidade (*Zero-Trust*)
- [ ] **Zero Hardcode de Credenciais**: Chaves de API, tokens e senhas nunca constam em `SKILL.md`, schemas ou scripts; são injetados exclusivamente via variáveis de ambiente no runtime.
- [ ] **Isolamento Semântico por Tags XML (OWASP LLM01:2025/2026)**: Entradas externas e dados do usuário são delimitados por `<system_instructions>`, `<context>` e `<untrusted_user_input>`, tratados como dados passivos.
- [ ] **Portão Human-in-the-Loop (HITL) e `--dry-run`**: Operações destrutivas (exclusão, alteração de banco, envio externo, transações financeiras) exigem simulação prévia e confirmação explícita do usuário.

### 5. Qualidade de Código e Avaliação Sistemática (*Evals*)
- [ ] **Testes Unitários Independentes**: Scripts em `scripts/` possuem cobertura para caminho feliz, valores-limite (*boundary values*), entradas nulas/malformadas e exceções (`<= 300` linhas por arquivo).
- [ ] **Métricas Quantitativas ($\text{Pass}@k$ e $\text{TEI}$)**: Homologação empírica medindo $\text{Pass}@1$, $\text{Pass}@k$ não enviesado e o Índice de Eficiência de Tokens ($\text{TEI}$) frente ao baseline.

---

## 🛠️ Parte 2: Guardrails e Critérios Específicos por Módulo de Domínio

Selecione e aplique **apenas** os módulos correspondentes à natureza da skill:

### Módulo 1: Skills de Execução, Automação & Código (`Python / Go / TS / ADK / ReAct`)
- **Critério de Parada e Orçamento Explícitos**: Defina `max_steps` (ex.: `12`), `max_tool_calls` (ex.: `20`), `deadline_seconds` (ex.: `90`) e condições claras de parada (`stop_when`) para impedir loops infinitos.
- **Zero Prompts Interativos de Terminal**: Proibido usar `input()`, `Read-Host` bloqueante ou aguardar `stdin` sem flag não-interativa, evitando congelar o runtime do agente.
- **Separação Limpa `stdout` vs `stderr`**: Emita payloads finais estruturados (JSON/Markdown) em `stdout` e logs de diagnóstico/progresso exclusivamente em `stderr` (especialmente crítico em servidores MCP `stdio`).
- **Runtime e Dependências Desacoplados**: Não execute `pip install` ou `npm install` dinâmicos silenciosos durante a execução da tool; declare dependências no cabeçalho PEP 723 (`uv run`) ou no manifesto do ambiente.
- ❌ **Anti-Padrões**: Nunca usar raciocínio estocástico do LLM para aritmética ou parsing determinístico; nunca retornar `"Error"` genérico sem contexto de recuperação.

### Módulo 2: Skills de Design Visual & Arquitetura da Informação (`Layouts / Slides / Infográficos`)
- **Arquitetura da Informação Antes da Estética**: Estabeleça a mensagem central, a hierarquia lógica e a divisão funcional por blocos antes de prescrever cores ou estilos.
- **Regra Estrita da Densidade Visual**: Limite o texto em cartões, blocos ou slides ao **teto máximo de 35 palavras por bloco** e entre **6 a 10 blocos por tela/página**, evitando parágrafos longos dentro de containers visuais.
- **Zero Ornamentos Sem Função Semântica**: Todo ícone, vetor ou divisor deve cumprir função estrutural clara (indicar estado, fluxo, comparação ou agrupamento).

### Módulo 3: Skills de Frontend, UI & Arquitetura Visual por Propósito (`HTML5 / React / Tailwind / DESIGN.md / minimal-impact-ui`)
- **Seleção de Tema pelo Propósito do Projeto & Padrão `minimal-impact-ui` (Ex Umbris + WinUI 3 Gallery)**: Identifique o propósito do sistema (*Conversão/SaaS*, *Editorial*, *FinTech*, *IA Nativa/AETHER*, *MedTech* ou *DevTools/Terminal IBM*) antes de escolher o tema (*Cinza Monolítico `#57545d` + Menus `#8e8999`*, *Claro Editorial `#F3F3F5` Ad Lucem*, *Preto Terminal IBM `#070709` + `IBM Plex`* ou *AETHER 2027* `oklch()`). Detalhes em [`references/preferencias_estilo_e_temas.md`](preferencias_estilo_e_temas.md), [`../../minimal-impact-ui/SKILL.md`](../../minimal-impact-ui/SKILL.md) e no Atlas [`../../minimal-impact-ui/references/atlas_ex_umbris_winui.html`](../../minimal-impact-ui/references/atlas_ex_umbris_winui.html).
- **Nitidez Tipográfica Absoluta (Zero Letras Vermelhas Embaçadas sobre Cinza/Escuro)**: Proibido usar `color: #e13535` puro ou serifa fina embaçada sobre fundos cinza (`#57545d`, `#49464f`) ou pretos (`#070709`). Use `.highlight-surgical` (Semibold + sublinhado `2px` em `--punctual-accent`) em títulos e `.accent-text` (texto `#FFFFFF` no cinza/escuro ou `#991B1B` no claro + fundo `--punctual-soft` + `border-left: 2.5px solid var(--punctual-accent)`) em badges/tags. Em botões preenchidos Azul (`#35acd8`) ou Verde (`#10B981`), use texto escuro (`#091318` / `#062016`).
- **6 Arquétipos de Composição de Página (Além de Formulários e Gráficos) & 28 Efeitos WinUI 3**: Estruture aplicações ricas usando *Split-Screen Live Workbench*, *Timeline Cronológica*, *Kanban Operacional*, *Canvas de Nós / Árvore de Decisão*, *Wizard Modo Foco Anti-TDAH* ou *Catálogo WinUI Gallery*, combinados com `Expander` (revelação progressiva), `Command Palette (Ctrl+K)`, `Connected Animation`, `Compact Sizing` e `Viewbox A4`.
- **HTML5 Semântico, Prevenção de XSS (`AUDIT-SEC-01`), Acessibilidade (`AUDIT-A11Y-01/02`) e FSM (`AUDIT-STATE-01/02`)**: Contraste WCAG 2.1 AA/AAA, tinta escura `#16151A` sobre `#8e8999`, `font-variant-numeric: tabular-nums`, curvas físicas `cubic-bezier(0.16, 1, 0.3, 1)`, estados `idle | loading | error | pressed`, `@media (prefers-reduced-motion: reduce)` e `@media print` A4.
- **Espaçamento, Camadas Esculpidas & Isolamento de Acento (`AUDIT-VIS-01`)**: Respiro $\ge 25\%$ do canvas, Bento Grid assimétrico, sombra esculpida em 3 camadas + `1px` Rim Light (`--shadow-sculpted`), blocos de contraste alternados (`--bg-contrast-card`: `#232127` / `#18181C`) e proporção 98/2 (ou 60-30-10).

### Módulo 4: Skills de Investigação, Pesquisa & RAG (`Deep Research / Documentos / MemPalace`)
- **Memória Não é Fonte de Verdade**: Trate a memória do agente como cache contextual; valide dados transacionais, clínicos ou normativos diretamente na fonte primária autoritativa antes de decidir ou escrever.
- **Ancoragem Factual (*Closed-Domain Grounding*)**: Toda afirmação factual deve citar a fonte primária, arquivo ou trecho original; quando ausente, declarar explicitamente `[LACUNA: Dado não localizado na fonte]`.
- **Raciocínio Transparente de Descarte**: Explicite brevemente quais documentos ou resultados foram descartados por desatualização, baixa relevância ou conflito de versão.
- **Filtragem Contra *Context Poisoning***: Nunca despeje payloads brutos de APIs ou páginas inteiras na janela de contexto; filtre, sanitize contra *indirect prompt injection* e resuma antes da injeção.

### Módulo 5: Skills de Criação & Edição de Imagem (`Midjourney / DALL-E 3 / Imagen`)
- **Prompts Finais Estritamente em Inglês**: Produza o prompt técnico final integralmente em inglês.
- **Estrutura Obrigatória dos 8 Pilares Visuais**:
  1. *Subject & Action* (sujeito e ação detalhados);
  2. *Environment / Scenario* (ambiente, profundidade e atmosfera);
  3. *Lighting* (direção, temperatura e qualidade da luz);
  4. *Composition & Camera* (lente, ângulo e enquadramento);
  5. *Artistic Style & Render* (estilo visual e acabamento material com função estética real, sem jargões vazios como `"8K"` isolado);
  6. *Color Palette* (tons dominantes e acentos);
  7. *Technical Flags / Aspect Ratio* (ex.: `--ar 16:9 --v 6.1`);
  8. *Negative Constraints* (`--no text, watermark, signature, blur, low quality, deformed, oversaturated`).

### Módulo 6: Skills de Criação & Edição de Vídeo (`Sora / Veo / Runway / Kling`)
- **Prompts Finais Estritamente em Inglês**: Redija o prompt técnico final em inglês.
- **Unidade de Ação e Câmera por Tomada**: Limite cada plano a **1 ação dominante** e **1 movimento principal de câmera** (ex.: *slow dolly-in*, *orbital tracking shot*), proibindo misturar movimentos conflitantes na mesma tomada.
- **Progressão Temporal Explícita**: Nunca descreva o vídeo como imagem estática; especifique início, evolução temporal do movimento, física dos materiais/fluidos e continuidade de iluminação.

### Módulo 7: Skills de Saúde & Ajuda Clínica (`Discussão de Casos / Prescrição / Calculadoras`)
- **Anonimização Estrita (PII/PHI)**: Substitua nomes, prontuários, CPFs e datas identificáveis por marcadores genéricos (`[PACIENTE_A]`, `[IDADE]`).
- **Cadeia Causal Obrigatória em 4 Passos**:
  $$\text{1. Fisiopatologia} \longrightarrow \text{2. Apresentação Clínica} \longrightarrow \text{3. Exames Discriminantes} \longrightarrow \text{4. Conduta Terapêutica}$$
- **Prescrição Farmacológica nos 6 Pilares**: Toda menção a medicamentos deve explicitar obrigatoriamente: **(1) Fármaco (DCB)**, **(2) Dose exata** (e `mg/kg` em pediatria), **(3) Via de administração**, **(4) Frequência/Intervalo**, **(5) Duração do tratamento** e **(6) Contraindicações / Ajuste Renal ou Hepático**.
- **Ancoragem Normativa e Disclaimers**: Cite a diretriz vigente com **Instituição e Ano de publicação** (proibido fabricar referências) e inclua o aviso institucional de caráter educativo/suporte à decisão médica no início e ao final da entrega.
