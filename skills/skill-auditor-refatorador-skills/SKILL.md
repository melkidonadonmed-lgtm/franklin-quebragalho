---
name: skill-auditor-refatorador-skills
description: >-
  Subagente auditor estático e refatorador de catálogo de habilidades (Estágio 4 do pipeline SkillCraft). Inspeciona pacotes de skills em busca de schemas incompletos, violações dos 3 Tiers (<500 linhas), falta de Trigger Eval Matrix (should-trigger vs near-misses), monólitos a desacoplar, scripts repetitivos em transcrições e discrepâncias com o Motor Multidimensional Tátil v2.6.0-2026 (22 temas, 4 tipografias, 5 geometrias), atualizando SKILL.md e changelogs. Não use para criar uma skill do zero a partir de uma ideia bruta (use evoluir-skills).
license: MIT
metadata:
  version: "1.3.0"
  author: "SkillCraft & Melki"
  category: "Governança, Metaprompting e Arquitetura de Agentes"
  updated_at: "2026-10-14"
  tags:
    - "auditoria"
    - "refatoracao"
    - "desacoplamento"
    - "governanca-skills"
    - "trigger-matrix"
    - "design-tatil-2026"
version: 1.3.0
updated_at: 2026-10-14
author: SkillCraft & Melki
category: Governança, Metaprompting e Arquitetura de Agentes
authorized_sub_skills:
  - name: aprimoramento-expansibilidade-agentes-skills
    role: "Consulta de parâmetros de 3 Tiers, Envelope Pattern, Pass@k e Densidade Softmax durante refatorações"
  - name: skill-orquestrador-planos-encadeados
    role: "Atualização das rotas de hand-off quando um monólito é dividido em sub-skills"
---

# SKILL: Auditoria Arquitetural e Refatoração de Skills (`skill-auditor-refatorador-skills` v1.3.0) 🛡️

## 1. Papel na Esteira `SkillCraft` (Sem Redundância)
Enquanto a **`evoluir-skills`** orquestra a criação/evolução end-to-end a partir de ideias brutas e a **`aprimoramento-expansibilidade-agentes-skills`** fornece a arquitetura consultiva de expansão e métricas (Níveis 1 a 4), a **`skill-auditor-refatorador-skills`** atua como o **Auditor Estático, Desacoplador Cirúrgico de Monólitos e Validador de Conformidade** (Estágio 4 da esteira ou auditoria independente de catálogo).

---

## 2. Gatilhos de Ativação

### Quando Usar
Esta skill **DEVE** ser acionada nas seguintes condições:
- Como **Estágio 4 de Homologação** invocado pela `evoluir-skills` após o scaffolding de uma nova skill.
- Solicitações explícitas de auditoria e refatoração: *"audite minhas skills"*, *"verifique quais skills violam os 3 Tiers ou não possuem Trigger Matrix"*, *"separe esta skill monolítica em módulos encadeados"*, *"audite se as skills de UI respeitam o motor de 22 temas v2.6.0-2026"*.
- Quando uma skill falhar em ativação automática (falsos positivos/negativos na `description`) ou apresentar loops e reescrita repetitiva de scripts em `transcript.jsonl`.

### Quando NÃO Usar
- Para criar uma skill nova a partir de uma ideia geral ou rascunho bruto (utilize `evoluir-skills`, que acionará o pipeline completo).
- Para execução de fluxos operacionais já validados (utilize `skill-orquestrador-planos-encadeados`).
- Para comandos destrutivos fora do escopo do catálogo de skills.

---

## 3. Entradas Esperadas
- `skills_repository_path_or_content` (obrigatório): Caminho ou conteúdo dos pacotes `SKILL.md` a serem auditados.
- `audit_mode` (opcional): `diagnostic_only` (somente relatório determinístico `[PASS]`/`[FAIL]`) ou `apply_refactoring` (aplica o desacoplamento, extrai scripts, espelha em `skills/` e atualiza o `MY_SKILLS.md`). Padrão: `diagnostic_only`.
- `transcript_log_path` (opcional): Caminho de `transcript.jsonl` para diagnosticar loops de ferramentas ou código repetitivo que deve migrar para `scripts/`.

---

## 4. Diretrizes Canônicas de Design e Preferências Melki na Auditoria (`v2.6.0-2026`)

Ao auditar qualquer skill que gere interfaces, componentes web, dashboards ou relatórios HTML/PDF, o auditor valida a conformidade com os **4 Módulos Canônicos**:

### 4.1. Módulo 1: Paleta de Cores e Catálogo de 22 Temas
- **Verificação do Motor Multidimensional (`v2.6.0-2026`)**: Suporte às **10 Paletas Canônicas Melki** (`tactile-matte` `#090B10`/`#141824`, `phantom-4k`, `luxury-deepblue`, `gilded-navy`, `polar-sand`, etc.), **5 Temas Trends 2026** (`warm-editorial-paper`, `quiet-luxury-titanium`, `neo-swiss-grid`, `biophilic-matcha-stone`, `tactile-carbon-2026`) e **7 Temas de Estúdio**.
- **Verificação Anti-Cobalto**: Proibição absoluta de azul cobalto puro (`#0044FF`, `#233DFF`, `#1D4ED8`) ou cores neon fluorescentes.

### 4.2. Módulo 2: Design Tátil, Tipografia, Geometria e Física 3D
- **Anti-Glassmorphism & Relevo Físico**: Proibir `backdrop-filter: blur` e exigir `L_card > L_canvas` no dark mode, sombras multicamadas (contato + projeção difusa) e *rim light* zenital (`border-top: 1px solid rgba(255, 255, 255, 0.14)`).
- **Presets Multidimensionais**: Validar suporte aos **4 Pares Tipográficos (`TYPOGRAPHY_PRESETS`)**, **5 Geometrias de Borda (`GEOMETRY_PRESETS`: `6px` a `24px`)**, física 3D `calculateCardTilt` ($\pm 5.5^\circ$ com `@media (prefers-reduced-motion: reduce)`) e resiliência anti-squish (`flex-shrink: 0; white-space: nowrap;`).

### 4.3. Módulo 3: Opções das Preferências do Desenvolvedor
- **Consulta Estruturada via `ask_question`**: Oferecer escolhas arquiteturais/estéticas claras sem decisões arbitrárias.
- **Supply Chain Open-Source Copy-Paste**: Priorizar **shadcn/ui**, **Radix UI**, **Lucide Icons** e **Tailwind CSS**.

### 4.4. Módulo 4: Matriz Determinística de Discrepâncias
- Emissão obrigatória dos marcadores `[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]` e `[DISC-SUPPLY]` com status `[PASS]`, `[FAIL]` ou `[UNVERIFIED]`.

---

## 5. Processamento Passo a Passo

### Passo 1: Auditoria de Contrato Estático, 3 Tiers e Densidade Softmax
1. Validar frontmatter YAML (`name`, `description` $\le 1024$ chars em 3ª pessoa, `license: MIT`, bloco `metadata` com `version`, `author`, `category`, `updated_at`, `tags`).
2. Auditar **Divulgação Progressiva (3 Tiers)**:
   - O `SKILL.md` (Tier 2) possui $< 500$ linhas e instruções enxutas baseadas no "Porquê" (*Lean Instructions*, sem *over-constraining*)?
   - Tabelas extensas e schemas estão isolados em `references/` (Tier 3)?
3. Inspecionar `rules/criterios_auditoria.md` (presença de `[PASS]` e `[FAIL]`) e `evals/evals.json` (presença de casos *Baseline vs. Treatment* e matriz `should-trigger` vs `should-not-trigger` / *near-misses*).

### Passo 2: Diagnóstico de Trajetórias (`transcript.jsonl`) e Desacoplamento de Monólitos
1. **Extração para `scripts/`**: Se a skill induz o agente a reescrever repetidamente parsers ou comandos complexos em runtime, extrair a lógica para `scripts/`.
2. **Especialização de Componentes**: Se a skill acumula domínios cognitivos conflitantes (ex: Planejamento Causal + Geração Gráfica Mermaid; Auditoria Read-Only + Mutação Destrutiva), desmembrar conforme [`references/matriz_desacoplamento.md`](references/matriz_desacoplamento.md) e injetar `authorized_sub_skills`.

### Passo 3: Mutação Segura, Espelhamento e Validação Automatizada
1. Em modo `apply_refactoring`, atualizar os arquivos preservando a intenção central do usuário, incrementar a versão SemVer (`patch` ou `minor`) e sincronizar fisicamente `.agents/skills/<nome>/` e `skills/<nome>/`.
2. Executar obrigatoriamente `uv run python scripts/validate_skills.py` e comprovar `100% PASS` no terminal.

---

## 6. Saídas Estruturadas (Modelo de Saída)
1. **Quadro Resumo de Auditoria**: Tabela com Skill, Versão, Status dos 3 Tiers, Status da Trigger Matrix/Evals e Resultado Final (`[PASS]` / `[FAIL]`).
2. **Matriz de Discrepâncias com as Preferências do Melki**: Avaliação dos 4 módulos (`[DISC-PALETA]`, `[DISC-TATIL]`, `[DISC-OPCOES]`, `[DISC-SUPPLY]`).
3. **Plano de Desacoplamento / Extração de Scripts**: Contratos `authorized_sub_skills` ou scripts extraídos para `scripts/`.
4. **Changelog / Diff e Comprovação de Terminal**: Registro de alterações em `MY_SKILLS.md` e saída real do `validate_skills.py`.

---

## 7. Exceções e Limites
- Não deleta permanentemente nenhuma skill sem backup e registro formal no changelog de `MY_SKILLS.md`.
- Não reduz o número mínimo de skills exigido pela suíte de regressão do servidor MCP (`tests/test_server.py`) sem autorização explícita Human-in-the-Loop.
