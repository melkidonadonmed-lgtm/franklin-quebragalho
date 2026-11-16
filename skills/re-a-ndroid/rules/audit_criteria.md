# Deterministic Audit and Rejection Criteria (`re-a-ndroid` v2.2.0)

To guarantee reproducible Android audits grounded in physical evidence from **REA (`Reverse Engineer Anything`)** and **Android CLI (`ADB`)**, classify every finding under three formal markers:

- `[PASS]`: Requirement verified with traceable evidence (`Evidence-ID`, XML dump, or logcat) within mathematical thresholds.
- `[FAIL]`: Binary/signature flaw, placebo security check, orphan route, accessibility violation ($< 48\text{dp}$), or latency regression.
- `[UNVERIFIED]`: Physically unverifiable (e.g., no ADB device attached for runtime telemetry; scope limited to static analysis).

---

### Rule 1: Binary Integrity, APK Signatures (`v2/v3+`) & Exported Components (Modules 1 & 2)

- **Criterion**: Does the APK enforce modern signature schemes (`v2` and `v3`/`v3.1`, Janus-immune), disable `android:debuggable="true"` in release builds, and protect *Activities*, *Services*, *BroadcastReceivers*, and *ContentProviders* with `android:exported="false"` (or explicit permissions)?
- **Checks**:
  - `v1`-only signature (JAR signing) or `android:debuggable="true"` in release APK -> `[FAIL: WEAK_SIGNATURE_OR_DEBUGGABLE_ENABLED]`
  - Sensitive component with `android:exported="true"` missing permission guard -> `[FAIL: UNPROTECTED_EXPORTED_COMPONENT]`
  - Valid `v2`/`v3` signatures and hardened `AndroidManifest.xml` attack surface -> `[PASS]`

### Rule 2: Network Security, SSL Pinning & Placebo Eradication (Modules 4 & 5)

- **Criterion**: Do all API/WebSocket channels enforce TLS (`https://`, `wss://`), implement real certificate validation / SSL Pinning, avoid security placebo functions (`isRooted() -> false`, `verifyToken() -> true`, empty `checkServerTrusted`), and eliminate open critical CVEs?
- **Checks**:
  - Security/auth method returning a constant boolean (`return true;` / `return false;`) or empty `TrustManager` -> `[FAIL: SECURITY_PLACEBO_FUNCTION_DETECTED]`
  - Cleartext traffic (`http://`, `ws://`, `cleartextTrafficPermitted="true"`) or unpatched critical CVE -> `[FAIL: INSECURE_NETWORK_OR_OPEN_CVE]`
  - Encrypted transport, clean dependencies, and $\text{FNR} < 0.001$ -> `[PASS]`

### Rule 3: Route Quality, Cold Boot Latency ($L_{\text{cold}}$) & Visual Fluidity (Modules 3, 6 & 8)

- **Criterion**: Does average Cold Start ($L_{\text{cold}}$ via `am start -W`) stay within SLA budget, is the navigation graph (`NavGraph` / Compose Navigation) free of orphan/dead routes ($P = 1$), and does E2E reliability achieve $\text{Pass}@k \ge 0.90$?
- **Checks**:
  - Navigation destinations declared in graph without UI trigger references -> `[FAIL: ORPHAN_ROUTE_DETECTED]`
  - Excessive Cold Start ($L_{\text{cold}} > 3000\text{ms}$) or severe jank in `dumpsys gfxinfo` -> `[FAIL: CRITICAL_BOOT_LATENCY_OR_JANK]`
  - Connected routes, optimized boot, and stable E2E flow -> `[PASS]`

### Rule 4: Accessibility (`contentDescription`), Touch Targets ($\ge 48\text{dp}$) & Haptics (Module 7)

- **Criterion**: Do all interactive nodes (`clickable="true"`) carry screen-reader labels (`text` or `content-desc`), satisfy the minimum touch area of $48 \times 48\text{dp}$ ($T_{\text{ratio}} = 1.0$), and trigger haptic feedback (`HapticFeedbackConstants`) on critical actions?
- **Checks**:
  - Clickable element missing `contentDescription`/`text` or width/height $< 48\text{dp}$ in `window_dump.xml` -> `[FAIL: INVALID_ACCESSIBILITY_OR_TOUCH_TARGET]`
  - Full label compliance, $\ge 48\text{dp}$ bounds, and integrated haptics -> `[PASS]`
