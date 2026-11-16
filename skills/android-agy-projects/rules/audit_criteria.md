# Deterministic Audit and Rejection Criteria (`android-agy-projects` v2.1.0)

To guarantee objective, falsifiable diagnostics grounded in official Android Studio (2026) documentation, evaluate every deliverable under three strict markers:

- `[PASS]`: Requirement fully satisfied and compatible with AGP 9.x / Kotlin 2.3–2.4+ / Compose BOM `2026.09.00`.
- `[FAIL]`: Direct build-rule violation, recomposition anti-pattern, obsolete dependency (`kapt`), or security flaw.
- `[UNVERIFIED]`: Cannot be verified due to missing access to `libs.versions.toml` or `build.gradle.kts`.

---

### Rule 1: Zero-Trust Versions, Built-in Kotlin (AGP 9.x) & `kapt` Eradication

- **Criterion**: Does the project use Version Catalogs (`gradle/libs.versions.toml`) with pinned active versions, replace `kapt` with `com.google.devtools.ksp` (`2.3.6+` / `2.3.12`), and remove the redundant/conflicting `org.jetbrains.kotlin.android` plugin on AGP 9.0+?
- **Checks**:
  - Use of `kapt` in Room/Hilt/Moshi or dynamic `+` versions (`18.+`) -> `[FAIL: KAPT_OR_DYNAMIC_VERSION_DETECTED]`
  - Manual application of `org.jetbrains.kotlin.android` in a `com.android.application` module on AGP 9.0+ with `android.newDsl=true` -> `[FAIL: CONFLICTING_KOTLIN_ANDROID_PLUGIN_AGP9]`
  - Clean `libs.versions.toml`, KSP2 active, and plugins aligned with AGP version -> `[PASS]`

### Rule 2: Jetpack Compose (`1.12+/1.13+`) Stability, Phase Deferral & Lazy Layouts

- **Criterion**: Do `LazyColumn`/`LazyRow`/`LazyGrid` containers declare primitive `key` and `contentType`, defer fast state reads to Layout/Draw via lambdas (`Modifier.offset { ... }`, `Modifier.graphicsLayer { ... }`), avoid Backwards Writes, and avoid `@Immutable`/`ImmutableList` on large collection models under Strong Skipping Mode?
- **Checks**:
  - `items(...)` in `LazyColumn` missing `key` or `contentType` -> `[FAIL: LAZY_MISSING_KEY_OR_CONTENT_TYPE]`
  - Adding `@Immutable` / `@Stable` / `ImmutableList` on models containing large `List`/`Set`/`Map` for `LazyColumn` -> `[FAIL: EQUALS_PENALTY_ON_STRONG_SKIPPING]`
  - Legacy `Modifier.composed` instead of `ModifierNodeElement` + `Modifier.Node` -> `[FAIL: LEGACY_MODIFIER_COMPOSED]`
  - Optimized recomposition, deferred phases, and reusable slots -> `[PASS]`

### Rule 3: R8 Full Mode Optimization, `gradle.properties` Hygiene & Baseline Profiles

- **Criterion**: Does `release` enable R8 via `optimization { enable = true }` (AGP 9.3+) or `isMinifyEnabled = true` + `isShrinkResources = true` + `proguard-android-optimize.txt` (pre-AGP 9.3), avoiding `proguard-android.txt` and banned AGP 9.0+ flags (`android.r8.integratedResourceShrinking`, `android.enableR8.fullMode=false`)?
- **Checks**:
  - `android.enableR8.fullMode=false` or `proguard-android.txt` -> `[FAIL: R8_DISABLED_OR_UNOPTIMIZED]`
  - Banned AGP 9.0 properties (`android.r8.integratedResourceShrinking` or `android.enableNewResourceShrinker.preciseShrinking`) -> `[FAIL: BANNED_GRADLE_PROPERTY_AGP9]`
  - R8 Full Mode enabled, strict keep rules (`<init>();` where needed), and Configuration Cache active -> `[PASS]`

### Rule 4: Edge-to-Edge (API 35/36+), Navigation 3 & Safe Concurrency

- **Criterion**: Do `ComponentActivity` classes call `enableEdgeToEdge()` before `setContent`, apply insets without double padding (`WindowInsets.safeDrawing` / `WindowInsetsRulers.Ime.current`), collect flows via `collectAsStateWithLifecycle()`, and offload I/O to `Dispatchers.IO`?
- **Checks**:
  - DB/network/JSON I/O on Main Thread or side effects inside `@Composable` body -> `[FAIL: MAIN_THREAD_BLOCK_OR_BODY_SIDE_EFFECT]`
  - Missing `enableEdgeToEdge()` or missing inset/IME handling on `compileSdk >= 35` -> `[FAIL: EDGE_TO_EDGE_API36_VIOLATION]`
  - Edge-to-Edge, Navigation 3 / Type-Safe Navigation, and structured Coroutines verified -> `[PASS]`

### Rule 5: Android 16 (API 36) Security, Secrets & Deliverable Completeness

- **Criterion**: Zero secrets hardcoded in Kotlin/XML/`build.gradle.kts` (`secrets-gradle-plugin` used), `PendingIntent` and `Intent` launches hardened against Android 16 Intent Redirection, and deliverables include all 4 required sections (Synthesis, 5-Axis Analysis/Matrix, Executable Code, Next Step)?
- **Checks**:
  - Hardcoded API key or token in Kotlin, XML, or `build.gradle.kts` -> `[FAIL: HARDCODED_ANDROID_SECRET]`
  - Missing Root Cause options (Scenario B) or Opportunity Matrix (Scenario C) -> `[FAIL: INCOMPLETE_DELIVERABLE]`
  - Verified security and complete deliverable scoring Self-Refine $\ge 85/100$ -> `[PASS]`
