---
name: code-quality-audit-3d-physics
description: >-
  Audita e sanitiza código de sistemas com Física 3D, Computação Gráfica (WebGL, Three.js, Babylon.js) e Engenharia Numérica (Python, JS/TS). Orquestra 5 módulos de subskills em 3 ondas (static-sanitization-auditor, architecture-hardcoded-auditor, physics-3d-math-auditor, deterministic-tests-auditor e state-checker-observer), calcula as 5 sub-dimensões de física (S1..S5), executa testes determinísticos Pass@k (k=10) e emite o Escore Normalizado Global Snorm (0 a 100) com filtro anti-alucinação.
license: MIT
metadata:
  version: "1.0.0"
  author: "Franklin-Main & Melki"
  category: "Auditoria de Código, Física 3D e Simulação Numérica"
  updated_at: "2026-10-15"
  tags:
    - "fisica-3d"
    - "auditoria-codigo"
    - "ast-parser"
    - "threejs"
    - "webgl"
    - "testes-deterministicos"
    - "pass-at-k"
    - "snorm"
version: 1.0.0
updated_at: 2026-10-15
author: Franklin-Main & Melki
category: Auditoria de Código, Física 3D e Simulação Numérica
---

# 1. NOME DA SKILL
`code-quality-audit-3d-physics` — Auditoria de Qualidade de Código, Sanitização Estática, Física 3D e Testes Determinísticos (Topologia 3+1+1)

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)
Ative esta skill quando o usuário solicitar:
- "Audite a física 3D, animações WebGL/Three.js ou simulação numérica deste código"
- "Verifique alocações de memória no laço de renderização (`ALLOC_IN_LOOP`), falta de `deltaTime` (`dt`) ou *Gimbal Lock*"
- "Execute os parsers AST (`static_ast_parser.py` / `js_ts_ast_parser.js`) e o runner de testes determinísticos (`physics_test_runner.py`)"
- "Calcule o Escore Normalizado Ponderado Global ($S_{\text{norm}}$) e a pontuação das 5 sub-dimensões de Física 3D ($s_{\text{Física}}$)"
- "Rode o observador `state-checker-observer` para validar alertas estáticos e eliminar falsos positivos"

---

## 3. LIMITES, EXCEÇÕES E QUANDO NÃO USAR
- **Não usar** para auditoria geral de governança de pastas Git/README/`.env` de repositórios web comuns sem motor numérico/3D (use `auditoria-projetos-sistema`).
- **Não usar** para consultoria puramente estética de cores/tipografia CSS sem relação com performance de loop, física 3D ou higiene de código (use `analise-design-tatil-frontend` ou `consultor-design-tatil-frontend`).
- **Não aplicar** mutações destrutivas no código-fonte auditado sem antes apresentar o Relatório Consolidado do Observador e obter aprovação do desenvolvedor.

---

## 4. ENTRADAS E PRÉ-REQUISITOS
- `target_path` (obrigatório): Caminho do arquivo (`.py`, `.js`, `.ts`, `.tsx`) ou diretório do motor físico/3D a ser auditado.
- `step_function` (opcional): Nome da função de passo de simulação física (ex: `step_physics_good`, `update`, `integrate`) para injeção no `physics_test_runner.py`.
- `output_format` (opcional): `markdown` (padrão executivo com templates de erro `🚨 [ERR-XXX]`) ou `json` (para integração em pipelines/DAG).

---

## 5. PROCESSAMENTO INTERNO E FLUXO DE EXECUÇÃO (3 ONDAS)

A execução opera sob o **Padrão Envelope em 3 Ondas**, coordenando os **5 Módulos de Subskills** documentados em [references/subskill_modules_spec.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/references/subskill_modules_spec.md) e [references/dossie_auditoria_qualidade_codigo_3d.md](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/references/dossie_auditoria_qualidade_codigo_3d.md) (ou via `franklin_execute_dag(plan_path_or_json="physics", target_dir="<caminho_arquivo>")`):

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

### Passo 1: Onda 1 — Varredura Estática de AST (Módulos 1, 2 e 3)
- Para arquivos Python (`.py`), execute [scripts/static_ast_parser.py](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/scripts/static_ast_parser.py):
  ```powershell
  uv run python skills/code-quality-audit-3d-physics/scripts/static_ast_parser.py <caminho_arquivo.py>
  ```
- Para arquivos JavaScript/TypeScript (`.js`, `.ts`), execute [scripts/js_ts_ast_parser.js](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/scripts/js_ts_ast_parser.js):
  ```powershell
  node skills/code-quality-audit-3d-physics/scripts/js_ts_ast_parser.js <caminho_arquivo.ts>
  ```
- **Regras Verificadas na Onda 1**:
  - **Módulo 1 (`static-sanitization-auditor`, $w_1 = 20\%$):** `ALLOC_IN_LOOP` ($-30$), `DUPLICATE_FUNCTION` ($-20$), `DEAD_CODE_FUNCTION` ($-10$), `UNUSED_VARIABLE` ($-5$).
  - **Módulo 2 (`architecture-hardcoded-auditor`, $w_2 = 15\%$):** `PHYSICS_RENDER_COUPLING` ($-35$), `RIGID_CONSTRUCTOR` ($-15$), `HARDCODED_MAGIC_NUMBER` ($-10$).
  - **Módulo 3 (`physics-3d-math-auditor`, $w_3 = 25\%$ e Sub-dimensões $S_1..S_5$):** `MISSING_DELTA_TIME` ($-40$ em $s_3$ / $-100$ em $S_1$), `UNCHECKED_NORMALIZE` ($-25$ em $s_3$ / $-40$ em $S_2$), `EULER_GIMBAL_LOCK` ($-20$ em $s_3$ / $-50$ em $S_2$), `STRICT_FLOAT_COMPARE` ($-15$ em $s_3$ / $-40$ em $S_5$), `MISSING_DAMPING` ($-15$ em $s_3$ / $-30$ em $S_3$).

### Passo 2: Onda 2 — Suíte de Testes Determinísticos em Tempo de Execução (Módulo 4)
- Execute [scripts/physics_test_runner.py](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/scripts/physics_test_runner.py):
  ```powershell
  uv run python skills/code-quality-audit-3d-physics/scripts/physics_test_runner.py --target <caminho_arquivo.py> --json
  ```
- Avalia as 5 baterias dinâmicas ($s_4 = \frac{\text{Testes Aprovados}}{5} \times 100$):
  1. `TEST_FPS_INDEPENDENCE` (60Hz vs 120Hz, divergência $< 0.1\text{m}$).
  2. `TEST_ENERGY_CONSERVATION` ($E_{\text{final}} \le E_{\text{inicial}}$).
  3. `TEST_NAN_IMMUNITY` (Vetor nulo sem gerar `NaN` ou `Inf`).
  4. `TEST_COLLISION_TUNNELING` (Retenção de projétil a $-100\text{ m/s}$ via CCD/substepping).
  5. `TEST_DETERMINISM_PASS_AT_K` ($Pass@10$ com $100\%$ de convergência de hash de estado).

### Passo 3: Onda 3 — Validação Cruzada e Consolidação pelo Observador (Módulo 5)
- Para executar as 3 ondas integradas com o filtro anti-alucinação e gerar o relatório consolidado, dispare diretamente [scripts/state_checker_observer.py](file:///c:/Users/melki/dev/repos/franklin-quebragalho/skills/code-quality-audit-3d-physics/scripts/state_checker_observer.py) ou acione o DAG no Epic-Volta via `franklin_execute_dag(plan_path_or_json="physics", target_dir="<caminho_arquivo>")`:
  ```powershell
  uv run python skills/code-quality-audit-3d-physics/scripts/state_checker_observer.py <caminho_arquivo>
  ```
- O Observador recalcula $S_{\text{norm}}$ pela equação canônica:
  $$S_{\text{norm}} = 0.20 \cdot s_1 + 0.15 \cdot s_2 + 0.25 \cdot s_3 + 0.20 \cdot s_4 + 0.20 \cdot s_5$$

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A entrega ao usuário deve conter obrigatoriamente:
1. **Cabeçalho Executivo e Escore Normalizado Final ($S_{\text{norm}}$ / 100)** com Breakdown dos 5 Módulos ($s_1..s_5$).
2. **Tabela das 5 Sub-dimensões Internas de Física 3D ($S_1..S_5$)** com pesos ($25\%, 25\%, 20\%, 15\%, 15\%$) e status determinístico (`[PASS]` / `[FAIL]`).
3. **Tabela de Resultados dos 5 Testes Determinísticos (`Pass@10`)**.
4. **Cards de Diagnóstico Padronizados (`🚨 [ERR-XXX / ID_PROBLEMA]`)** contendo:
   - Dimensão atingida, Severidade, Localização (`arquivo:linha`) e Veredito do Observador;
   - **1. Descrição Detalhada do Problema e Causa Raiz**;
   - **2. A MELHOR Forma de Resolver e Justificativa Técnica** (com bloco de código refatorado);
   - **3. Resultado Esperado Após a Correção** (métrica quantitativa verificável).
