# Ondas, Penalidades e Card de Diagnóstico — `code-quality-audit-3d-physics`

Referência operacional das 3 ondas e penalidades consumida por [`../SKILL.md`](../SKILL.md), complementando [`subskill_modules_spec.md`](subskill_modules_spec.md), [`dossie_auditoria_qualidade_codigo_3d.md`](dossie_auditoria_qualidade_codigo_3d.md), [`estrutura_pontuacao_fisica_3d.md`](estrutura_pontuacao_fisica_3d.md) e [`observer_agent_spec.yaml`](observer_agent_spec.yaml).

## Topologia Envelope 3+1+1

```text
┌───────────────────────────────────────────────────────────────────────────┐
│        ORQUESTRADOR: code-quality-audit-3d-physics (Topologia 3+1+1)      │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│ ONDA 1 - MÓDULO 1 │       │ ONDA 1 - MÓDULO 2 │       │ ONDA 1 - MÓDULO 3 │
│ Sanitização & AST │       │ Arquitetura &     │       │ Física 3D & Math  │
│ (w1 = 20% | s1)   │       │ Hardcoded (w2=15%)│       │ (w3 = 25% | s3)   │
└─────────┬─────────┘       └─────────┬─────────┘       └─────────┬─────────┘
          └───────────────────────────┼───────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ ONDA 2 - MÓDULO 4: deterministic-tests-auditor (w4 = 20% | s4)            │
│ • FPS Independence (60Hz vs 120Hz) • Conservação de Energia • Anti-NaN    │
│ • Prevenção de Tunneling (CCD)     • Reprodutibilidade Pass@k (k=10)      │
└─────────────────────────────────────┬─────────────────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│ ONDA 3 - MÓDULO 5 (GATEKEEPER): state-checker-observer (w5 = 20% | s5)    │
│ • Validação Cruzada no Código-Fonte (Descarte de Falsos Positivos)        │
│ • Cálculo de S1..S5 e Escore Global Snorm • Emissão do Relatório Final    │
└───────────────────────────────────────────────────────────────────────────┘
```

## Penalidades por Módulo e Testes Dinâmicos

- **Onda 1 — AST:**
  - **Módulo 1 (`static-sanitization-auditor`, $w_1 = 20\%$):** `ALLOC_IN_LOOP` ($-30$), `DUPLICATE_FUNCTION` ($-20$), `DEAD_CODE_FUNCTION` ($-10$), `UNUSED_VARIABLE` ($-5$).
  - **Módulo 2 (`architecture-hardcoded-auditor`, $w_2 = 15\%$):** `PHYSICS_RENDER_COUPLING` ($-35$), `RIGID_CONSTRUCTOR` ($-15$), `HARDCODED_MAGIC_NUMBER` ($-10$).
  - **Módulo 3 (`physics-3d-math-auditor`, $w_3 = 25\%$ e $S_1..S_5$):** `MISSING_DELTA_TIME` ($-40$ em $s_3$ / $-100$ em $S_1$), `UNCHECKED_NORMALIZE` ($-25$ / $-40$ $S_2$), `EULER_GIMBAL_LOCK` ($-20$ / $-50$ $S_2$), `STRICT_FLOAT_COMPARE` ($-15$ / $-40$ $S_5$), `MISSING_DAMPING` ($-15$ / $-30$ $S_3$).
- **Onda 2 — 5 Testes (`physics_test_runner.py`, $s_4 = \frac{\text{Pass}}{5} \times 100$):** `TEST_FPS_INDEPENDENCE` (`< 0.1m` 60Hz vs 120Hz), `TEST_ENERGY_CONSERVATION` ($E_{\text{final}} \le E_{\text{inicial}}$), `TEST_NAN_IMMUNITY` (vetor nulo sem `NaN`/`Inf`), `TEST_COLLISION_TUNNELING` (`-100 m/s` via CCD/substepping), `TEST_DETERMINISM_PASS_AT_K` ($Pass@10$ 100%).
- **Cards de Diagnóstico (`🚨 [ERR-XXX / ID_PROBLEMA]`):** Dimensão, Severidade, `arquivo:linha`, Veredito do Observador + `1. Causa Raiz`, `2. Melhor Correção com Código`, `3. Métrica Esperada`.
