# 8 Modules, 5 Stages & 6 Metrics Protocol — `re-a-ndroid`

Extended operational reference consumed by [`SKILL.md`](../SKILL.md), complementing [`modules_8_matrix_and_report.md`](modules_8_matrix_and_report.md) and `agent-server-auditor`'s `references/audit-websocket-jsonrpc.md`.

## 8 Specialist Modules Matrix

| Module | Primary Technical Scope | Tooling / Evidence Sources |
| :--- | :--- | :--- |
| **M1. Architecture & Manifest** | Domain, MVVM/MVI/Clean, component graph, and exported *Activities/Services/Receivers/Providers*. | `decode_android_resources`, `project_android_application_graph`, `AndroidManifest.xml` |
| **M2. Binaries, DEX & Signatures** | DEX bytecode, `lib/*.so`, engines (`Flutter`/`Dart AOT`, `Unity IL2CPP`, `RN`, `Compose`), and `v1–v3.1` signatures (Janus, key rotation lineage, `posture`). | `inspect_android_package`, `inspect_apk_signature`, `inspect_analysis_view(kind="apk-signature")`, `identify_flutter_build`, `inspect_dart_aot`, `inspect_il2cpp_metadata` |
| **M3. Real-Time Dynamics & UI** | CPU/Heap (`dumpsys meminfo`), UI tree (`uiautomator dump`), and runtime crashes (`logcat *:E`). | `inspect_adb_device`, `read_adb_logcat` |
| **M4. Packages & CVE Patching** | Gradle/Maven libraries cross-checked against OSV.dev, NVD, and GitHub Advisories without regression. | `libs.versions.toml`, `build.gradle.kts`, ReAct |
| **M5. APIs, WSS, JSON-RPC & Placebos** | `http://`/`wss://` traffic, SSL Pinning, JSON-RPC 2.0, Gemini API, and stubbed checks (`return true`/`false`). | `search_android_classes`, `inspect_android_method`, `audit-websocket-jsonrpc.md` |
| **M6. Routes, Latency & Orphans** | Cold/Warm Start (`am start -W`), route cyclomatic density, and unreachable screens. | `trace_android_references`, `NavGraph` / Compose |
| **M7. A11y, Touch & Haptics** | `contentDescription`, $\ge 48 \times 48\text{dp}$ minimum bounds, and `HapticFeedbackConstants`. | `window_dump.xml`, `rea_android_auditor.py` |
| **M8. E2E Tests & Jank Rate** | Automated ADB PTY interaction flows and dropped-frame rate (`dumpsys gfxinfo`). | `capture_adb_screen`, `dumpsys gfxinfo framestats` |

## 6 Mandatory Mathematical Indicators (`scripts/rea_android_auditor.py`)

1. **E2E Functional Reliability ($\text{Pass}@k$):** $\text{Pass}@k = 1 - \prod_{i=1}^k \left(1 - \frac{c}{n - k + i}\right)$
2. **Average Cold Start Latency ($L_{\text{cold}}$):** $L_{\text{cold}} = \frac{1}{M} \sum_{j=1}^M \text{TotalTime}_j$
3. **Route Cyclomatic Density ($M_{\text{rotas}}$):** $M_{\text{rotas}} = E - N + 2P$
4. **Accessibility Compliance Rate ($A_{\text{rate}}$):** $A_{\text{rate}} = \left(\frac{N_{\text{valid\_labels}} + N_{\text{valid\_touch}}}{2 \cdot N_{\text{total\_interactive\_nodes}}}\right) \times 100\%$
5. **Valid Touch Target Ratio ($T_{\text{ratio}}$):** $T_{\text{ratio}} = \frac{\text{Clickable Nodes with Width and Height } \ge 48\text{dp}}{\text{Total Clickable Nodes}}$
6. **Security False-Negative Rate ($\text{FNR}$):** $\text{FNR} = \frac{\text{FN}}{\text{FN} + \text{TP}}$ (strict target: $\text{FNR} < 0.001$)
