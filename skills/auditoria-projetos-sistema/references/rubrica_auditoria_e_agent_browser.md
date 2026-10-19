# Protocolo `agent-browser` (@eX), Rubrica de Estilo por Propósito e Template de Relatório (`auditoria-projetos-sistema` v3.0.0)

Referência técnica de Tier 3 para inspeção visual dinâmica via `agent-browser`, rubrica de adequação do tema ao propósito do projeto (0 a 100) e template executivo de entrega.

---

## 1. Protocolo de Inspeção Dinâmica com `agent-browser` (Módulos 4 e 5 — Requer HITL)

```powershell
# 1. Abertura, estabilização e extração de árvore semântica (@e1, @e2...)
agent-browser open $AppUrl
agent-browser wait 1500
agent-browser snapshot -i

# 2. Conexão a instância existente do Chrome/Edge (CDP)
agent-browser --cdp 9222 snapshot
agent-browser --auto-connect snapshot

# 3. Captura comparativa de Atmosferas / Temas (Dark / Light / Monolítico)
agent-browser --color-scheme dark open $AppUrl
agent-browser screenshot ./reports/dark_mode.png --full
agent-browser --color-scheme light open $AppUrl
agent-browser screenshot ./reports/light_mode.png --full

# 4. Captura anotada com rótulos @eX para inspeção multimodal
agent-browser screenshot ./reports/audit_annotated.png --annotate

# 5. Teste de transição de abas/menus e mutação de estado (FSM)
agent-browser click @e1
agent-browser wait 800
agent-browser snapshot -i
```

### Falhas Determinísticas Rastreadas no Snapshot `@eX` & Estilo:
- `[FAIL: TEMA_DESALINHADO_AO_PROPOSITO]`: Tema ou paleta aplicada mecanicamente sem relação com o objetivo do projeto (ex.: estética de entretenimento em sistema clínico ou falta de tipografia técnica em terminal).
- `[FAIL: CONTRASTE_MENU_OU_WCAG]`: Texto branco lavado sobre menus claros/cinzas (`#8e8999`), razão WCAG $< 4.5:1$ ou inversão incorreta de luminância ($L_{\text{card}} \le L_{\text{canvas}}$ no escuro).
- `[FAIL: HIERARQUIA_OU_TIPOGRAFIA_FRACA]`: Ausência de `clamp()`, falta de `tabular-nums` em KPIs/tabelas, ausência de `IBM Plex` em tema Preto Terminal (`Ex Umbris`) ou múltiplos CTAs primários competindo na mesma dobra.
- `[FAIL: ESPACAMENTO_OU_CAMADAS_RUINS]`: Whitespace $< 25\%$, cards colados sem respiro, ausência de sombra esculpida em 3 camadas + `1px` Rim Light, ou violação de raios concêntricos.
- `[FAIL: DIVSOUP_ACESSIBILIDADE]`: Tags `<div>`/`<span>` simulando botões sem semântica ARIA nem suporte a teclado.
- `[FAIL: NO_INERTE_SEM_ACAO]`: Elementos interativos com `onClick` vazio, `preventDefault()` isolado ou sem mutação observável.
- `[FAIL: ANTI_SQUISH_VIOLADO]`: Botões ou badges sem `flex-shrink: 0; white-space: nowrap;` ou alvos $< 44\times44\text{px}$.

---

## 2. Template Canônico de Relatório de Auditoria (Saída Estruturada)

```markdown
# RELATÓRIO DE AUDITORIA TÉCNICA E VISUAL DO PROJETO

## 1. RESUMO EXECUTIVO & NOTA GERAL
- **Projeto Auditado:** [Nome ou Caminho]
- **Propósito / Domínio Identificado:** [Conversão & SaaS | Editorial & Leitura | FinTech & Confiança | IA Nativa & AETHER | MedTech Clínico | DevTools & Terminal IBM]
- **Tema / Atmosfera Recomendada vs. Atual:** [Ex: Ad Lucem / Cinza #57545d + Menus #8e8999 / Preto Terminal IBM Ex Umbris / AETHER 2027]
- **Pontuação Consolidada:** [X / 100] -> [Enterprise (90-100) / Moderado (70-89) / Instável (50-69) / Reprovado (<50)]
- **Diagnóstico Síntese:** [2 a 3 frases objetivas]

## 2. AUDITORIA ESTRUTURAL E GOVERNANÇA DE PASTAS (20 pts)
| Arquivo / Pasta Vital | Status | Observação Técnica |
| :--- | :--- | :--- |
| `AGENTS.md` / `README.md` | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `CONTEXT.md` / `SPEC.md` | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `DESIGN.md` (Arquitetura Visual & Propósito) | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `.gitignore` & `.env.example` | `[PASS]` / `[FAIL]` | [Verificação de vazamento de segredos/build] |

## 3. COERÊNCIA NARRATIVA: DOCUMENTADO VS. IMPLEMENTADO (20 pts)
| Funcionalidade Declarada | Status | Evidência / Arquivo |
| :--- | :--- | :--- |
| [Recurso X] | `[IMPLEMENTADO_FUNCIONAL]` / `[MOCK_SUPERFICIAL]` / `[INEXISTENTE_DOCUMENTADO]` / `[CÓDIGO_FANTASMA]` | [Caminho] |

## 4. HIGIENE DE CÓDIGO, TIPAGEM, CHUNKING & ARQUIVOS ÓRFÃOS (25 pts)
- **Arquivos/Exports Órfãos:** [Lista]
- **Desacoplamento, Tipagem e Chunking (`source_id`, `chunk_index`, `byte_range`):** [Diagnóstico]

## 5. AUDITORIA DE PROPÓSITO VISUAL, ESTILO, CAMADAS & NÓS INTERATIVOS (20 pts)
- **Encaixe do Tema ao Propósito (4 pts):** [Avaliação do tema atual vs. objetivo do projeto]
- **Contraste, Proporção 98/2 (ou 60-30-10) & Menus (4 pts):** [WCAG AA/AAA, APCA, legibilidade de menus e isolamento de 1 CTA Primário]
- **Tipografia, Hierarquia & `tabular-nums` (4 pts):** [Escala `clamp()`, 4 níveis de tinta, IBM Plex no terminal preto]
- **Espaçamento, Respiro & Camadas Esculpidas (4 pts):** [Whitespace >= 25%, Bento Grid, raios concêntricos, sombra 3 camadas + 1px Rim Light, cards de contraste alternados]
- **Snapshot Interativo (`agent-browser snapshot -i`) & FSM (4 pts):** [Relação de nós `@eX`, estados `idle/loading/error/pressed`, `divsoup` e nós inertes]

## 6. SEGURANÇA, GIT & PROTOCOLOS MCP (15 pts)
- **Configuração MCP e Schemas (`extra="forbid"`):** [Diagnóstico]

## 7. PLANO DE AÇÃO IMEDIATO (PRIORIZADO)
1. [Correção Crítica Bloqueante]
2. [Ajuste de Tema, Contraste, Espaçamento ou Tipografia ao Propósito]
3. [Saneamento de Orfandade / Nós Interativos]
```
