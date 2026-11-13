---
name: re-a-ndroid
description: "Engenharia reversa e auditoria de APKs Android com re-a-ndroid, REA e ADB descompilando DEX .so, assinaturas v1-v3.1, funções placebo, latência de rotas e alvos 48dp. Use para auditar APKs; não use para criar MVP."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "2.2.0"
  updated_at: "2026-11-13"
  author: "arq-software-team & melki-agent-os"
  category: "android-security-auditing"
  tags: ["android-reverse-engineering", "rea", "adb", "apk-signature", "dex-audit", "a11y-48dp"]
---

# `re-a-ndroid` — Auditoria Android com REA, CoT, ReAct & Self-Refine

## 1. Propósito e Gatilhos (Quando Usar)

Protocolo de engenharia reversa, segurança binária/rede, acessibilidade e performance Android integrando **REA (`Reverse Engineer Anything`)**, **ADB**, **CoT**, **ReAct**, **Self-Refine** e auditoria WebSocket/JSON-RPC ([`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md)):

- Dissecação estática de `.apk`/`.aab`, DEX, `lib/*.so`, engines (`Flutter`/`Dart AOT`, `Unity IL2CPP`), assinaturas v1–v3.1 e `AndroidManifest.xml`.
- Inspeção dinâmica ADB (`am start -W`, `uiautomator dump`, `dumpsys meminfo/gfxinfo`, `logcat *:E`), caça a **funções placebo**, CVEs Gradle/Maven e alvos `48x48dp`.

## 2. Entradas, Pré-requisitos e Ciclo Cognitivo

- **`apk_or_project_path` (obrigatório):** Caminho de `.apk`/`.aab` ou raiz do projeto Android.
- **`package_name` / `launcher_activity` (opcional):** Identificadores para instrumentação ADB.
- **`rea_detail` (opcional):** `"summary"` (padrão para economia de contexto) ou `"full"`.
- **Ciclo:** `0. Pre-Flight Condicional (Gemini API / WS)` $\to$ `1. CoT` $\to$ `2. ReAct (REA + ADB + OSV.dev)` $\to$ `3. Self-Refine`.

## 3. Processamento e Fluxo em 5 Etapas (8 Módulos)

Consulte a matriz completa e fórmulas em [`references/protocolo_5_etapas_e_metricas.md`](references/protocolo_5_etapas_e_metricas.md) e [`references/matriz_8_modulos_e_laudo.md`](references/matriz_8_modulos_e_laudo.md):

1. **Etapa 1 — Ingestão & Descompilação (REA):** Execute `inspect_android_package(detail="summary")`, `inspect_apk_signature` + `inspect_analysis_view(kind="apk-signature", detail="summary")` (nunca `inspect_signature`, exclusivo de Mach-O), `decode_android_resources` e `project_android_application_graph`. Em engines nativas, use `identify_flutter_build`/`inspect_dart_aot`/`inspect_il2cpp_metadata`; em timeout do JADX, ajuste `jadx.operation_timeout_ms` via `update_analysis_settings` e isole `_meta.provenance.untrusted_content == true`.
2. **Etapa 2 — Dinâmica & UI (ADB):** Coletar `adb shell am start -W -n "[PKG]/[ACTIVITY]"`, `uiautomator dump /sdcard/window_dump.xml` e `dumpsys gfxinfo "[PKG]" framestats`.
3. **Etapa 3 — Rede (`HTTPS`/`WSS`/`JSON-RPC`) & Placebos:** Se integrar Gemini API/Live, consultar `google-developer-knowledge` ou `gemini_get_doc` (`aistudio.google.com/llms.txt`; evite `gemini_search_docs`, desabilitada); se usar WS/JSON-RPC, aplicar `audit-websocket-jsonrpc.md` (`TLS 1.3`, `Network Security Config`, Ephemeral Tokens, $RTT_{\text{avg}} < 150\text{ms}$); auditar `isRooted`/`verifyToken`/`checkServerTrusted` via `inspect_android_method`.
4. **Etapa 4 — CVEs (ReAct):** Cruzar `libs.versions.toml`/`build.gradle.kts` com OSV.dev/NVD.
5. **Etapa 5 — Síntese (`scripts/rea_android_auditor.py`):** Calcular os 6 indicadores ($\text{Pass}@k$, $L_{\text{cold}}$, $M_{\text{rotas}}$, $A_{\text{rate}}$, $T_{\text{ratio}}$, $\text{FNR} < 0.001$) com `Evidence-ID`.

## 4. Saídas e Entregáveis

Laudo Self-Refine conforme [`references/matriz_8_modulos_e_laudo.md`](references/matriz_8_modulos_e_laudo.md): (1) Metadados e Assinatura, (2) Achados (`SEC-*`, `PLC-*`, `ACC-*`, `PERF-*`, `NAV-*`) com `Evidence-ID`, (3) 6 Métricas e (4) Patch para o *Deep Coder*.

## 5. Exceções, Limites e Quando NÃO Usar

- **Scaffolding Android Greenfield:** Não use para criar MVPs do zero em Kotlin 2.4 / Compose BOM `2026.09.00` (use `android-agy-projects`).
- **Frontend Web Puro:** Não use para React/Next.js/CSS (use `plan-uiux`, `complex-zero` ou `frontend-testing-auditor`).
- **Guardrails ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Zero confiança textual (*Read-After-Write* obrigatório), preservar `minSdk`/`targetSdk`/assinaturas e respeitar *Air-Gap Sandbox* com capturas locais.
