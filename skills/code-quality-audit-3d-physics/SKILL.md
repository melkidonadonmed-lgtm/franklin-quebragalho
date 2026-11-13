---
name: code-quality-audit-3d-physics
description: "Audita e sanitiza código de Física 3D, Computação Gráfica WebGL Three.js Babylon.js, shaders, colisões e nota Snorm Pass@10. Use para revisar motores 3D e simulação; não use para CRUD web."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "1.0.0"
  updated_at: "2026-11-13"
  author: "Franklin-Main & Melki"
  category: "Auditoria de Código, Física 3D e Simulação Numérica"
  tags: ["fisica-3d", "auditoria-codigo", "ast-parser", "threejs", "webgl", "testes-deterministicos", "pass-at-k", "snorm"]
---

# `code-quality-audit-3d-physics` — Auditoria 3D/WebGL e Física Numérica

## 1. Propósito e Gatilhos (Quando Usar)

Orquestra em **Topologia Envelope 3+1+1** a auditoria estática e dinâmica de motores de Física 3D, WebGL/Three.js/Babylon.js e simulação numérica:

- Detectar `ALLOC_IN_LOOP`, acoplamento física-render, falta de `deltaTime`, *Gimbal Lock*, `normalize` sem guarda e comparação estrita de floats.
- Executar os parsers AST (`static_ast_parser.py` / `js_ts_ast_parser.js`), testes determinísticos (`physics_test_runner.py`, `Pass@10`) e filtro anti-falsos-positivos (`state_checker_observer.py`).

## 2. Entradas e Pré-requisitos

- **`target_path` (obrigatório):** Arquivo (`.py`, `.js`, `.ts`, `.tsx`) ou diretório do motor 3D/físico.
- **`step_function` (opcional):** Nome da função de passo (`step_physics_good`, `update`, `integrate`).
- **`output_format` (opcional):** `markdown` (padrão) ou `json`.

## 3. Processamento em 3 Ondas e Execução CLI

Consulte o diagrama, pesos e penalidades em [`references/ondas_e_penalidades_3d.md`](references/ondas_e_penalidades_3d.md), [`references/subskill_modules_spec.md`](references/subskill_modules_spec.md), [`references/dossie_auditoria_qualidade_codigo_3d.md`](references/dossie_auditoria_qualidade_codigo_3d.md), [`references/estrutura_pontuacao_fisica_3d.md`](references/estrutura_pontuacao_fisica_3d.md) e [`references/observer_agent_spec.yaml`](references/observer_agent_spec.yaml):

```powershell
uv run python skills/code-quality-audit-3d-physics/scripts/static_ast_parser.py <caminho_arquivo.py>
node skills/code-quality-audit-3d-physics/scripts/js_ts_ast_parser.js <caminho_arquivo.ts>
uv run python skills/code-quality-audit-3d-physics/scripts/physics_test_runner.py --target <caminho_arquivo.py> --json
uv run python skills/code-quality-audit-3d-physics/scripts/state_checker_observer.py <caminho_arquivo>
```

Ou via DAG: `franklin_execute_dag(plan_path_or_json="physics", target_dir="<caminho_arquivo>")`.

$$S_{\text{norm}} = 0.20 \cdot s_1 + 0.15 \cdot s_2 + 0.25 \cdot s_3 + 0.20 \cdot s_4 + 0.20 \cdot s_5$$

## 4. Saídas e Entregáveis

1. Cabeçalho executivo com $S_{\text{norm}} / 100$ e breakdown $s_1..s_5$ ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)).
2. Tabela das sub-dimensões $S_1..S_5$ ($25\%, 25\%, 20\%, 15\%, 15\%$) e dos 5 testes (`Pass@10`).
3. Cards `🚨 [ERR-XXX / ID_PROBLEMA]` com `arquivo:linha`, causa raiz, código refatorado e métrica verificável.

## 5. Exceções, Limites e Quando NÃO Usar

- **Repositórios CRUD/Web Comuns:** Não use sem motor físico/numérico (use `auditoria-projetos-sistema`).
- **Estética CSS Pura:** Não use para cores/tipografia sem loop físico (use `frontend-ui-ux-auditor` ou `plan-uiux`).
- **Aprovação para Mutações:** Nunca aplique alterações destrutivas sem apresentar o Relatório do Observador e obter aprovação humana.
