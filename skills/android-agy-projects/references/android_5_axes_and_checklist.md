# Detailed Playbook — 5 Android 2026 Axes, COT Options & AUDIT Matrix (`android-agy-projects`)

Technical Level 3 companion to `SKILL.md` for deep diagnostics (Scenarios B and C). See also [`android_2026_versions_and_agp9_matrix.md`](android_2026_versions_and_agp9_matrix.md).

## 1. Scenario B (`COT Mode`) — The 5 Root-Cause Axes (Android 2026)

1. **Axis 1 — Build, AGP 9 & KSP2:** Remove `org.jetbrains.kotlin.android` and `kapt`; third-party plugins referencing `BaseExtension` / `applicationVariants` must migrate to `androidComponents.onVariants`; require KSP `2.3.6+` and Hilt `2.59.2+`.
2. **Axis 2 — Recomposition, Phases & Compose Stability (`1.13+`):** Prevent Backwards Writes (`Read -> Write` in same frame); enforce primitive `key` + `contentType` in `LazyColumn`/`LazyRow`/`LazyGrid`; defer scroll/animation via lambdas (`Modifier.offset { ... }`, `graphicsLayer { ... }`) + `computedStateOf` / `derivedStateOf`; **ban** blind `@Immutable` / `ImmutableList` on large list models under Strong Skipping Mode (`.equals()` $O(N)$ vs. `===` $O(1)$).
3. **Axis 3 — Main Thread & Side Effects:** Offload I/O to `Dispatchers.IO`, use `SideEffect` for synchronous post-composition sync, and prefer `Modifier.onVisibilityChanged` over `LaunchedEffect(Unit)` inside pre-fetched lazy items.
4. **Axis 4 — Memory Leaks & Lifecycle:** Replace `collectAsState()` with `collectAsStateWithLifecycle()` on continuous streams; unregister `BroadcastReceiver`/listeners in `DisposableEffect`; never retain an `Activity` `Context`.
5. **Axis 5 — R8 Full Mode & Keep Rules:** On AGP 9.0+ (`android.r8.strictFullModeForKeepRules=true`), `-keep class A` requires explicit `{ <init>(); }`; `proguard-android.txt` is banned; avoid broad `-keep class com.app.** { *; }`.

## 2. Resolution Options (`COT Mode`)

| Option | Focus | Advantages | Trade-offs |
| :--- | :--- | :--- | :--- |
| **Option 1: Internal Refactoring** | Direct fix in existing DSL/code | Zero APK/DEX bloat | Requires regression test coverage |
| **Option 2: Official Jetpack** | AndroidX KB canonical path | First-party Google, AGP 9, KMP support | Align `compose-bom` / `compileSdk 36` |
| **Option 3: Mature Open-Source** | Coil 3, Retrofit 3, Ktor 3 | Battle-tested + Coroutines/KSP2 | Audit R8 keep rules |

## 3. Opportunity Matrix & Checklist (`AUDIT Mode`)

| Critical Hotspot | Category | Impact | Prioritized Action |
| :--- | :--- | :--- | :--- |
| **`kapt` or missing Built-in Kotlin** | Build Speed | 25–40% faster builds | Migrate to KSP `2.3.12` and drop `kotlin-android` |
| **Missing `optimization { enable = true }` / Baseline Profile** | Startup / APK | Up to -30% TTFD (`< 1s`) | Enable R8 Full Mode + `androidx.profileinstaller` |
| **`LazyColumn` missing `key`/`contentType` or Main I/O** | Jank / ANR | Zero frozen frames `>700ms` | Lambda `offset`/`graphicsLayer` + `Dispatchers.IO` |

- **Build & Security:** `org.gradle.jvmargs=-Xmx4g`, `parallel=true`, `caching=true`, `configuration-cache=true`, on-demand `buildFeatures`, Intent Redirection hardening (API 36), `PendingIntent.FLAG_IMMUTABLE`, `secrets-gradle-plugin`, Fakes over Mocks, and `@PreviewTest` (AGP 9.5+).
