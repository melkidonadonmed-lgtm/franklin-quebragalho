---
name: re-a-ndroid
description: "Engenharia reversa e auditoria de APKs Android com re-a-ndroid, REA e ADB descompilando DEX .so, assinaturas v1-v3.1, funções placebo, latência de rotas e alvos 48dp. Use para auditar APKs; não use para criar MVP."
version: "2.2.0"
updated_at: "2026-11-12"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "2.2.0"
  updated_at: "2026-11-12"
  author: "arq-software-team & melki-agent-os"
  category: "android-security-auditing"
  tags: ["android-reverse-engineering", "rea", "adb", "apk-signature", "dex-audit", "a11y-48dp"]
---
# Skill: `re-a-ndroid` — Auditoria Integral de Aplicações Android com REA, CoT, ReAct & Self-Refine (`v2.2.0`)

## 1. Visão Geral, Propósito Operacional e Gatilhos (Quando Usar)

A skill **`re-a-ndroid`** estabelece o protocolo determinístico de engenharia reversa, auditoria de segurança binária/rede, inspeção de acessibilidade e análise dinâmica de performance para aplicações Android. Integra o servidor **REA (`Reverse Engineer Anything`)**, **Android CLI (`ADB`)**, raciocínio **Chain-of-Thought (CoT)**, malha **ReAct**, verificação **Self-Refine** (*Read-After-Write*) e a sub-skill de auditoria de WebSockets/JSON-RPC ([`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md)).

* **Quando Usar (Gatilhos Positivos):**
  * Dissecação estática de APKs, bytecode DEX, bibliotecas nativas (`lib/*.so`), esquemas de assinatura (`v1` a `v3.1`) e componentes exportados no `AndroidManifest.xml`.
  * Inspeção dinâmica em tempo real via ADB (`am start -W`, `uiautomator dump`, `dumpsys meminfo`, `dumpsys gfxinfo`, `logcat *:E`).
  * Interceptação de endpoints (`REST`, `gRPC`, `ws://`, `wss://`, `JSON-RPC 2.0`, integrações Gemini API / Live API), verificação de SSL Pinning e caça a **funções placebo** (`isRooted() -> false`, `verifyToken() -> true`).
  * Auditoria de CVEs em dependências Gradle/Maven, rotas órfãs em `NavGraph`/Compose, alvos de toque ($48 \times 48\text{dp}$), `contentDescription` e *Haptic Feedback*.

---

## 2. Entradas, Pré-requisitos, Parâmetros e Arquitetura Cognitiva

* `apk_or_project_path` (obrigatório): Caminho do binário `.apk`/`.aab` ou diretório raiz do projeto Android.
* `package_name` / `launcher_activity` (opcional): Identificadores para instrumentação via `adb shell`.
* `rea_detail` (opcional): `"summary"` (padrão para economia de contexto em `inspect_analysis_view`) ou `"full"`.

**Ciclo Cognitivo:** `0. Pre-Flight Condicional (somente se o APK consumir Gemini API ou WS/JSON-RPC)` $\to$ `1. CoT (Sub-hipóteses de segurança/rotas)` $\to$ `2. ReAct (REA estático + ADB dinâmico + OSV.dev)` $\to$ `3. Self-Refine (Read-After-Write + 6 métricas)`.

---

## 3. Fluxo de Execução em 5 Etapas e Matriz de Auditoria em 8 Módulos

### Matriz dos 8 Módulos Especializados

| Módulo | Escopo Técnico Principal | Ferramentas / Fontes de Evidência |
| :--- | :--- | :--- |
| **M1. Arquitetura & Manifesto** | Domínio, MVVM/MVI/Clean, grafo do app e *Activities/Services/Receivers/Providers* exportados. | `decode_android_resources`, `project_android_application_graph`, `AndroidManifest.xml` |
| **M2. Binários, DEX & Assinatura** | Bytecode DEX, `lib/*.so`, frameworks (`Flutter`/`Dart AOT`, `Unity IL2CPP`, `RN`, `Compose`) e assinatura v1–v3.1 (*Janus*, *key rotation lineage* e `posture`). | `inspect_android_package`, `inspect_apk_signature`, `inspect_analysis_view(kind="apk-signature")`, `identify_flutter_build`, `inspect_dart_aot`, `inspect_il2cpp_metadata` |
| **M3. Dinâmica & UI em Tempo Real** | CPU/Heap (`dumpsys meminfo`), hierarquia (`uiautomator dump`) e erros (`logcat *:E`). | `inspect_adb_device`, `read_adb_logcat` |
| **M4. Pacotes & Reparo de CVEs** | Confronto de libs Gradle/Maven com OSV.dev, NVD e GitHub Advisories sem regressão. | `libs.versions.toml`, `build.gradle.kts`, ReAct |
| **M5. APIs, WSS, JSON-RPC & Código Placebo** | Tráfego `http://`/`wss://`, SSL Pinning, JSON-RPC 2.0, Gemini API (`llms.txt`/`llms-full.txt`) e métodos simulados (`return true`/`false` fixo). | `search_android_classes`, `inspect_android_method`, [`audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md) |
| **M6. Rotas, Latência & Órfãs** | Boot *Cold/Warm Start* (`am start -W`), complexidade ciclomática e destinos mortos. | `trace_android_references`, `NavGraph` / Compose |
| **M7. A11y, Toque & Haptics** | `contentDescription`, área mínima $\ge 48 \times 48\text{dp}$ e `HapticFeedbackConstants`. | `window_dump.xml`, `rea_android_auditor.py` |
| **M8. Testes E2E & Jank Rate** | Fluxos automatizados via ADB PTY e taxa de *dropped frames* (`dumpsys gfxinfo`). | `capture_adb_screen`, `dumpsys gfxinfo framestats` |

### Workflow Determinístico em 5 Etapas

1. **Etapa 1 — Ingestão, Grafo e Descompilação Estática (REA v6.8+):** Execute `inspect_android_package` (`detail="summary"`), `inspect_apk_signature` + `inspect_analysis_view(kind="apk-signature", detail="summary")` (validando esquemas v1–v3.1, linhagem de rotação de chaves e `posture`, nunca `inspect_signature` que é restrito a Mach-O), `decode_android_resources` e `project_android_application_graph`. Quando houver libs nativas de engines, acione `identify_flutter_build` / `inspect_dart_aot` ou `inspect_il2cpp_metadata`. Se JADX atingir timeout (`details.limit` com `scope: "rea-runtime"`), ajuste `jadx.operation_timeout_ms` via `update_analysis_settings` e isole retornos com `_meta.provenance.untrusted_content == true`.
2. **Etapa 2 — Inspeção Dinâmica e Visual (ADB):** Meça o boot com `adb shell am start -W -n "[PKG]/[ACTIVITY]"`, extraia a árvore de UI via `adb shell uiautomator dump /sdcard/window_dump.xml` e colete `adb shell dumpsys gfxinfo "[PKG]" framestats`.
3. **Etapa 3 — Interceptação de Rede (`HTTPS`/`WSS`/`JSON-RPC`) e Caça a Funções Placebo:**
   * **Somente quando o APK integrar Gemini API / Live API**, consulte `gemini_search_docs` antes de auditar os contratos.
   * **Somente quando o APK usar `ws://`/`wss://` ou `JSON-RPC 2.0`**, aplique [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md) (`TLS 1.3`, `Network Security Config` / CA confiável, Ephemeral Tokens fora da URL, *Exponential Backoff + Jitter* e $RTT_{\text{avg}} < 150\text{ ms}$).
   * Inspecione métodos de segurança (`isRooted`, `verifyToken`, `checkServerTrusted`) com retorno booleano estático via `inspect_android_method`.
4. **Etapa 4 — Auditoria ReAct de Dependências e CVEs:** Cruze versões de SDKs de terceiros com OSV.dev/NVD e formule o patch exato para `gradle/libs.versions.toml` ou `build.gradle.kts`.
5. **Etapa 5 — Síntese e Validação Matemática (`scripts/rea_android_auditor.py`):** Calcule as 6 métricas formais, vincule cada achado a um `Evidence-ID` e emita o Laudo Self-Refine completo detalhado em [`references/matriz_8_modulos_e_laudo.md`](references/matriz_8_modulos_e_laudo.md).

---

## 4. Métricas Determinísticas, Saídas e Entregáveis (Laudo Self-Refine)

O agente (ou o script [`scripts/rea_android_auditor.py`](scripts/rea_android_auditor.py)) calcula obrigatoriamente 6 indicadores matemáticos:

* **1. Confiabilidade Funcional E2E ($\text{Pass}@k$):** $\text{Pass}@k = 1 - \prod_{i=1}^k \left(1 - \frac{c}{n - k + i}\right)$
* **2. Latência Média de Cold Start ($L_{\text{cold}}$):** $L_{\text{cold}} = \frac{1}{M} \sum_{j=1}^M \text{TotalTime}_j$
* **3. Densidade Ciclomática de Rotas ($M_{\text{rotas}}$):** $M_{\text{rotas}} = E - N + 2P$
* **4. Taxa de Conformidade de Acessibilidade ($A_{\text{rate}}$):** $A_{\text{rate}} = \left(\frac{N_{\text{valid\_labels}} + N_{\text{valid\_touch}}}{2 \cdot N_{\text{total\_interactive\_nodes}}}\right) \times 100\%$
* **5. Razão de Alvos de Toque Válidos ($T_{\text{ratio}}$):** $T_{\text{ratio}} = \frac{\text{Nodes Clicáveis com Largura e Altura } \ge 48\text{dp}}{\text{Total de Nodes Clicáveis}}$
* **6. Taxa de Falsos Negativos em Segurança ($\text{FNR}$):** $\text{FNR} = \frac{\text{FN}}{\text{FN} + \text{TP}}$ (meta estrita: $\text{FNR} < 0.001$).

O entregável final segue o template padronizado em [`references/matriz_8_modulos_e_laudo.md`](references/matriz_8_modulos_e_laudo.md), contendo: (1) Metadados do APK e Assinatura, (2) Tabela Consolidada de Achados (`SEC-*`, `PLC-*`, `ACC-*`, `PERF-*`, `NAV-*`) com `Evidence-ID`, (3) As 6 Métricas Calculadas e (4) Instruções Determinísticas de Reparo para o *Deep Coder*.

---

## 5. Instruções para o Deep Coder, Limites e Guardrails (Quando NÃO Usar)

* **Quando NÃO Usar (Fronteira Negativa):**
  * **Não use para criar projetos/MVPs Android do zero ou configurar AGP 9/KSP2 inicial sem APK/código alvo:** Para scaffolding greenfield em Kotlin 2.4+ / Compose BOM `2026.09.00`, utilize `android-agy-projects`.
  * **Não use para auditoria de frontend Web puro (React/Next.js/CSS):** Utilize `plan-uiux`, `complex-zero` ou `frontend-testing-auditor`.
* **Guardrails de Execução e Compliance ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):**
  * **Pre-Flight Condicional:** Consulte `gemini_search_docs` ou [`../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../agent-server-auditor/references/audit-websocket-jsonrpc.md) quando o app contiver chamadas Gemini API ou transporte WebSocket/JSON-RPC.
  * **Zero Confiança Textual:** Nunca marque um achado como corrigido sem reexecutar o comando REA/ADB ou o script validador (*Read-After-Write*).
  * **Preservação de Assinatura e SDK:** Reparos em `build.gradle.kts` ou classes Java/Kotlin devem preservar a compatibilidade com `minSdk`/`targetSdk` e a integridade de assinatura v2/v3.
  * **Air-Gap Sandbox Enforcement:** Em ambientes isolados, utilize capturas locais (`apk-summary.json`, `window_dump.xml`) sem baixar binários externos não auditados.
