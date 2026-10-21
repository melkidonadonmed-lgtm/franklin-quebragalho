# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`organizador-projetos-ideias` v1.0.0)

Para assegurar que a concepção de ideias (`ideation_to_v1`) e a organização de projetos existentes (`project_organizer_sync`) sejam auditáveis e livres de alucinação, cada execução é avaliada sob três marcadores estritos:
- `[PASS]`: Requisito integralmente atendido e comprovado nos arquivos reais do projeto.
- `[FAIL]`: Violação direta de regra operacional, divergência entre `README.md` e disco ou limpeza destrutiva sem confirmação.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência de acesso ao diretório ou aguardando resposta humana na etapa de ideação.

---

### Regra 1: Roteamento Dinâmico e Protocolo Inteligente do *"Não sei"* (Modo 1)
- **Critério**: Quando ativada para refinar uma ideia (`ideation_to_v1`), a skill investigou intenção/objetivo, perguntou as funções desejadas e, caso o usuário tenha respondido *"não sei"*, gerou perguntas baseadas na ideia e propôs o pacote mínimo de funções (MVP) perguntando se deseja alterar/acrescentar e se deseja criar a versão `1.0` com metadados datados?
- **Teste**:
  - Usuário responde *"não sei"* às funções e a skill trava ou exige que o usuário invente sozinho sem sugerir o mínimo -> `[FAIL: FALLBACK_NAO_SEI_OMITIDO]`
  - Ausência de metadados da versão com data (`AAAA-MM-DD`) ao consolidar a v1.0 -> `[FAIL: METADADOS_VERSAO_AUSENTES]`
  - Proposta de MVP gerada com clareza, design/estrutura propostos e confirmação da v1.0 solicitada -> `[PASS]`

### Regra 2: Sincronização de Documentos-Chave e Paridade `README.md` vs. Estado Real (Modo 2)
- **Critério**: Na organização de projeto (`project_organizer_sync`), a skill verificou arquivos faltantes, estruturou/atualizou `AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`, `GEMINI.md`/`CLAUDE.md` e garantiu que o `README.md` reflita exatamente os arquivos e pastas reais presentes no disco?
- **Teste**:
  - `README.md` cita arquivos, scripts ou pastas inexistentes no disco sem marcá-los como roadmap -> `[FAIL: README_DESATUALIZADO_VS_REAL]`
  - Omissão na verificação/criação dos documentos-chave (`AGENTS.md`, `SPEC.md`, `CONTEXT.md`, `DESIGN.md`) -> `[FAIL: DOCUMENTOS_CHAVE_INCOMPLETOS]`
  - Documentação base completa e `README.md` batendo 1:1 com a árvore real -> `[PASS]`

### Regra 3: Auditoria e Organização de Componentes e Contratos (`MCP`, `FastAPI`, `RPC`)
- **Critério**: A skill inspecionou e organizou os componentes e contratos de comunicação aplicáveis ao projeto (`tools.json` / MCP, conexão FastAPI, contratos RPC), documentando métodos, parâmetros e schemas atualizados para 2026?
- **Teste**:
  - Contratos RPC/MCP/FastAPI deixados espalhados ou sem métodos documentados quando presentes no escopo -> `[FAIL: CONTRATOS_DESORGANIZADOS]`
  - Componentes e contratos organizados com métodos claros e tipagem atualizada -> `[PASS]`

### Regra 4: Segurança (`.env` / `.gitignore`), Repositório Online e Higiene da Raiz com Dry-Run
- **Critério**: A skill verificou `.env` e `.gitignore`, checou a existência de repositório online (`git remote -v`) e realizou a limpeza da raiz (removendo/movendo arquivos fora de escopo) apenas após apresentar preview seguro (*Dry-Run*)?
- **Teste**:
  - Exclusão definitiva de arquivos da raiz sem confirmação do usuário -> `[FAIL: LIMPEZA_RAIZ_DESTRUTIVA]`
  - Segredos reais do `.env` expostos na documentação ou ausência de checagem do `.gitignore` -> `[FAIL: VAZAMENTO_ENV_OU_GITIGNORE]`
  - Raiz higienizada com segurança, `.env`/`.gitignore` validados e status do repositório online reportado -> `[PASS]`

### Regra 5: Diagrama de Funcionamento (Mermaid) e Atualização de Memória/Contexto
- **Critério**: Quando há fluxo operacional no projeto, a skill gerou o diagrama Mermaid válido (rótulos entre aspas) e atualizou a memória e o estado atual (`CONTEXT.md`) com os dados novos?
- **Teste**:
  - Projeto com fluxo claro entregue sem diagrama de funcionamento Mermaid -> `[FAIL: DIAGRAMA_FLUXO_AUSENTE]`
  - Estado atual e memória não atualizados após reestruturação do projeto -> `[FAIL: MEMORIA_CONTEXTO_DESATUALIZADOS]`
  - Diagrama Mermaid válido e memória/contexto sincronizados -> `[PASS]`
