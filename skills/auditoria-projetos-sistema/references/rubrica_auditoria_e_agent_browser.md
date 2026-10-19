# Protocolo `agent-browser` (@eX), Rubrica Ponderada e Template de Relatório (`auditoria-projetos-sistema` v2.3.0)

Referência técnica de Tier 3 para inspeção visual dinâmica via `agent-browser`, rubrica ponderada (0 a 100) e template executivo de entrega.

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

# 3. Captura comparativa Dark Mode vs Light Mode
agent-browser --color-scheme dark open $AppUrl
agent-browser screenshot ./reports/dark_mode.png --full
agent-browser --color-scheme light open $AppUrl
agent-browser screenshot ./reports/light_mode.png --full

# 4. Captura anotada com rótulos @eX para inspeção multimodal
agent-browser screenshot ./reports/audit_annotated.png --annotate

# 5. Teste de transição de abas/menus e mutação de estado
agent-browser click @e1
agent-browser wait 800
agent-browser snapshot -i
```

### Falhas Determinísticas Rastreadas no Snapshot `@eX`:
- `[FAIL: DIVSOUP_ACESSIBILIDADE]`: Tags `<div>`/`<span>` simulando botões sem semântica ARIA nem suporte a teclado.
- `[FAIL: NO_INERTE_SEM_ACAO]`: Elementos interativos com `onClick` vazio, `preventDefault()` isolado ou sem mutação observável.
- `[FAIL: ANTI_SQUISH_VIOLADO]`: Botões ou badges sem `flex-shrink: 0; white-space: nowrap;` ou alvos $< 44\times44\text{px}$.

---

## 2. Template Canônico de Relatório de Auditoria (Saída Estruturada)

```markdown
# RELATÓRIO DE AUDITORIA TÉCNICA E VISUAL DO PROJETO

## 1. RESUMO EXECUTIVO & NOTA GERAL
- **Projeto Auditado:** [Nome ou Caminho]
- **Pontuação Consolidada:** [X / 100] -> [Enterprise (90-100) / Moderado (70-89) / Instável (50-69) / Reprovado (<50)]
- **Diagnóstico Síntese:** [2 a 3 frases objetivas]

## 2. AUDITORIA ESTRUTURAL E GOVERNANÇA DE PASTAS (20 pts)
| Arquivo / Pasta Vital | Status | Observação Técnica |
| :--- | :--- | :--- |
| `AGENTS.md` / `README.md` | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `CONTEXT.md` / `SPEC.md` | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `DESIGN.md` (`v4.5-soft`) | `[PASS]` / `[FAIL]` | [Diagnóstico] |
| `.gitignore` & `.env.example` | `[PASS]` / `[FAIL]` | [Verificação de vazamento de segredos/build] |

## 3. COERÊNCIA NARRATIVA: DOCUMENTADO VS. IMPLEMENTADO (20 pts)
| Funcionalidade Declarada | Status | Evidência / Arquivo |
| :--- | :--- | :--- |
| [Recurso X] | `[IMPLEMENTADO_FUNCIONAL]` / `[MOCK_SUPERFICIAL]` / `[INEXISTENTE_DOCUMENTADO]` / `[CÓDIGO_FANTASMA]` | [Caminho] |

## 4. HIGIENE DE CÓDIGO, TIPAGEM, CHUNKING & ARQUIVOS ÓRFÃOS (25 pts)
- **Arquivos/Exports Órfãos:** [Lista]
- **Desacoplamento, Tipagem e Chunking (`source_id`, `chunk_index`, `byte_range`):** [Diagnóstico]

## 5. AUDITORIA VISUAL, DESIGN SYSTEM & NÓS INTERATIVOS (20 pts)
- **Temas, Contraste WCAG e Tipografia (`DESIGN.md v4.5-soft`):** [Diagnóstico]
- **Snapshot Interativo (`agent-browser snapshot -i`):** [Relação de nós `@eX`, `divsoup` e nós inertes]

## 6. SEGURANÇA, GIT & PROTOCOLOS MCP (15 pts)
- **Configuração MCP e Schemas (`extra="forbid"`):** [Diagnóstico]

## 7. PLANO DE AÇÃO IMEDIATO (PRIORIZADO)
1. [Correção Crítica Bloqueante]
2. [Saneamento de Orfandade / UI]
3. [Melhoria Preventiva]
```
