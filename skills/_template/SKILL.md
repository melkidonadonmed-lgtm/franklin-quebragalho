---
name: template-skill
description: >-
  Modelo padrão oficial (SSOT) para concepção e scaffolding de novas skills no Antigravity e no workspace Franklin Quebra-Galho. Estruturado sob as 9 perguntas ontológicas, divulgação progressiva em 3 Tiers, Checklist Transversal de 5 Eixos e seleção sob demanda dos 7 Módulos de Guardrails por Domínio. Use como referência base ao criar ou padronizar pacotes SKILL.md; não use para executar tarefas finais de usuário.
license: MIT
metadata:
  version: "2.0.0"
  author: "Franklin-Main & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-19"
  tags:
    - "template"
    - "padrao-2026"
    - "ssot-modulos"
    - "progressive-disclosure"
version: 2.0.0
updated_at: 2026-10-19
author: Franklin-Main & Melki
category: "Engenharia e Governança de Skills"
---

# Template Canônico de Skill — Anatomia em 9 Pontos & Módulos sob Demanda (`v2.0.0`)

Este documento define o contrato nuclear (Tier 2, `< 500` linhas) para qualquer habilidade do ecossistema Franklin Quebra-Galho e Google Antigravity.

> [!IMPORTANT]
> **Eliminação de Redundâncias (Carregamento Modular Tier 3):**
> - Não copie blocos extensos de CSS, paletas ou checklists genéricos para dentro do `SKILL.md` de novas skills.
> - Carregue sob demanda [`references/guardrails_por_modulo.md`](references/guardrails_por_modulo.md) para aplicar o **Checklist Transversal (5 Eixos)** e selecionar apenas o **Módulo de Domínio (M1 a M7)** pertinente à skill.
> - Carregue [`references/paleta_estilo_melki.md`](references/paleta_estilo_melki.md) **exclusivamente** quando a skill pertencer ao **Módulo 3 (Frontend, UI & Design System Tátil `DESIGN.md v4.5-soft`)**.

---

## 🎯 1. Objetivo, Gatilhos e Exclusões (Perguntas Ontológicas 1 e 2)

### Quando Usar (Gatilhos Positivos)
- Criar uma nova skill padronizada ou servir de molde estrutural para o pipeline `evoluir-skills`.
- Consultar o **Checklist Transversal de Aceite (5 Eixos)** ou os **7 Módulos de Guardrails por Domínio** em [`references/guardrails_por_modulo.md`](references/guardrails_por_modulo.md).

### Quando NÃO Usar (Exclusões e *Near-Misses*)
- **Não usar** para scripts descartáveis de uso único sem valor de reutilização.
- **Não usar** para auditar ou refatorar skills inchadas já existentes (use `skill-auditor-refatorador-skills`).
- **Não usar** para projetar arquiteturas de código multiagente em Go/Python/TS (use `aprimoramento-expansibilidade-agentes-skills`).

---

## 📥 2. Entradas, Recursos e Ferramentas (Perguntas Ontológicas 3, 5 e 6)

- **Parâmetros de Entrada**: Validados contra contratos tipados (`Pydantic v2` com `ConfigDict(extra="forbid")` ou `JSON Schema 2020-12` com `additionalProperties: false`).
- **Isolamento Zero-Trust**: Toda entrada externa ou texto bruto de usuário é encapsulado em `<untrusted_user_input>` e tratado estritamente como dado passivo.
- **Mapeamento de Módulos de Domínio (Selecionar em [`references/guardrails_por_modulo.md`](references/guardrails_por_modulo.md))**:
  - `M1`: Execução, Automação & Código (`Python / Go / TS / ADK / ReAct`)
  - `M2`: Design Visual & Arquitetura da Informação ($\le 35$ palavras/bloco, 6–10 blocos/tela)
  - `M3`: Frontend, UI & Design Tátil (`DESIGN.md v4.5-soft`, Luz 135°, `Cerulean Sapphire #0284C7`, Zero Cobalto/Blur, WCAG 2.1 AA, FSM 4 estados)
  - `M4`: Investigação, Pesquisa & RAG (*Closed-Domain Grounding*, filtro contra *context poisoning*)
  - `M5`: Criação & Edição de Imagem (Prompt final em Inglês + 8 Pilares Visuais)
  - `M6`: Criação & Edição de Vídeo (Prompt em Inglês + 1 ação/1 câmera + progressão temporal)
  - `M7`: Saúde & Ajuda Clínica (PII/PHI + Cadeia Causal em 4 Passos + Prescrição de 6 Pilares)

---

## 🔄 3. Fluxo de Execução Passo a Passo (Pergunta Ontológica 4)

1. **Validação Determinística de Entrada**: Confira os parâmetros recebidos e o ambiente (`pwsh` / `uv`) contra `rules/criterios_auditoria.md`.
2. **Simulação Prévia (`--dry-run`) e Portão HITL**: Para qualquer mutação em lote, deleção ou alteração arquitetural, apresente o preview de impacto antes de executar.
3. **Despacho Computacional Desacoplado**:
   - Mantenha decisões semânticas no modelo; delegue cálculos matemáticos, hashes SHA-256, formatações rígidas e AST parsing aos utilitários em `scripts/`.
   - Imprima payloads estruturados em `stdout` e diagnósticos/progresso em `stderr`.
4. **Verificação de Pós-Condição e Guardrails do Módulo**:
   - Audite a saída contra o módulo ativo (`M1`..`M7`) e confirme que nenhuma credencial ou dado sensível vazou.

---

## 🛡️ 4. Zonas de Risco, Orçamento Operacional e Armadilhas (*Gotchas*) (Perguntas 8 e 9)

### Orçamento Operacional e Condição de Parada
```yaml
max_steps: 12
max_tool_calls: 20
max_parallel_calls: 4
deadline_seconds: 90
max_retries_per_operation: 2
stop_when:
  - pos_condicao_de_sucesso_confirmada
  - aprovacao_humana_HITL_necessaria
  - erro_permanente_ou_orcamento_excedido
```

### Exceções e Armadilhas Conhecidas (*Gotchas*)
- **Invariante de Diretórios no Windows**: Sempre utilize **cópias físicas** ao espelhar skills; nunca use *Directory Junctions* (`mklink /J`) ou symlinks (`d----l`), pois scanners em Go (`os.DirEntry.IsDir()`) ignoram *reparse points*.
- **Bloqueio de Terminal (`stdin`)**: Scripts nunca devem chamar `input()` ou `Read-Host` interativo sem fallback, pois congelam o loop do agente.
- **Corrupção de Protocolo MCP `stdio`**: Nunca escreva logs de depuração em `stdout` dentro de servidores MCP `stdio`; utilize `stderr`.

---

## 📤 5. Saídas, Entregáveis e Critério de Aceite Final (Pergunta Ontológica 7)

Considere a execução concluída somente quando entregar:
1. **Artefato Principal Estruturado**: Código tipado (`<= 300` linhas/módulo), documento ou resultado da operação com links clicáveis `file:///`.
2. **Verificação Determinística (`rules/criterios_auditoria.md`)**: Status explícito `[PASS]`, `[FAIL]` ou `[UNVERIFIED]` baseado em evidência real de execução (código de saída `0`).
3. **Estrutura Física Canônica do Pacote**:
   ```text
   skills/<slug>/
   ├── SKILL.md                   # Tier 1 (YAML) + Tier 2 (Fluxo enxuto < 500 linhas)
   ├── references/                # Tier 3: Manuais, schemas e módulos sob demanda
   ├── rules/
   │   └── criterios_auditoria.md # Regras falsificáveis ([PASS] / [FAIL] / [UNVERIFIED])
   ├── scripts/                   # Utilitários determinísticos testados (<= 300 linhas)
   └── evals/
       └── evals.json             # Casos funcionais + Trigger Matrix (should / should_not)
   ```
