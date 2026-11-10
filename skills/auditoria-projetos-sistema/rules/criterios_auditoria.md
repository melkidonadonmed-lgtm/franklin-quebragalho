# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`auditoria-projetos-sistema` v6.0.0)

Para eliminar auditorias superficiais que leem apenas Markdown, o agente auditor deve executar os scripts de `scripts/` e emitir estritamente:

- `[PASS]`: Requisito comprovado na AST do código real, na árvore física do disco ou no DOM ao vivo.
- `[FAIL]`: Requisito violado com apontamento exato de arquivo, linha ou métrica.
- `[UNVERIFIED]`: Não verificável por ausência de insumos ou runtime desligado.

---

### Regra 1: Verificação Obrigatória de Código Real e Estrutura Física (`project_structure_and_code_auditor.py` — 20 pts)

- **Critério**: O auditor executou `project_structure_and_code_auditor.py`, inspecionou `README.md`, `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `CURRENT_STATE.md`, `.gitignore` e `.env.example`, classificou o Nível de Complexidade (1, 2, 3 ou Poliglota MCP) e conferiu a AST das funções reais?
- **Teste**:
  - Auditoria feita apenas lendo `.md` sem inspecionar código-fonte real -> `[FAIL: AUDITORIA_SUPERFICIAL_SEM_CODIGO]`
  - `.env` exposto ou `.gitignore` sem proteger `.env`/`node_modules`/`.venv` -> `[FAIL: VAZAMENTO_CREDENCIAIS_GIT]`
  - Estrutura física, documentos vitais e código real inspecionados -> `[PASS]`

### Regra 2: Paridade Documentação vs. Implementação e Diagnóstico Causal de MVP (20 pts)

- **Critério**: Cada módulo prometido em `README.md`/`SPEC.md` foi confrontado contra o disco (`[IMPLEMENTADO_FUNCIONAL]`, `[MOCK_SUPERFICIAL]`, `[INEXISTENTE_DOCUMENTADO]`, `[CÓDIGO_FANTASMA]`) e cada bloqueio de MVP possui justificativa causal (`Por quê:`)?
- **Teste**:
  - Caminho ou módulo citado no `README.md`/`SPEC.md` não existe no disco -> `[FAIL: INEXISTENTE_DOCUMENTADO]`
  - Item de MVP sem justificativa causal (`Por quê:`) ou inflado com Scope Creep -> `[FAIL: MVP_SEM_CAUSA_EFEITO]`
  - Paridade 1:1 comprovada e MVP enxuto -> `[PASS]`

### Regra 3: Qualidade de Código Real (AST), Zero Placebos e Detecção de Orfandade (25 pts)

- **Critério**: Os motores `project_structure_and_code_auditor.py` e `frontiercode_maintainability_guardrail.py` comprovam zero funções placebo (`pass`, `onClick={() => {}}`), zero `except:` genérico e zero arquivos órfãos?
- **Teste**:
  - Função vazia/stub ou controle placebo sem ação real -> `[FAIL: FUNCAO_PLACEBO_REAL_STATE]`
  - Arquivo de código isolado sem consumidor nem entrypoint -> `[FAIL: ARQUIVO_ORFAO]`
  - Código tipado, coeso ($\le 60$ linhas/função) e 100% conectado -> `[PASS]`

### Regra 4: Regra `60-30-10`, Cores `OKLCH`, Sombras em 3 Níveis e Navegação em 3 Camadas (`SGA` — 20 pts)

- **Critério**: A interface respeita a **Proporção `60-30-10`** (`60%` `--surface-canvas`, `30%` `--surface-card`/`--surface-elevated`, `10%` acento cirúrgico), **Cores Perceptuais `OKLCH`** (`oklch()`, `light-dark()`, Dark Mode $L = 0.16 \to 0.22 \to 0.27$ sem `#000000`), **Sombras Multi-Camadas em 3 Níveis** (Umbra + Penumbra com `spread` negativo + Borda Especular `inset 0 1px 0 0`), **Navegação em 3 Camadas** (`<= 3 <nav>`, menus descompactados `>= 13px`, `X ativa Y`, reuso In-Place sem sub-abas aninhadas) e `SGA >= 85` via `deterministic_scorer.py`?
- **Teste**:
  - Violação da proporção `60-30-10`, ausência de `oklch()`, uso de `#000000` puro ou cores neon -> `[FAIL: VIOLACAO_60_30_10_OU_OKLCH]`
  - Sombra simples de camada única sem Umbra + Penumbra + Rim Light zenital -> `[FAIL: SOMBRA_LAVADA_OU_CAMADAS_RUINS]`
  - Menus compactados (`< 13px`), proliferação de abas (`> 4` ou sub-abas), *Dead Ends* ou `row-reverse` quebrando `Tab` -> `[FAIL: NAVEGACAO_OU_SGA_REPROVADO]`
  - Conformidade integral com os 9 Eixos do SSOT, `60-30-10 OKLCH` e `SGA` -> `[PASS]`

### Regra 5: Segurança MCP/RPC e Protocolo HITL para `agent-browser` / `chrome-devtools-mcp` (15 pts)

- **Critério**: Os contratos MCP/FastAPI/RPC usam validação estrita (`extra="forbid"`) e a inspeção dinâmica de DOM (`agent-browser` `@eX` / `chrome-devtools-mcp`) respeitou aprovação HITL?
- **Teste**:
  - Execução de navegador em URL sem confirmação HITL ou servidor MCP poluindo `stdout` -> `[FAIL: VIOLACAO_HITL_OU_MCP_STDIO]`
  - Contratos estritos e esteira visual validada com segurança -> `[PASS]`
