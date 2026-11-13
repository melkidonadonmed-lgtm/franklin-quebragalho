# Protocolo de 8 Módulos, 5 Etapas e 6 Métricas — `re-a-ndroid`

Referência operacional estendida consumida por [`../SKILL.md`](../SKILL.md), complementando [`matriz_8_modulos_e_laudo.md`](matriz_8_modulos_e_laudo.md) e [`../../agent-server-auditor/references/audit-websocket-jsonrpc.md`](../../agent-server-auditor/references/audit-websocket-jsonrpc.md).

## Matriz dos 8 Módulos Especializados

| Módulo | Escopo Técnico Principal | Ferramentas / Fontes de Evidência |
| :--- | :--- | :--- |
| **M1. Arquitetura & Manifesto** | Domínio, MVVM/MVI/Clean, grafo e *Activities/Services/Receivers/Providers* exportados. | `decode_android_resources`, `project_android_application_graph`, `AndroidManifest.xml` |
| **M2. Binários, DEX & Assinatura** | Bytecode DEX, `lib/*.so`, engines (`Flutter`/`Dart AOT`, `Unity IL2CPP`, `RN`, `Compose`) e assinatura v1–v3.1 (*Janus*, *key rotation lineage*, `posture`). | `inspect_android_package`, `inspect_apk_signature`, `inspect_analysis_view(kind="apk-signature")`, `identify_flutter_build`, `inspect_dart_aot`, `inspect_il2cpp_metadata` |
| **M3. Dinâmica & UI em Tempo Real** | CPU/Heap (`dumpsys meminfo`), hierarquia (`uiautomator dump`) e erros (`logcat *:E`). | `inspect_adb_device`, `read_adb_logcat` |
| **M4. Pacotes & Reparo de CVEs** | Libs Gradle/Maven vs. OSV.dev, NVD e GitHub Advisories sem regressão. | `libs.versions.toml`, `build.gradle.kts`, ReAct |
| **M5. APIs, WSS, JSON-RPC & Placebo** | Tráfego `http://`/`wss://`, SSL Pinning, JSON-RPC 2.0, Gemini API e métodos simulados (`return true`/`false`). | `search_android_classes`, `inspect_android_method`, `audit-websocket-jsonrpc.md` |
| **M6. Rotas, Latência & Órfãs** | Boot *Cold/Warm Start* (`am start -W`), complexidade ciclomática e destinos mortos. | `trace_android_references`, `NavGraph` / Compose |
| **M7. A11y, Toque & Haptics** | `contentDescription`, área mínima $\ge 48 \times 48\text{dp}$ e `HapticFeedbackConstants`. | `window_dump.xml`, `rea_android_auditor.py` |
| **M8. Testes E2E & Jank Rate** | Fluxos automatizados via ADB PTY e taxa de *dropped frames* (`dumpsys gfxinfo`). | `capture_adb_screen`, `dumpsys gfxinfo framestats` |

## 6 Indicadores Matemáticos Obrigatórios (`scripts/rea_android_auditor.py`)

1. **Confiabilidade Funcional E2E ($\text{Pass}@k$):** $\text{Pass}@k = 1 - \prod_{i=1}^k \left(1 - \frac{c}{n - k + i}\right)$
2. **Latência Média de Cold Start ($L_{\text{cold}}$):** $L_{\text{cold}} = \frac{1}{M} \sum_{j=1}^M \text{TotalTime}_j$
3. **Densidade Ciclomática de Rotas ($M_{\text{rotas}}$):** $M_{\text{rotas}} = E - N + 2P$
4. **Taxa de Conformidade de Acessibilidade ($A_{\text{rate}}$):** $A_{\text{rate}} = \left(\frac{N_{\text{valid\_labels}} + N_{\text{valid\_touch}}}{2 \cdot N_{\text{total\_interactive\_nodes}}}\right) \times 100\%$
5. **Razão de Alvos de Toque Válidos ($T_{\text{ratio}}$):** $T_{\text{ratio}} = \frac{\text{Nodes Clicáveis com Largura e Altura } \ge 48\text{dp}}{\text{Total de Nodes Clicáveis}}$
6. **Taxa de Falsos Negativos em Segurança ($\text{FNR}$):** $\text{FNR} = \frac{\text{FN}}{\text{FN} + \text{TP}}$ (meta estrita: $\text{FNR} < 0.001$)
