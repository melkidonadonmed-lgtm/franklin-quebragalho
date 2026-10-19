# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`auditoria-projetos-sistema` v3.0.0)

Para evitar simulações vazias e auditorias inventadas, o agente auditor deve emitir estritamente um dos seguintes status determinísticos:
- `[PASS]`: Requisito comprovado e verificado contra âncoras documentais ou código real inspecionado.
- `[FAIL]`: Requisito violado com motivo específico demonstrado e apontamento de linha/arquivo.
- `[UNVERIFIED]`: Não verificável por ausência de insumos no input ou impossibilidade de execução.

---

### Regra 1: Governança Física e Arquivos Vitais (Dimensão 1 - 20 pts)
- **Critério**: O repositório contém `README.md`, `CONTEXT.md` (ou `GEMINI.md`/`AGENTS.md`), `DESIGN.md` (se possuir UI), `SPEC.md`/`TODO.md`, `.env.example` e `.gitignore`?
- **Teste**:
  - `README.md` ausente ou vazio -> `[FAIL: README_AUSENTE]`
  - `.env` ou segredos comitados no Git -> `[FAIL: VAZAMENTO_CREDENCIAIS_GIT]`
  - `.gitignore` sem exclusão de `node_modules/` ou builds -> `[FAIL: GITIGNORE_INADEQUADO]`
  - Arquivos vitais presentes e íntegros -> `[PASS]`

### Regra 2: Coerência Narrativa Documental (Dimensão 2 - 20 pts)
- **Critério**: Todas as funcionalidades descritas no README existem e estão implementadas?
- **Teste de Classificação**:
  - Função existe e tem lógica real conectada -> `[IMPLEMENTADO_FUNCIONAL]`
  - Interface existe mas retorna dados estáticos sem conexão -> `[MOCK_SUPERFICIAL]`
  - Documentação promete mas arquivo/rota não existe -> `[INEXISTENTE_DOCUMENTADO]`
  - Módulo complexo presente sem registro documental -> `[CÓDIGO_FANTASMA]`

### Regra 3: Higiene de Código e Detecção de Orfandade (Dimensão 3 - 25 pts)
- **Critério**: Há arquivos de código `.ts`, `.tsx`, `.js`, `.py` não importados a partir dos entrypoints (`index`, `app`, `main`, `server`)?
- **Teste**:
  - Arquivo isolado sem nenhuma referência cruzada ou teste -> `[FAIL: ARQUIVO_ORFAO]`
  - Funções exportadas que não possuem consumidores -> `[FAIL: EXPORT_MORTO]`
  - Árvore de dependências 100% conectada -> `[PASS]`

### Regra 4: Adequação ao Propósito, Estilo, Espaçamento, Contraste, Tipografia, Camadas e Nós (Dimensão 4 - 20 pts)
- **Critério**: O estilo visual reflete o **propósito do projeto** (sem paletas fixas artificiais), respeitando espaçamento/respiro ($\ge 25\%$), contraste perceptual (WCAG 2.1 AA/AAA, tinta escura em menus claros/`#8e8999`), tipografia fluida (`clamp()`, `tabular-nums`, `IBM Plex` em tema Preto Terminal), elevação em camadas (sombra esculpida tripla + `1px` Rim Light + blocos de contraste alternados), isolamento de 1 CTA primário e nós interativos funcionais (`@eX`)?
- **Teste**:
  - Tema incompatível com o domínio/propósito do projeto ou repetição mecânica de paleta sem contexto -> `[FAIL: TEMA_DESALINHADO_AO_PROPOSITO]`
  - Menus e navegação compactados (`gap < 8px`), texto branco lavado sobre menu claro/cinza (`#8e8999`) ou contraste WCAG $< 4.5:1$ -> `[FAIL: CONTRASTE_MENU_OU_WCAG]`
  - Múltiplos CTAs primários coloridos competindo na mesma vista ou acento cromático dominando $> 15\%$ da tela -> `[FAIL: POLUICAO_CROMATICA_SEM_ISOLAMENTO]`
  - Ausência de escala fluida `clamp()`, falta de `tabular-nums` em métricas/tabelas ou ausência de `IBM Plex` em tema Preto Terminal -> `[FAIL: HIERARQUIA_OU_TIPOGRAFIA_FRACA]`
  - Falta de respiro ($\text{whitespace} < 25\%$), ausência de camadas (sombra esculpida 3 estágios + `1px` Rim Light) ou raios internos não concêntricos -> `[FAIL: ESPACAMENTO_OU_CAMADAS_RUINS]`
  - Botão menor que $44\times44\text{px}$ ou sem classes anti-squish (`flex-shrink: 0; white-space: nowrap`) -> `[FAIL: BOTAO_PEQUENO_OU_SQUISH]`
  - Tag `<div>` simulando botão sem `tabIndex`/ARIA ou botão com `onClick` vazio -> `[FAIL: DIVSOUP_OU_NO_INERTE]`
  - Tema alinhado ao propósito, contraste nítido, tipografia calibrada, camadas esculpidas e nós ergonômicos comprovados -> `[PASS]`

### Regra 5: Protocolo Human-in-the-Loop para Execução Visual com agent-browser (Dimensão 5 - 15 pts)
- **Critério**: O pipeline automatizado de navegação e screenshots via `agent-browser` foi disparado com consentimento explícito e parâmetros delimitados?
- **Teste**:
  - Agente disparou comandos `agent-browser open` ou mutações sem autorização prévia -> `[FAIL: VIOLACAO_HITL]`
  - Agente solicitou confirmação apresentando comandos (`open`, `snapshot -i`, `screenshot --annotate`) e URLs -> `[PASS]`
