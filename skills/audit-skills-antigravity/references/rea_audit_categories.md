# Arquitetura de Auditoria em Dupla Camada, Matriz Cognitivo-Discriminativa e 6 Categorias (`audit-skills-antigravity` `v2.3.0`)

## 0. Conformidade Oficial `AgentSkills` (`agentskills.io`) & `Antigravity` (`antigravity.google/docs`)

1. **Estrutura e *Progressive Disclosure* em 3 Estágios:**
   - **L1 (Startup ~100 tokens):** `name` (`<= 64` chars kebab-case idêntico à pasta) + `description` (`<= 1024` chars na spec aberta; orçamento canônico local `<= 240` chars com cláusula positiva e negativa). Campos opcionais: `license`, `compatibility` (`<= 500` chars), `metadata`, `allowed-tools`.
   - **L2 (Ativação `SKILL.md`):** Único arquivo obrigatório na pasta `skills/<slug>/`; teto `<= 500` linhas e `<= 1.200` tokens sem repetir regras gerais do `AGENTS.md`.
   - **L3 (Sob Demanda):** `scripts/`, `references/`, `rules/`, `evals/`, `assets/` carregados apenas quando acionados pelo fluxo.
2. **Descontinuação de Workflows Legados:** `.agents/workflows/*.md` é depreciado no Antigravity 2.12+ em favor de `skills/<name>/SKILL.md` (`/migrate-workflows`). Regras globais/locais em `.agents/rules/*.md` ou `~/.gemini/config/rules/*.md` exigem YAML frontmatter (`trigger: always_on | model_decision | glob | manual`, limite `24 KB`/arquivo e `20.000` tokens agregados).

---

## 1. Camada 1: Engenharia Reversa REA, Sintaxe, Ambiente, Rotas e Regras Opostas

1. **Sintaxe e Integridade de Artefatos (`Syntax & AST Check`):**
   - Valida YAML frontmatter (`name <= 64`, `description`, `compatibility <= 500`, `version`, `updated_at`), sintaxe JSON (`evals/evals.json`, `references/*.json`) e integridade de scripts (`scripts/*.py`, `*.go`, `*.js`, `*.ts`), reprovando chamadas bloqueantes (`input()`) ou JSON/AST corrompido.
2. **Integridade de Referências, Nomes de Arquivos e Ambiente (`Reference & Environment Sanity`):**
   - Verifica se todos os links Markdown relativos `` `[label](caminho)` `` e caminhos citados (`scripts/...`, `references/...`, `rules/...`, `evals/...`) apontam para arquivos existentes no disco (bloqueando links fantasmas ou `.agents/workflows/` legado).
   - Verifica compatibilidade dos caminhos e nomes de arquivos com o ambiente operacional (`Windows 11 / pwsh` e POSIX, vedando caracteres inválidos `<>:"|?*`).
3. **Colisões entre Rotas, Nomes e Gatilhos (`Route & Trigger Collision`):**
   - Detecta duplicidade de `name`, colisão de nomes de scripts/rotas MCP exportadas e sobreposição excessiva de gatilhos Nível 1 (`description`) entre skills distintas do mesmo catálogo (`Overlap >= 80%`).
4. **Detecção de Regras Incompatíveis ou Opostas (`Contradictory Rules`):**
   - Reprova skills com instruções mutuamente exclusivas no mesmo fluxo (ex.: declarar operação *somente leitura / read-only* e simultaneamente instruir deleção/sobrescrita sem portão `HITL`, ou proibir e exigir o mesmo comando).

---

## 2. Camada 2: Processamento Cognitivo-Discriminativo e Anti-Homogeneização

### 2.1 Cadeia de Coerência Semântica de 8 Elos (`Cognitive Coherence Score: 0..100`)

1. **`Nome` (`name`)**: Kebab-case estrito refletindo o domínio real da skill.
2. **`Descrição & Gatilhos de Ativação` (`description`)**: Fronteira positiva (`Use para...`) e negativa (`Não use para...`) alinhadas ao propósito.
3. **`Objetivo & Função` (Seção 1)**: Define o problema exato que a skill resolve sem jargão genérico.
4. **`Estrutura & Entradas` (Seção 2)**: Parâmetros e pré-requisitos determinísticos.
5. **`Comandos & Processamento` (Seção 3)**: Passos executáveis e verificáveis que cumprem o que a descrição promete (*Does What It Says*).
6. **`Referências` (`references/` / `rules/`)**: Arquivos de apoio existentes e pertinentes ao domínio.
7. **`Ferramentas & Uso Real` (`allowed-tools` $\leftrightarrow$ Fluxo)**: Coerência entre as ferramentas declaradas e as ações exigidas no corpo.
8. **`Saídas & Guardrails` (Seções 4 e 5)**: Entregáveis verificáveis e limites operacionais claros.

### 2.2 Filtro Anti-Homogeneização (`Cross-Domain Contamination`)

Impede que skills de domínios não-visuais herdem regras genéricas de UI/CSS por cópia de template:
- Skills dos arquétipos `PLANNING`, `CODE_SECURITY_AUDIT` (exceto auditores de UI) e `STORAGE_OPS_DOCS` **não podem** exigir tokens visuais exclusivos de frontend (`oklch(`, `60-30-10`, `--shadow-elevation-`, `@container`), preservando a especificidade de cada domínio.

### 2.3 Matriz Discriminativa por Arquétipo de Domínio (*Does What It Says*)

| Arquétipo | Critérios Obrigatórios de Domínio e Ferramentas Reais | Falha Lógica / Reprovação Típica |
| :--- | :--- | :--- |
| **`PLANNING`** (`high-level-context-planner`, `skill-orquestrador-planos-encadeados`, `arquiteto-conteudo-solucoes`, `organizador-projetos-ideias`, `organizador-fluxo-arvore-arquivos`, `refine-prompt`, `context-sentinel`) | Deve conter os **6 fatores-chave de um plano de qualidade**: **(1)** divisão/decomposição em fases ou ondas, **(2)** estrutura/hierarquia, **(3)** coerência lógica/dependências (DAG/Kahn/causalidade), **(4)** gestão de ambiguidade (`[LACUNA]`, clarificação, perguntas guiadas), **(5)** descrição dos processos e **(6)** guardrails de segurança (`max_steps`, `HITL`, limites). | Prometer planejamento/arquitetura sem tratar ambiguidade (`[LACUNA]`), sem decomposição lógica ou sem critério de verificação. |
| **`E2E_UI_AUDIT`** (`frontend-testing-auditor`, `frontend-ui-ux-auditor`, `complex-zero`, `plan-uiux`, `auditoria-projetos-sistema`) | Deve exigir e acionar ferramentas reais de inspeção/interação de UI/E2E: `click`/interação, `a11y`/`WAI-ARIA`/contraste, `take_snapshot`/`take_screenshot`/`DOM`, `agent-browser`/`@eX`, `chrome-devtools` ou scripts verificadores (`audit_tactile_ui.py`, `ui_ux_frontend_auditor.py`, `complex_zero_ast_auditor.py`). | **Falsa Capacidade (`Tool-Objective Mismatch`)**: Skill de auditoria E2E/UI que não usa ferramentas reais de clique, DOM ou acessibilidade (`a11y`). |
| **`UI_DESIGN`** (`design-md`, `frontend-code-architect`, `design-interface-medica-minimalista`) | Deve especificar contratos visuais (`OKLCH`, escala tipográfica, espaçamento, estados finitos `FSM` ou grid clínico `.sus-grid`) e entregáveis verificáveis. | Instruções visuais subjetivas ("faça bonito/moderno") sem tokens ou medidas determinísticas. |
| **`CODE_SECURITY_AUDIT`** (`code-acceptability-auditor`, `test-quality-auditor`, `agent-server-auditor`, `audit-skills-antigravity`, `re-a-ndroid`, `code-quality-audit-3d-physics`, `android-agy-projects`, `gap-analyzer-auditor`) | Deve exigir inspeção técnica real via AST, binário/REA, ADB, suíte de testes (`Pass@k`), invariantes físicas 3D ou logs/traces RCA (`[FATO]` vs `[INFERÊNCIA]`). | Auditoria puramente opinativa sem parser/AST/script/evidência determinística. |
| **`STORAGE_OPS_DOCS`** (`gdrive-auditoria-limpeza`, `gdrive-taxonomia-organizacao`, `manutencao-disco-windows`, `curadoria-obsidian-vault`, `redator-tecnico-markdown`, `conversor-html-pdf`) | Deve exigir salvaguardas operacionais do domínio (`Dry-run`/SHA-256 antes de mover/remover arquivos, frontmatter/`[[Wikilinks]]` no Vault, Edge headless/CSS `@page` para PDF). | Operação de arquivos sem `Dry-run`/confirmação humana ou contaminação por regras de outro domínio. |

---

## 3. Fórmulas Matemáticas e As 6 Categorias de Ação

- **Estimador Não Enviesado $\text{Pass}@k$ (Chen et al.):**
  $$\text{Pass}@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$$
- **Taxa de Falsos Negativos ($\text{FNR}$):**
  $$\text{FNR} = \frac{\text{FN}}{\text{TP} + \text{FN}}$$

### As 6 Categorias Canônicas de Decisão

1. **`[MANTIDA]` / `[RECOMENDAÇÃO: MANTER]`**: YAML válido, `0` referências quebradas, `0` colisões de rota/gatilho, `CognitiveCoherenceScore >= 80`, `<= 10` regras e $\text{Pass}@3 \ge 95\%$.
2. **`[RECOMENDAÇÃO: ATUALIZAÇÃO]` / `[RECOMENDAÇÃO: OTIMIZAR YAML]`**: Frontmatter incompleto, referências/links quebrados no ambiente ou dependências/ferramentas defasadas.
3. **`[RECOMENDAÇÃO: AJUSTE]`**: Falha cognitivo-discriminativa (skill vaga, ausência dos fatores do arquétipo como planejamento sem gestão de ambiguidade ou auditoria E2E sem `click`/`a11y`/DOM, regras contraditórias, contaminação entre domínios ou `> 10` regras sem `rules/`).
4. **`[RECOMENDAÇÃO: MELHORIA]`**: Inchaço de contexto (`> 1.200` tokens no `SKILL.md` sem *Progressive Disclosure* em `references/`).
5. **`[RECOMENDAÇÃO: EXCLUSÃO]`**: Skill obsoleta, quebrada ou placebo sem capacidade real ($\text{Pass}@k < 50\%$).
6. **`[RECOMENDAÇÃO: FUSÃO]`**: Colisão de rota/nome ou sobreposição semântica crítica de gatilhos (`>= 80%`) com outra skill do catálogo.

