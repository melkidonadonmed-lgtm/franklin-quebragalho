---
name: re-a-ndroid
description: "Reverse engineer and audit Android APKs using REA and ADB by decompiling DEX/.so binaries, inspecting v1-v3.1 signatures, detecting placebo security checks, measuring route latency, and verifying 48dp targets. Use to audit compiled APKs. Do NOT use to scaffold Android MVPs (android-agy-projects) or audit web apps (ui-frontend-analyst)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "2.2.0"
  updated_at: "2026-11-16"
  author: "Franklin"
  category: "Android APK Reverse Engineering & Security/Performance Auditing"
  tags: ["re-a-ndroid", "engenharia-reversa", "auditoria", "apk", "apks", "android", "rea", "adb", "dex", "assinaturas", "placebo", "latencia", "rotas", "48dp", "android-reverse-engineering", "apk-signature", "dex-audit", "a11y-48dp"]
---

# `re-a-ndroid` (`v2.2.0`) — Android APK Reverse Engineering & Audit

## 1. Overview & Scope

Audits Android APKs via **REA**, **ADB**, **CoT**, **ReAct**, and **Self-Refine** (coupled with `agent-server-auditor`'s `references/audit-websocket-jsonrpc.md` for WS/JSON-RPC):
- Decompiles `.apk`/`.aab`, DEX, `lib/*.so`, engines (`Flutter`/`Dart AOT`, `Unity IL2CPP`), `v1–v3.1` signatures, and `AndroidManifest.xml`.
- Collects ADB telemetry (`am start -W`, `uiautomator dump`, `dumpsys meminfo/gfxinfo`, `logcat *:E`), detects security placebos, checks CVEs, and validates `48x48dp` targets.
- **When NOT to Use:** Do NOT use to scaffold Kotlin 2.4 / Compose BOM `2026.09.00` MVPs (`android-agy-projects`) or audit React/Next.js UIs (`ui-frontend-analyst`, `complex-zero`, `ui-quality-judge`).

## 2. Inputs & Prerequisites

- **`apk_or_project_path`** (required), **`package_name` / `launcher_activity`**, **`rea_detail`** (`"summary"` default | `"full"`).
- **Loop:** `0. Pre-Flight` $\to$ `1. CoT` $\to$ `2. ReAct (REA + ADB + OSV.dev)` $\to$ `3. Self-Refine`.

## 3. Step-by-Step Procedure

Consult [`references/protocol_5_stages_and_metrics.md`](references/protocol_5_stages_and_metrics.md) and [`references/modules_8_matrix_and_report.md`](references/modules_8_matrix_and_report.md):

1. **Stage 1 — REA Ingestion:** Call `inspect_android_package(detail="summary")`, `inspect_apk_signature` + `inspect_analysis_view(kind="apk-signature", detail="summary")` (never `inspect_signature`), `decode_android_resources`, `project_android_application_graph`, and `identify_flutter_build`/`inspect_dart_aot`/`inspect_il2cpp_metadata`. On JADX timeout, raise `jadx.operation_timeout_ms` via `update_analysis_settings` and isolate `_meta.provenance.untrusted_content == true`.
2. **Stage 2 — ADB UI Telemetry:** Run `adb shell am start -W -n "[PKG]/[ACTIVITY]"`, `uiautomator dump /sdcard/window_dump.xml`, and `dumpsys gfxinfo "[PKG]" framestats`.
3. **Stage 3 — Network & Placebos:** Ground Gemini/Live calls via `google-developer-knowledge`/`gemini_get_doc`; audit WS/JSON-RPC (`TLS 1.3`, Ephemeral Tokens, $RTT_{\text{avg}} < 150\text{ms}$); inspect `isRooted`/`verifyToken`/`checkServerTrusted` via `inspect_android_method`.
4. **Stage 4 — CVEs (ReAct):** Check `libs.versions.toml`/`build.gradle.kts` against OSV.dev/NVD.
5. **Stage 5 — Synthesis ([`scripts/rea_android_auditor.py`](scripts/rea_android_auditor.py)):** Compute $\text{Pass}@k$, $L_{\text{cold}}$, $M_{\text{rotas}}$, $A_{\text{rate}}$, $T_{\text{ratio}}$, $\text{FNR} < 0.001$ with `Evidence-ID`.

## 4. Gotchas & Edge Cases

- Enforce Read-After-Write, preserve `minSdk`/`targetSdk`/signing keystores, and obey Air-Gap Sandbox rules.
- Mark dynamic checks `[UNVERIFIED]` if no ADB device is attached while completing static REA analysis.

## 5. Output Schema & Validation Criteria

Emit a Self-Refine Report per [`references/modules_8_matrix_and_report.md`](references/modules_8_matrix_and_report.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md): metadata & signature, findings (`SEC-*`, `PLC-*`, `ACC-*`, `PERF-*`, `NAV-*`) with `Evidence-ID` and `[PASS]`/`[FAIL]`/`[UNVERIFIED]`, 6 math metrics, and Deep Coder patches.

## 6. User Communication Rule

All direct responses, APK audit reports, clarifying questions, and summaries to the end user MUST be in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
