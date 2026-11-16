# Full Technical Reference: 8 Modules, CLI/MCP Playbook & Report Template (`re-a-ndroid` v2.2.0)

## 1. Detailed Breakdown of the 8 Specialist Audit Modules

### Module 1: General Purpose & App Architecture

- **Contextual Analysis:** Map application business domain, target audience, requested permissions, and structural architecture (MVVM, MVI, Clean Architecture).
- **Component Inventory:** Catalog all *Activities*, *Services*, *BroadcastReceivers*, and *ContentProviders* declared and exported (`android:exported="true"`) in `AndroidManifest.xml`.

### Module 2: Static Binary, SDK & Signature Inspection (via REA)

- **Decompilation & DEX Parsing:** Read decompiled bytecode via REA/JADX (`inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`), extract native libraries (`lib/*.so`), and identify cross-platform engines (Flutter, React Native, Unity, Kotlin Multiplatform).
- **Third-Party SDKs & Analytics:** Inventory ad, telemetry, and authentication libraries.
- **Signature Audit:** Validate APK signing schemes (v1, v2, v3, v3.1) for tamper resistance and Janus (CVE-2017-13156) immunity.

### Module 3: Real-Time Dynamic & Visual Inspection (via Android CLI / ADB)

- **Process Monitoring:** Gather CPU, heap/native memory, and thread stats via `adb shell top` and `adb shell dumpsys meminfo <PACKAGE_NAME>`.
- **Visual & Layout Dump Inspection:** Extract accessibility hierarchy via `adb shell uiautomator dump` and audit view nesting depth.
- **Logcat & Error Tracing:** Stream filtered error logs (`adb logcat *:E` / MCP `read_adb_logcat`) for uncaught exceptions (*NullPointerException*, *ANR*, *StrictMode*).

### Module 4: Package Vulnerability Analysis & Deterministic Patching

- **Dependency Verification:** Cross-check identified Gradle/Maven artifacts against OSV.dev, NVD, and GitHub Security Advisories.
- **Zero-Regression Upgrade Plan:** Propose patch upgrades in `gradle/libs.versions.toml` or `build.gradle.kts`, prioritizing critical security fixes without breaking compatibility.

### Module 5: API Calls, WebSockets & Placebo Function Detection

- **Traffic Inspection:** Inspect HTTP/REST endpoints, persistent WebSockets (`ws://`, `wss://`), and gRPC/RPC channels.
- **Network Security Validation:** Verify SSL Pinning (`network_security_config.xml`, OkHttp `CertificatePinner`, or custom `TrustManager`) and detect cleartext traffic (`http://`, `cleartextTrafficPermitted="true"`).
- **Placebo / Fake Security Code Detection:** Locate mocked/constant security checks (e.g., `boolean isRooted() { return false; }`, `boolean verifyToken() { return true; }`, or empty `checkServerTrusted`) that bypass security controls.

### Module 6: Route Quality, Latency & Orphan Route Detection

- **Startup Latency Measurement:** Capture Cold Start and Warm Start timings using `adb shell am start -W -n "<PACKAGE>/<ACTIVITY>"`.
- **Orphan & Dead Routes:** Detect destinations declared in navigation graphs (`NavGraph` XML or typed Jetpack Navigation 3 / Compose routes) lacking valid UI trigger references (`trace_android_references`).
- **Navigation Bottlenecks:** Flag transitions causing memory retention or Main Thread blocking.

### Module 7: Accessibility, Interactivity & Haptic Feedback

- **Readable Labels (`contentDescription`):** Check interactive graphical nodes (`ImageButton`, `Icon`, nodes with `clickable="true"` and `text=""`) for non-empty descriptions.
- **Touch Target Dimensions:** Enforce minimum touch target bounds of $48 \times 48\text{dp}$.
- **Haptic Feedback:** Verify integration with system vibration/haptic APIs (`HapticFeedbackConstants`, `LocalHapticFeedback` in Compose, or `Vibrator`/`VibrationEffect`) on critical confirmations/errors.

### Module 8: E2E Flows & Layout Rendering Performance

- **E2E Flow Automation:** Automate user interactions (taps, swipes, form inputs) via ADB scripts and assert post-action state.
- **Visual Fluidity (*Jank Rate*):** Measure dropped/janky frames during animations and scrolling via `adb shell dumpsys gfxinfo <PACKAGE_NAME> framestats`.

---

## 2. REA CLI/MCP & ADB Command Playbook

### Stage 1: Ingestion & Static Decompilation (REA)

```bash
# Structural APK summary and evidence bundle generation
rea inspect-android-package "[APK_PATH]" --detail summary --evidence_output ./apk-summary.json --json

# Digital signature validation (v1, v2, v3, v3.1)
rea inspect-apk-signature "[APK_PATH]" --json
```

### Stage 2: Real-Time Dynamic & Visual Inspection (ADB)

```bash
# Measure Cold/Warm Start (WaitTime / TotalTime in ms)
adb shell am start -W -n "[PACKAGE_NAME]/[LAUNCHER_ACTIVITY]"

# Dump accessibility tree and bounds of active UI
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml ./window_dump.xml

# Collect rendering and frame jank stats
adb shell dumpsys gfxinfo "[PACKAGE_NAME]" framestats
```

### Stage 3: Local Deterministic Validator Execution (`scripts/rea_android_auditor.py`)

```bash
python skills/re-a-ndroid/scripts/rea_android_auditor.py --self-test
python skills/re-a-ndroid/scripts/rea_android_auditor.py --window-dump ./window_dump.xml --dpi 420 --json
```

---

## 3. Final Audit Report Matrix (Self-Refine Template)

```markdown
# ANDROID APP AUDIT REPORT: RE-A-NDROID

## AUDIT METADATA
- **Application:** `[PACKAGE_NAME]`
- **Version:** `[VERSION_NAME] ([VERSION_CODE])`
- **APK SHA-256 Hash:** `[HASH_SHA256]`
- **Signature Scheme:** `[v1/v2/v3/v3.1 Status]`
- **Test Device:** `[Model / Android Version / API Level]`

---

## 1. CONSOLIDATED FINDINGS & REMEDIATIONS TABLE

| ID | Category | Component / Route | Detected Issue | Risk Level | Traceable Evidence | Deterministic Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Binary / SDK | `libnative.so` | Dependency `vulnerable-sdk:1.2` (CVE-2025-XXXX) | Critical | `apk-summary.json#m1` | Upgrade dependency to `1.4.0`. |
| **PLC-01** | Placebo Code | `RootChecker.java` | `isDeviceRooted()` returns static `false` | Critical | `classes.dex:L104` | Replace with Play Integrity API + native root checks. |
| **ACC-01** | Accessibility | `btn_submit` | Missing `contentDescription` on icon button | Medium | `window_dump.xml:L42` | Add `android:contentDescription="@string/btn_submit_desc"`. |
| **PERF-01**| Performance | `/CheckoutActivity` | 3800ms Cold Boot ($TotalTime$) | Medium | `am_start.log:L12` | Defer SDK init asynchronously via `AppStartup` / `Dispatchers.IO`. |
| **NAV-01** | Routes | `/legacy_payment` | Orphan route with hardcoded test params | Low | `NavGraph.xml:L88` | Remove unused route from navigation graph. |

---

## 2. COMPUTED MATHEMATICAL METRICS
- **E2E Functional Reliability ($\text{Pass}@k$):** `98.5%` ($n=10, k=1$)
- **Average Cold Start Latency ($L_{\text{cold}}$):** `2100 ms`
- **Accessibility Compliance Rate ($A_{\text{rate}}$):** `84.2%`
- **Valid Touch Target Ratio ($T_{\text{ratio}}$):** `91.0%` ($\ge 48\text{dp}$)
- **Route Cyclomatic Density ($M_{\text{rotas}}$):** `14`
- **Security False-Negative Rate ($\text{FNR}$):** `0.0000` ($< 0.001$)

---

## 3. DETERMINISTIC REPAIR INSTRUCTIONS FOR DEEP CODER

### Repair 1: Eliminate Placebo Function in `RootChecker.java`
- **Target File:** `app/src/main/java/com/example/app/security/RootChecker.java`
- **Action:** Replace stub implementation with real integrity verification (Play Integrity API plus `su` binary and `ro.build.tags` checks).

### Repair 2: Fix Accessibility in `activity_main.xml`
- **Target File:** `app/src/main/res/layout/activity_main.xml`
- **Action:** Enforce minimum $48 \times 48\text{dp}$ touch bounds (`minWidth="48dp"`, `minHeight="48dp"`) and add `contentDescription` attributes for TalkBack screen readers.
```
