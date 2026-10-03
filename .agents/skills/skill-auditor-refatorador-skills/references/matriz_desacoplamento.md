# MATRIZ DE DESACOPLAMENTO E ESPECIALIZAÇÃO DE SKILLS

Este documento estabelece os padrões arquiteturais de referência para refatoração e desmembramento de habilidades monolíticas em agentes autônomos.

---

## 1. Princípio da Especialização de Componentes

Monólitos em prompts de agentes acumulam múltiplos domínios cognitivos divergentes, levando à degradação de atenção (*attention dispersion*), aumento drástico de alucinações e desperdício de tokens na janela de contexto.

O desacoplamento divide a responsabilidade em papéis atômicos e bem definidos:

| Tipo de Monólito | Problema Típico | Padrão de Desacoplamento Recomendado |
| :--- | :--- | :--- |
| **Planejamento + Diagramação** | Sintaxe Mermaid quebrada, esquecimento de fases | `skill-planejador-estrategico` + `skill-diagramador-visual` |
| **Coleta/Ingestão + Validação** | Dados sujos aceitos sem bloqueio | `skill-extrator-dados` + `skill-validador-schema` |
| **Orquestração + Execução** | Bloqueios não tratados e loops infinitos | `skill-orquestrador-planos` + skills operárias isoladas |
| **Geração de Texto + Formatação PDF** | Erros de script e quebras de página | `skill-redator-markdown` + `skill-conversor-pdf` |

---

## 2. Padrão de Invocação Cruzada (`authorized_sub_skills`)

Ao desacoplar uma funcionalidade secundária de uma skill principal, a skill principal retém a autoridade de invocar a nova sub-skill sob demanda, sem reincorporar seu código ou regras internas.

### Exemplo de Configuração Contratual

No arquivo `SKILL.md` da skill planejadora:

```yaml
---
name: skill-planejador-estrategico
description: >-
  Subagente planejador tático. Decompõe requisitos complexos em fases cronológicas e matrizes de dependência causal.
authorized_sub_skills:
  - name: skill-diagramador-visual
    trigger_condition: "quando o plano exigir fluxograma de processos com mais de 3 nós ou visualização de arquitetura"
    input_contract: "nós, arestas e rótulos estruturados em JSON"
---
```

---

## 3. Fluxo de Transição entre Módulos Desacoplados

O orquestrador intermediará a troca de mensagens para manter o contexto limpo:

```text
[Usuário / Caller]
       │ (Pedido de Planejamento)
       ▼
[skill-planejador-estrategico] ──► Produz fases e identifica necessidade de diagrama
       │
       ▼ (Dispara sob demanda)
[skill-diagramador-visual]     ──► Compila Mermaid TD/LR validado
       │
       ▼ (Retorna artefato validado)
[skill-orquestrador]           ──► Consolida a entrega final
```
