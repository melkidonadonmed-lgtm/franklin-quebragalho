---
name: auditoria-projetos-sistema
description: >-
  Audita a integridade estrutural, arquivos essenciais (README, CONTEXT, DESIGN, SPEC), higiene de repositório (.env, .gitignore, Git), orfandade de código, discrepâncias entre escopo documentado e executado, conformidade de UI/UX (temas, fontes, alvos de clique, nós de ação) e esteira visual automatizada via agent-browser (snapshots interativos, nós @eX e anotações visuais) com emissão de nota ponderada (0 a 100).
version: "2.1.0"
compatibility: Ambientes com suporte a Agent Skills (Antigravity IDE, Claude Desktop, Cursor, Google ADK, VS Code Copilot). Requer agent-browser CLI e Node.js 20+ ou Python 3.11+.
metadata:
  version: "2.1.0"
  author: "Arquiteto de Soluções & Melki"
  category: "Engenharia de Software, Auditoria e Qualidade"
---

# 1. NOME DA SKILL
`auditoria-projetos-sistema` (Auditor Sênior de Repositórios, Arquitetura, UI/UX e Protocolos de Contexto com agent-browser)

---

## 2. DESCRIÇÃO
Esta skill implementa uma esteira de inspeção técnica e visual de alta fidelidade para repositórios modernos. Ela analisa a hierarquia física de pastas e arquivos de governança, identifica códigos e arquivos órfãos, confronta a promessa funcional da documentação contra a implementação real nos arquivos, avalia a coesão do Design System (discrepâncias de fontes, coerência de temas por componente e se os nós interativos realmente ativam ações funcionais) e disponibiliza um protocolo de captura sequencial de telas e inspeção do DOM vivo via **agent-browser** (com extração de snapshots interativos `@eX`, screenshots anotados para modelos de visão e teste de temas). O resultado é consolidado em um relatório formal com nota ponderada de 0 a 100, matriz de riscos e plano de ação imediato.

---

## 3. GATILHOS DE ATIVAÇÃO
Carregue esta skill quando o usuário solicitar:
- "Audite este projeto / repositório por completo"
- "Verifique a integridade da estrutura de pastas, arquivos essenciais e gitignore"
- "Avalie a qualidade do código, arquivos órfãos e compare com o README"
- "Audite a UI/UX, fontes, temas por seção e se os botões/nós realmente funcionam"
- "Execute auditoria visual ou modo de print com o agent-browser para inspecionar páginas web"
- "Inspecione nós interativos e acessibilidade visual com agent-browser snapshot"
- "Calcule a nota de maturidade técnica do projeto"

**Quando NÃO usar esta skill:**
- Para refatorar código massivamente antes da aprovação do relatório de auditoria.
- Para gerar novas funcionalidades do zero que não façam parte de uma verificação de conformidade.
- Para resolver apenas um bug pontual isolado de sintaxe sem contexto do projeto.

---

## 4. ENTRADAS ESPERADAS
- `project_root_path` (obrigatório): Caminho absoluto ou relativo da raiz do projeto auditado.
- `stack_preference` (opcional): Stack primária do projeto (ex.: Next.js/React + Tailwind + FastAPI, Node.js puro, Python Agentic).
- `audit_scope` (opcional): Escopo desejado (`completo`, `somente_arquitetura_git`, `somente_ui_ux`, `somente_codigo`). Padrão: `completo`.
- `enable_visual_run` (opcional, booleano): Habilita o pipeline de navegação e captura via `agent-browser` (padrão: `false`, requer aprovação prévia HITL).
- `app_url` (opcional): URL da aplicação em execução para auditoria dinâmica via `agent-browser` (ex.: `http://localhost:3000`, `http://localhost:5173`, `http://localhost:5678`).

---

## 5. PROCESSAMENTO INTERNO (MÓDULOS DESACOPLADOS)

O agente deve processar a auditoria em fases sequenciais para evitar saturação da janela de contexto:

```text
[Início da Auditoria]
│
▼
[Módulo 1: Governança Física & Git] ──► .env, .gitignore, pastas vitais
│
▼
[Módulo 2: Coerência Documental]     ──► README/CONTEXT vs Código Real
│
▼
[Módulo 3: Qualidade & Orfandade]    ──► Arquivos mortos, exports sem uso
│
▼
[Módulo 4: UI/UX, Temas & Nós]       ──► Cores, Fontes, Handlers e agent-browser snapshot
│
▼
[Módulo 5: Esteira Visual agent-browser] ──► (Requer HITL) Prints anotados & Transições
│
▼
[Módulo 6: Integrações & MCP]        ──► Schemas, Tools, Conectores
│
▼
[Módulo 7: Rubrica & Nota Final]     ──► Cálculo ponderado (0 a 100)
```

---

### MÓDULO 1: GOVERNANÇA DE PASTAS, HIGIENE DE REPOSITÓRIO E GIT
1. **Varredura de Estrutura Mínima Obrigatória:**
   - Conferir se existem os artefatos vitais de governança:
     * `README.md` (instruções objetivas de instalação e inicialização).
     * `CONTEXT.md` (regras de negócio, fronteiras e restrições da IA).
     * `DESIGN.md` (tokens visuais, paleta, componentes base — se houver UI).
     * `SPEC.md` ou `TODO.md` (delimitação estrita do MVP atual).
     * `.env.example` (documentação de variáveis de ambiente sem segredos reais).
     * `.gitignore` (bloqueio estrito de `node_modules/`, `.env`, `.venv/`, `.next/`, `dist/`, caches locais).
   - Verificar presença das pastas especializadas:
     * `.agents/skills/` ou `skills/` (definições no padrão SKILL.md).
     * `mcp_servers/` (servidores locais ou arquivos de conexão).
     * `scripts/` (utilitários de automação e validação).
     * `tests/` (testes unitários e de integração).
2. **Auditoria de Vazamento e Git:**
   - Detectar se há chaves de API, senhas ou tokens expostos em arquivos comitáveis.
   - Conferir se o lockfile do projeto é único e íntegro (ex.: apenas `package-lock.json` ou apenas `pnpm-lock.yaml`, nunca múltiplos simultâneos).

---

### MÓDULO 2: CONFRONTO DOCUMENTAÇÃO VS. REALIDADE (PROMETIDO VS. IMPLEMENTADO)
1. **Extração das Premissas Documentadas:**
   - Ler o `README.md` e `CONTEXT.md`, isolando a lista de funcionalidades alegadas, rotas prometidas e integrações declaradas.
2. **Confronto com a Base de Código:**
   - Para cada recurso prometido: verificar se o arquivo, rota de API ou tela realmente existe.
   - Classificar o status:
     * `[IMPLEMENTADO_FUNCIONAL]`: Existe e possui lógica completa.
     * `[MOCK_SUPERFICIAL]`: O componente existe visualmente, mas devolve dados fictícios estáticos sem conexão real.
     * `[INEXISTENTE_DOCUMENTADO]`: O documento promete o recurso, mas não há código correspondente.
     * `[CÓDIGO_FANTASMA]`: Há módulos complexos criados que não foram descritos na documentação.

---

### MÓDULO 3: QUALIDADE DE CÓDIGO, MODULARIDADE E ARQUIVOS ÓRFÃOS
1. **Detecção de Código Morto e Orfandade:**
   - Rastrear arquivos `.ts`, `.tsx`, `.js`, `.py` presentes na árvore que nunca são importados no ponto de entrada (`index`, `app`, `main`).
   - Identificar funções exportadas que não possuem consumidores internos nem testes.
2. **Análise de Arquitetura e Acoplamento:**
   - Verificar se há separação entre camadas de Domínio/Regras de Negócio, Infraestrutura/APIs e Apresentação/UI.
   - Detectar anti-padrões como: chamadas diretas de banco de dados ou `fetch` soltos no corpo de renderização de componentes, ausência de tratamento de erros `try/catch` e tipos `any` genéricos.

---

### MÓDULO 4: AUDITORIA DE UI/UX, DESIGN SYSTEM, TEMAS E NÓS DE AÇÃO
1. **Auditoria Estática de Temas e Tokens:**
   - Mapear a paleta de cores usada em cada sessão (`Header`, `Sidebar`, `Main`, `Cards`, `Modals`).
   - Identificar conflitos de tema: componentes com fundo claro forçado (`bg-white`) dentro de páginas configuradas para Dark Mode profundo, ou textos com contraste ilegível (reprovado na WCAG 2.1 AA).
2. **Discrepância Tipográfica (Fontes e Escalas):**
   - Identificar declared fonts vs. inline fonts: fontes carregadas pelo sistema vs. classes arbitrárias soltas no código (ex.: misturar semântica de `inter`, `roboto` e `font-mono` sem convenção).
   - Checar se a tipografia é fluida (uso de `rem` ou `clamp()`) ou se trava em `px` fixos que quebram em visualização mobile.
3. **Auditoria Dinâmica de Nós Interativos com `agent-browser`:**
   - Se a aplicação estiver em execução ou acessível via URL, executar a inspeção dinâmica de nós:
     ```powershell
     agent-browser open [app_url] && agent-browser snapshot -i
     ```
   - O comando devolve a árvore semântica filtrada de elementos interativos com identificadores únicos (`@e1`, `@e2`, ...), papéis (`role`), nomes acessíveis (`name`) e estados (`disabled`, `expanded`).
   - **Verificações com o Snapshot:**
     * Detectar botões sem nome acessível ou texto vazio.
     * Detectar tags `<div>` simulando botões sem eventos de teclado e sem semântica ARIA (`[FAIL: DIVSOUP_ACESSIBILIDADE]`).
     * Identificar botões ou links que não disparam mutações nem eventos (`[FAIL: NO_INERTE_SEM_ACAO]`).
4. **Composição Geral, Escala dos Tokens e Resiliência de Conteúdo (Anti-Squish & Overflow Shielding):**
   - **Composição Geral e Grid:** Avaliar a respiração visual, margens de contêineres e responsividade dos grids (`grid-template-columns`). Reprovar layouts onde cartões fiquem comprimidos horizontalmente gerando quebras desordenadas de títulos.
   - **Tamanho dos Tokens e Alvos de Clique:** Auditar dimensões mínimas (`min-width`, `min-height`), alvos de toque (mínimo de 36px a 44px) e aplicação estrita de `flex-shrink: 0` em botões de ação e badges para impedir esmagamento flexbox.
   - **Resiliência de Conteúdo em Tokens (Content Fitting):**
     * Proibição estrita de palavras espremidas na vertical (ex.: texto de botão quebrando letra por letra).
     * Truncamento inteligente em caminhos de arquivo, hashes e URLs (`text-overflow: ellipsis`, `white-space: nowrap`, `overflow: hidden`) preservando a ponta final com a extensão do arquivo ou com tooltip nativo (`title`).
     * Preservação de rótulos em botões com `white-space: nowrap`.
   - **Tipografia e Ritmo Vertical:** Auditar escala tipográfica harmônica, `line-height` proporcional (1.3 a 1.6) e hierarquia semântica entre títulos, subtítulos, textos de apoio e dados monoespaçados.

---

### MÓDULO 5: ESTEIRA VISUAL AUTOMATIZADA COM AGENT-BROWSER (HITL)
> [!IMPORTANT]
> **REGRA DE SEGURANÇA OBRIGATÓRIA (Human-in-the-Loop):** A execução da esteira visual com navegação web ativa deve sempre ser aprovada previamente pelo usuário antes do disparo.

1. **Abertura e Estabilização de Renderização:**
   - O agente apresenta ao usuário os comandos exatos de execução:
     ```powershell
     agent-browser open [app_url] && agent-browser wait 1500
     ```
   - Caso o Chrome do usuário já esteja aberto com depuração remota ativada:
     ```powershell
     agent-browser --cdp 9222 snapshot
     ```
     ou conexão automática com:
     ```powershell
     agent-browser --auto-connect snapshot
     ```

2. **Auditoria de Temas Claro e Escuro (Color Scheme Testing):**
   - Capturar a visualização em Dark Mode e Light Mode nativamente:
     ```powershell
     agent-browser --color-scheme dark open [app_url] && agent-browser screenshot ./reports/dark_mode.png --full
     agent-browser --color-scheme light open [app_url] && agent-browser screenshot ./reports/light_mode.png --full
     ```

3. **Captura Visual Anotada para Inspeção Multimodal:**
   - O `agent-browser` gera uma captura onde cada elemento interativo recebe um rótulo numérico visível com seu identificador `@eX`:
     ```powershell
     agent-browser screenshot ./reports/audit_annotated.png --annotate
     ```
   - O agente ou modelo multimodal de visão inspeciona a imagem anotada para conferir alinhamento de rótulos, contraste tátil e ausência de overlaps visuais.

4. **Teste de Transições e Mutações de Estado:**
   - Acionar nós interativos sequenciais via encadeamento:
     ```powershell
     agent-browser click @e1 && agent-browser wait 800 && agent-browser snapshot -i
     ```
   - Verificar se houve mutação de estado esperada (ex: modal aberto, rota alterada, feedback de toast visível) ou se ocorreu travamento visual.

---

### MÓDULO 6: INTEGRAÇÃO COM MODEL CONTEXT PROTOCOL (MCP) E CONECTORES
1. **Checagem de Configurações MCP:**
   - Verificar se existe `mcp_config.json`, `.vscode/mcp.json` ou arquivos de conexão válidos.
   - Avaliar se os servidores declarados contêm caminhos absolutos corretos e variáveis de ambiente protegidas.
2. **Qualidade dos Schemas de Tools:**
   - Se o projeto expõe ferramentas MCP: verificar se possuem nome semântico, descrição com efeito colateral explícito, esquema de entrada rigoroso (`extra="forbid"`) e tipos definidos.

---

### MÓDULO 7: SISTEMA DE PONTUAÇÃO PONDERADA (NOTA 0 A 100)
A nota de maturidade técnica do projeto é calculada pela soma das 5 dimensões ponderadas:

| Dimensão | Peso | Critério de Pontuação |
| :--- | :--- | :--- |
| **1. Governança e Arquitetura** | 20 pts | Presença de README, CONTEXT, SPEC, DESIGN, .env.example e .gitignore sem lixo. |
| **2. Coerência Funcional** | 20 pts | O que o README descreve corresponde ao código real (zero funções fantasma/mock enganoso). |
| **3. Qualidade de Código & Higiene** | 25 pts | Ausência de arquivos órfãos, tipagem forte, ausência de loops assíncronos e testes mínimos. |
| **4. Ergonomia UI/UX & Acessibilidade** | 20 pts | Temas coerentes, contraste WCAG AA, fontes sem discrepâncias, nós interativos funcionais (validados via AST ou `agent-browser snapshot -i`). |
| **5. Segurança e Protocolos (Git/MCP)** | 15 pts | Zero segredos comitados, schemas de entrada blindados, dependências seguras. |

**Tabela de Classificação Final:**
- **90 a 100 pts:** Nível Enterprise / Pronto para Produção.
- **70 a 89 pts:** Funcional com Débitos Técnicos Moderados.
- **50 a 69 pts:** MVP Instável / Requer Saneamento Estrutural.
- **Abaixo de 50 pts:** Reprovado / Risco Crítico de Manutenção ou Segurança.

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)
A saída desta skill deve ser gerada estritamente no seguinte formato estruturado:

```markdown
# RELATÓRIO DE AUDITORIA TÉCNICA E VISUAL DO PROJETO

## 1. RESUMO EXECUTIVO & NOTA GERAL
- **Projeto Auditado:** [Nome ou Caminho do Projeto]
- **Pontuação Consolidada:** [X / 100] -> [Classificação: Enterprise / Moderado / Instável / Reprovado]
- **Diagnóstico Síntese:** [2 a 3 frases resumindo a maturidade do repositório]

## 2. AUDITORIA ESTRUTURAL E GOVERNANÇA DE PASTAS
| Arquivo / Pasta Vital | Status | Observação Técnica |
| :--- | :--- | :--- |
| `README.md` | [PRESENTE / AUSENTE / INCOMPLETO] | [Diagnóstico] |
| `CONTEXT.md` | [PRESENTE / AUSENTE] | [Diagnóstico] |
| `DESIGN.md` | [PRESENTE / AUSENTE] | [Diagnóstico] |
| `SPEC.md` / `TODO.md` | [PRESENTE / AUSENTE] | [Diagnóstico] |
| `.gitignore` | [CONFORME / INADEQUADO] | [Apontar se vaza build ou node_modules] |
| `.env.example` | [SEGURO / AUSENTE / CHAVES_EXPOSTAS] | [Diagnóstico] |
| `skills/` ou `.agents/` | [CONFIGURADO / AUSENTE] | [Diagnóstico] |
| `mcp_servers/` / configs | [CONFIGURADO / AUSENTE] | [Diagnóstico] |

## 3. COERÊNCIA NARRATIVA: DOCUMENTADO VS. IMPLEMENTADO
| Funcionalidade Declarada | Status no Código | Evidência / Arquivo |
| :--- | :--- | :--- |
| [Recurso X do README] | [IMPLEMENTADO / MOCK / INEXISTENTE] | [src/components/... ou ausente] |

## 4. HIGIENE DE CÓDIGO & ARQUIVOS ÓRFÃOS
- **Arquivos Não Referenciados (Órfãos):** [Lista dos arquivos que existem mas nunca são importados]
- **Exports Mortos:** [Funções que ninguém consome]
- **Gargalos de Qualidade:** [Erros de tipagem, dependências ausentes, loops potenciais]

## 5. AUDITORIA VISUAL, DESIGN SYSTEM & NÓS INTERATIVOS
- **Coerência de Temas:** [Diagnóstico de Light/Dark mode por componente e quebras de contraste]
- **Discrepâncias de Fontes:** [Fontes declaradas vs. fontes arbitrárias encontradas]
- **Integridade dos Nós e Ações:**
  * Snapshot Interativo (`agent-browser snapshot -i`): [Relação de nós @eX detectados e status]
  * Botões sem ação real: [Lista de botões com onClick vazio ou apenas preventDefault]
  * Acessibilidade de Navegação: [Uso correto de tags semânticas vs divsoup]

## 6. STATUS DA ESTEIRA VISUAL (AGENT-BROWSER & ANOTAÇÕES)
- [Status: Não executado (Aguardando aprovação) OU Executado com sucesso via agent-browser]
- [Capturas Realizadas: Fullpage, Dark/Light Mode e Screenshot Anotado --annotate]
- [Achados das transições de tela: Estabilidade do layout, ausência de flickers ou quebras de alinhamento]

## 7. MATRIZ DE PONTUAÇÃO DETALHADA
- Governança e Arquitetura: [X / 20]
- Coerência Funcional: [X / 20]
- Qualidade de Código & Higiene: [X / 25]
- Ergonomia UI/UX & Acessibilidade: [X / 20]
- Segurança e Protocolos (Git/MCP): [X / 15]
- **NOTA TOTAL: [X / 100]**

## 8. PLANO DE AÇÃO IMEDIATO (PRIORIZADO)
1. [Ação Crítica 1 - Correção bloqueante]
2. [Ação de Média Prioridade 2 - Saneamento de orfandade/tema]
3. [Melhoria Preventiva 3 - Refinamento de documentação]
```

---

## 7. EXCEÇÕES E LIMITES (O QUE A SKILL NÃO COBRE)

* **Não executa deploys ou alterações no banco de produção:** Limita-se à auditoria de arquivos e código local.
* **Não substitui suites formais de testes end-to-end de carga (stress testing):** O teste de transição e print analisa a estabilidade estética e navegabilidade visual, não vazão de requisições por segundo.
* **Não executa mutações no sistema de arquivos sem confirmação prévia:** Toda deleção de código órfão ou criação de arquivos deve ser expressamente confirmada pelo operador.
* **Navegação Dinâmica Restrita a Ambientes Autorizados:** O uso de `agent-browser` para interações ao vivo exige aplicação em execução acessível (localhost ou URL de staging aprovada).
