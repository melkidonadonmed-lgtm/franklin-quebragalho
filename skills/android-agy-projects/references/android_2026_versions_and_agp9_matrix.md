# Official 2026 Android Versions Matrix, AGP 9.x Migration & Jetpack Compose Recipes

Level 3 technical reference for **`android-agy-projects`** (`v2.1.0`), grounded in the official Android Studio Knowledge Base (`kb://android/...`), AGP 9.0–9.5 release notes, and upstream GitHub repositories (`JetBrains/kotlin`, `google/ksp`, `google/dagger`, `square/retrofit`, `androidx/androidx`).

---

## 1. Official Compatibility Matrix (Android Studio, AGP 9.x, Gradle & Kotlin — 2026)

| Component | Minimum (AGP 9.0) | Recommended / Current (Late 2026) | Official Technical Notes |
| :--- | :---: | :---: | :--- |
| **Android Studio** | Otter 3 (`2025.2.3`) | **Quail (`2026.1.x`) / Rabbit (`2026.2.x`)** | Includes Agent Mode with Planning Mode, native Skills support (`AGENTS.md` / `SKILL.md`), AQI Agent, and Android CLI. |
| **Android Gradle Plugin (AGP)** | `9.0.0` | **`9.0.1` (LTS) / `9.3.0` / `9.5.0`** | Introduces Built-in Kotlin (`android.builtInKotlin=true`), strict public DSL (`android.newDsl=true`), and `optimization { enable = true }` (9.3+). |
| **Gradle Wrapper** | `9.1.0` | **`9.1.0` (AGP 9.0) / `9.6.0` (AGP 9.5)** | Requires **JDK 17** minimum (supports up to JDK 25 on Gradle 9.1+). |
| **SDK Build Tools & API** | `36.0.0` (API 36) | **API 36 (Android 16 *Baklava*) / API 37 (Android 17)** | Google Play requires `targetSdk = 36` in 2026. On AGP 9.0+, `targetSdk` inherits `compileSdk` by default if omitted. |
| **Kotlin (KGP)** | `2.2.10` (built-in) | **`2.3.20` / `2.4.21` (Stable)** | K2 compiler, context parameters, explicit backing fields, and Strong Skipping Mode enabled by default in Compose. |
| **Google KSP (KSP2)** | `2.3.1` (`2.3.6` for AGP 9) | **`2.3.12`** | Since KSP `2.3.0`, versioning is decoupled from Kotlin version. Mandatory replacement for `kapt` on AGP 9. |
| **Jetpack Compose BOM** | `2025.12.00` | **`2026.09.00` (Compose `1.12+` / `1.13+`)** | Includes Material 3 Expressive, `computedStateOf` (1.13+), `SideEffect(keys)` (1.12+), and `Modifier.onVisibilityChanged`. |
| **Jetpack Navigation 3** | `1.0.0` | **`1.2.0` (`adaptive-navigation3 = 1.3.0`)** | Compose-first navigation backed by `SnapshotStateList`, `NavDisplay`, and adaptive `Scenes`. |
| **Dagger / Hilt** | `2.59.2` (for AGP 9) | **`2.60.1` (`androidx.hilt = 1.4.0`)** | Full KSP2 support and `rememberHiltViewModelFactory`. |
| **AndroidX Room** | `2.7.0` (KMP/KSP) | **`2.8.5` (`androidx.room`) / `3.0.3` (`androidx.room3`)** | Room 3.0 is 100% KMP, KSP-only (no Java/KAPT), built on Coroutines + `androidx.sqlite`. |
| **Square Retrofit** | `2.11.0` | **`3.0.0` (`3.0.0.4`)** | Built on OkHttp 4.12+/5.x in native Kotlin with 2.x binary compatibility. |

---

## 2. Critical AGP 9.x Architectural Changes (`kb://android/build/releases/agp-9-0-0-release-notes`)

1. **Built-in Kotlin (`android.builtInKotlin=true` by default):**
   - **Mandatory Action:** Remove `alias(libs.plugins.kotlin.android)` / `id("org.jetbrains.kotlin.android")` from `build.gradle.kts` in `com.android.application` and `com.android.library` modules.
   - **Why:** AGP 9.0+ compiles Kotlin natively via KGP `2.2.10+`. Retaining `kotlin-android` triggers a DSL incompatibility failure.
2. **`org.jetbrains.kotlin.kapt` Incompatibility:**
   - `kotlin("kapt")` is incompatible with Built-in Kotlin.
   - **Migration:** Switch all supported processors (Room, Hilt, Moshi, Glide) to `ksp(...)` (`com.google.devtools.ksp` `2.3.6+`). Only for legacy processors lacking `SymbolProcessorProvider`, apply `id("com.android.legacy-kapt")` strictly on that module.
3. **Strict Public DSL (`android.newDsl=true`) & Variant API (`androidComponents`):**
   - Internal classes (`BaseExtension`, `ApplicationExtensionImpl`) are hidden and `applicationVariants` / `libraryVariants` removed.
   - **Replacement:** Use `androidComponents { onVariants { variant -> ... } }` and `beforeVariants`.
4. **Simplified R8 in AGP 9.3+ (`kb://android/agents/skills/performance/r8-analyzer/references/CONFIGURATION`):**

   ```kotlin
   // build.gradle.kts (AGP 9.3+)
   android {
       buildTypes {
           release {
               optimization {
                   enable = true // Enables R8 code shrinking, resource shrinking, and proguard-android-optimize.txt
               }
               proguardFiles("proguard-rules.pro")
           }
       }
   }
   ```

   - For **pre-AGP 9.3** (AGP 8.13 or 9.0–9.2), retain:

   ```kotlin
   buildTypes {
       release {
           isMinifyEnabled = true
           isShrinkResources = true
           proguardFiles(
               getDefaultProguardFile("proguard-android-optimize.txt"),
               "proguard-rules.pro"
           )
       }
   }
   ```

   - **Keep Rules on AGP 9.0+ (`android.r8.strictFullModeForKeepRules=true`):** `-keep class A` no longer preserves the no-arg constructor implicitly; write `-keep class A { <init>(); }` when instantiated via reflection. `getDefaultProguardFile("proguard-android.txt")` is blocked (`android.r8.proguardAndroidTxt.disallowed=true`).
5. **Canonical Version Catalog (`gradle/libs.versions.toml` — AGP 9.3+ Built-in Kotlin vs. AGP 8.13 LTS):**

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
   # On AGP 9.0+, Built-in Kotlin is active in com.android.application/library (do not apply kotlin-android)
   android-application = { id = "com.android.application", version.ref = "agp" }
   android-library = { id = "com.android.library", version.ref = "agp" }
   android-kmp-library = { id = "com.android.kotlin.multiplatform.library", version.ref = "agp" }
   kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
   kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
   ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
   hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
   ```

   If the project remains on **AGP 8.13 LTS** prior to Gradle 9.1+ upgrade, pin `agp = "8.13.0"`, `kotlin = "2.3.20"`, `ksp = "2.3.6"`, and `kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }`.

---

## 3. Official Jetpack Compose Performance Rules (`kb://android/agents/skills/jetpack-compose/jetpack-compose-performance/skill`)

1. **Strong Skipping Mode vs. `@Immutable` / `@Stable` on Collections:**
   - **NEVER** add `@Immutable`, `@Stable`, or `ImmutableList<T>` to models holding large collections (`List`, `Set`, `Map`) passed to `LazyColumn`/`LazyRow`/`LazyGrid`.
   - **Why:** With Strong Skipping Mode enabled by default on Kotlin 2.0+, Compose already skips recomposition for `kotlin.collections.List` via instance equality (`===`, $O(1)$). Adding `@Immutable` or `ImmutableList` forces structural `.equals()` ($O(N)$) on every item per recomposition, degrading scroll smoothness.
2. **`computedStateOf` (Compose 1.13+) vs. `derivedStateOf`:**
   - On Compose `1.13+`, prefer `computedStateOf { scrollState.value > 0 }` for rapidly changing state filters/booleans (lighter invalidation than `derivedStateOf`). On Compose `< 1.13`, use `remember { derivedStateOf { ... } }`.
   - For trivial primitive reads (`list.size`), use direct properties without `derivedStateOf`.
3. **Mandatory Primitive `key` & `contentType` in Lazy Layouts:**

   ```kotlin
   LazyColumn {
       items(
           items = feedItems,
           key = { item -> item.id },             // Primitive: String, Long, or Int
           contentType = { item -> item.viewType } // Required for composition slot reuse
       ) { item ->
           FeedItemRow(item = item)
       }
   }
   ```

4. **Defer State Reads to Layout/Draw (*Phase Deferral*) & Ban Backwards Writes:**
   - Prefer `Modifier.offset { IntOffset(x = animatedOffset.roundToPx(), y = 0) }` and `Modifier.graphicsLayer { alpha = animatedAlpha }` over non-lambda variants.
   - Never mutate a `MutableState` after reading it in the same composition pass (*Backwards Write*).
5. **Replace `Modifier.composed` with `Modifier.Node`:**
   - `Modifier.composed` triggers per-node subcomposition; always implement `ModifierNodeElement<T>` + `Modifier.Node` (`DrawModifierNode`, `LayoutModifierNode`).

---

## 4. Edge-to-Edge, IME & Adaptive Navigation 3 (`kb://android/agents/skills/system/edge-to-edge/skill`)

```kotlin
// MainActivity.kt — Android 16 (API 36) Edge-to-Edge + Navigation 3 Standard
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge() // Mandatory before setContent
        setContent {
            AppTheme {
                val backStack = rememberNavBackStack(HomeKey)
                Scaffold(contentWindowInsets = WindowInsets.safeDrawing) { innerPadding ->
                    NavDisplay(
                        backStack = backStack,
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding)
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

---

## 5. Official Knowledge Base Shortcuts (`android_docs_fetch`)

- **AGP 9 Upgrade:** `kb://android/agents/skills/build-system/agp/agp-9-upgrade/skill`
- **KMP + AGP 9 Matrix:** `kb://JetBrains/kotlin-agent-skills/skills/kotlin-tooling-agp9-migration/references/VERSION-MATRIX`
- **Compose Performance:** `kb://android/agents/skills/jetpack-compose/jetpack-compose-performance/skill`
- **R8 Analyzer:** `kb://android/agents/skills/performance/r8-analyzer/skill`
- **Navigation 3:** `kb://android/agents/skills/navigation/navigation-3/skill`
- **Edge-to-Edge & IME:** `kb://android/agents/skills/system/edge-to-edge/skill`
- **Adaptive Layouts:** `kb://android/agents/skills/jetpack-compose/adaptive/skill`
- **Testing Strategy:** `kb://android/agents/skills/testing/testing-setup/skill`
