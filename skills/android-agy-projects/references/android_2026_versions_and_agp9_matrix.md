# Official 2026 Android Versions Matrix, AGP 9.x Migration & Compose Recipes (`android-agy-projects` v2.1.0)

Level 3 reference grounded in `kb://android/...`, AGP 9.0–9.5 release notes, and upstream `JetBrains/kotlin`, `google/ksp`, `google/dagger`, `square/retrofit`, and `androidx/androidx`.

## 1. Official Compatibility Matrix (2026)

| Component | Min (AGP 9.0) | Current (Late 2026) | Technical Notes |
| :--- | :---: | :---: | :--- |
| **Android Studio** | Otter 3 (`2025.2.3`) | **Quail (`2026.1`) / Rabbit (`2026.2`)** | Agent Mode, native `AGENTS.md`/`SKILL.md`, AQI Agent, Android CLI. |
| **AGP** | `9.0.0` | **`9.0.1` LTS / `9.3.0` / `9.5.0`** | Built-in Kotlin (`android.builtInKotlin=true`), `newDsl=true`, `optimization { enable = true }` (9.3+). |
| **Gradle Wrapper** | `9.1.0` | **`9.1.0` (9.0) / `9.6.0` (9.5)** | Requires JDK 17+ (supports up to JDK 25). |
| **SDK / API** | `36.0.0` (API 36) | **API 36 (*Baklava*) / API 37** | Play mandates `targetSdk = 36`; AGP 9 inherits `compileSdk` if omitted. |
| **Kotlin (KGP)** | `2.2.10` | **`2.3.20` / `2.4.21`** | K2 compiler, context parameters, Strong Skipping default in Compose. |
| **Google KSP2** | `2.3.1` (`2.3.6` AGP9) | **`2.3.12`** | Version decoupled from Kotlin; mandatory replacement for `kapt`. |
| **Compose BOM** | `2025.12.00` | **`2026.09.00` (`1.12+`/`1.13+`)** | M3 Expressive, `computedStateOf` (1.13+), `SideEffect(keys)`, `onVisibilityChanged`. |
| **Navigation 3** | `1.0.0` | **`1.2.0` (`adaptive = 1.3.0`)** | Compose-first `SnapshotStateList`, `NavDisplay`, adaptive `Scenes`. |
| **Hilt / Room / Retrofit** | `2.59.2` / `2.7.0` / `2.11.0` | **`2.60.1` (`androidx.hilt 1.4.0`) / `2.8.5` (`room3 3.0.3`) / `3.0.0`** | KSP2-ready; Room 3 is KMP/KSP-only; Retrofit 3 uses native Kotlin OkHttp 4.12+/5.x. |

## 2. Critical AGP 9.x Changes & Canonical `libs.versions.toml`
1. **Built-in Kotlin:** Remove `alias(libs.plugins.kotlin.android)` from `com.android.application`/`library` modules (retaining it breaks DSL).
2. **`kapt` Removal:** Migrate Room/Hilt/Moshi/Glide to `ksp(...)` (`2.3.6+`); use `com.android.legacy-kapt` only on modules with legacy processors.
3. **Strict Public DSL:** Replace `applicationVariants`/`libraryVariants` with `androidComponents { onVariants { ... } }`.
4. **R8 Full Mode (`strictFullModeForKeepRules=true`):** AGP 9.3+ uses `release { optimization { enable = true }; proguardFiles("proguard-rules.pro") }` (pre-9.3 keeps `isMinifyEnabled = true; isShrinkResources = true`). Write `-keep class A { <init>(); }` explicitly; `proguard-android.txt` is blocked.

```toml
[versions]
agp = "9.3.0"
kotlin = "2.4.21"
ksp = "2.3.12"
coreKtx = "1.16.0"
lifecycle = "2.9.0"
activityCompose = "1.10.1"
composeBom = "2026.09.00"
nav3 = "1.2.0"
adaptiveNav3 = "1.3.0"
hilt = "2.60.1"
androidxHilt = "1.4.0"
retrofit = "3.0.0"
room = "2.8.5"
kotlinxSerialization = "1.8.1"
coroutines = "1.10.1"
coil3 = "3.1.0"

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
android-kmp-library = { id = "com.android.kotlin.multiplatform.library", version.ref = "agp" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
```
*(For AGP 8.13 LTS prior to Gradle 9.1+, pin `agp = "8.13.0"`, `kotlin = "2.3.20"`, `ksp = "2.3.6"`, and keep `kotlin-android`.)*

## 3. Jetpack Compose Performance & Edge-to-Edge Navigation 3
- **Strong Skipping vs. `@Immutable`:** NEVER annotate large `List`/`Set`/`Map` models with `@Immutable` or `ImmutableList<T>` in `Lazy*` — Strong Skipping uses $O(1)$ `===`, whereas `@Immutable` forces $O(N)$ structural `.equals()`.
- **State Derivation & Phase Deferral:** Use `computedStateOf` (Compose `1.13+`) or `remember { derivedStateOf { ... } }` (`< 1.13`); defer animations to `Modifier.offset { ... }` / `Modifier.graphicsLayer { ... }`; ban backwards state writes; replace `Modifier.composed` with `ModifierNodeElement` + `Modifier.Node`.
- **Lazy Keys:** Always pass primitive `key = { it.id }` and `contentType = { it.viewType }`.

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AppTheme {
                val backStack = rememberNavBackStack(HomeKey)
                Scaffold(contentWindowInsets = WindowInsets.safeDrawing) { innerPadding ->
                    NavDisplay(
                        backStack = backStack,
                        modifier = Modifier.fillMaxSize().padding(innerPadding)
                            .consumeWindowInsets(innerPadding)
                            .fitInside(WindowInsetsRulers.Ime.current),
                        entryProvider = entryProvider {
                            entry<HomeKey> { HomeScreen(onNavigate = { backStack.add(it) }) }
                        }
                    )
                }
            }
        }
    }
}
```

## 4. Official Knowledge Base Shortcuts (`android_docs_fetch`)
- `kb://android/agents/skills/build-system/agp/agp-9-upgrade/skill` | `kb://JetBrains/kotlin-agent-skills/skills/kotlin-tooling-agp9-migration/references/VERSION-MATRIX`
- `kb://android/agents/skills/jetpack-compose/jetpack-compose-performance/skill` | `kb://android/agents/skills/performance/r8-analyzer/skill`
- `kb://android/agents/skills/navigation/navigation-3/skill` | `kb://android/agents/skills/system/edge-to-edge/skill` | `kb://android/agents/skills/testing/testing-setup/skill`
