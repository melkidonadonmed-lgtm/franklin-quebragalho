# Matriz Oficial de Versões Android 2026, Migração AGP 9.x e Receitas Jetpack Compose

Referência técnica de Tier 3 para a skill **`android-agy-projects`** (`v2.1.0`), consolidada a partir da Base de Conhecimento oficial do Android Studio (`kb://android/...`), notas de lançamento do AGP 9.0–9.5 e repositórios oficiais no GitHub (`JetBrains/kotlin`, `google/ksp`, `google/dagger`, `square/retrofit`, `androidx/androidx`).

---

## 1. Matriz Oficial de Compatibilidade (Android Studio, AGP 9.x, Gradle & Kotlin — 2026)

| Componente | Versão Mínima (AGP 9.0) | Versão Recomendada / Atual (Out–Nov/2026) | Notas Técnicas Oficiais |
| :--- | :---: | :---: | :--- |
| **Android Studio** | Otter 3 (`2025.2.3`) | **Quail (`2026.1.x`) / Rabbit (`2026.2.x`)** | Inclui Agent Mode com *Planning Mode*, suporte nativo a Skills (`AGENTS.md` / `SKILL.md`), AQI Agent e Android CLI. |
| **Android Gradle Plugin (AGP)** | `9.0.0` | **`9.0.1` (LTS) / `9.3.0` / `9.5.0`** | Introduz *Built-in Kotlin* (`android.builtInKotlin=true`), novo DSL estrito (`android.newDsl=true`) e bloco `optimization { enable = true }` (9.3+). |
| **Gradle Wrapper** | `9.1.0` | **`9.1.0` (AGP 9.0) / `9.6.0` (AGP 9.5)** | Requer **JDK 17** no mínimo (com suporte a até JDK 25 no Gradle 9.1+). |
| **SDK Build Tools & API** | `36.0.0` (API 36) | **API 36 (Android 16 *Baklava*) / API 37 (Android 17)** | Google Play exige `targetSdk = 36` em 2026. No AGP 9.0+, `targetSdk` herda `compileSdk` por padrão se omitido. |
| **Kotlin (KGP)** | `2.2.10` (embutido) | **`2.3.20` / `2.4.21` (Estável)** | Compilador K2, *context parameters*, *explicit backing fields* e *Strong Skipping Mode* padrão no Compose. |
| **Google KSP (KSP2)** | `2.3.1` (`2.3.6` p/ AGP 9) | **`2.3.12`** | Desde o KSP `2.3.0`, o versionamento é desacoplado da versão do Kotlin. Obrigatório para substituir `kapt` no AGP 9. |
| **Jetpack Compose BOM** | `2025.12.00` | **`2026.09.00` (Compose `1.12+` / `1.13+`)** | Inclui Material 3 Expressive, `computedStateOf` (1.13+), `SideEffect(keys)` (1.12+) e `Modifier.onVisibilityChanged`. |
| **Jetpack Navigation 3** | `1.0.0` | **`1.2.0` (`adaptive-navigation3 = 1.3.0`)** | Navegação Compose-first baseada em `SnapshotStateList`, `NavDisplay` e `Scenes` adaptativas. |
| **Dagger / Hilt** | `2.59.2` (p/ AGP 9) | **`2.60.1` (`androidx.hilt = 1.4.0`)** | Suporte total a KSP2 e `rememberHiltViewModelFactory`. |
| **AndroidX Room** | `2.7.0` (KMP/KSP) | **`2.8.5` (`androidx.room`) / `3.0.3` (`androidx.room3`)** | Room 3.0 é 100% KMP, exclusivo via KSP (sem Java/KAPT) e baseado em Coroutines + `androidx.sqlite`. |
| **Square Retrofit** | `2.11.0` | **`3.0.0` (`3.0.0.4`)** | Baseado em OkHttp 4.12+/5.x em Kotlin nativo com compatibilidade binária com 2.x. |

---

## 2. Mudanças Arquiteturais Críticas do AGP 9.x (`kb://android/build/releases/agp-9-0-0-release-notes`)

1. **Built-in Kotlin (`android.builtInKotlin=true` por padrão):**
   - **Ação Obrigatória:** Remova `alias(libs.plugins.kotlin.android)` / `id("org.jetbrains.kotlin.android")` dos arquivos `build.gradle.kts` de módulos `com.android.application` e `com.android.library`.
   - **Por quê:** O AGP 9.0+ compila fontes Kotlin nativamente e traz dependência de runtime no KGP `2.2.10+`. Manter o plugin `kotlin-android` gera erro de incompatibilidade com o novo DSL.
2. **Incompatibilidade do `org.jetbrains.kotlin.kapt`:**
   - O plugin `kotlin("kapt")` é incompatível com o *Built-in Kotlin*.
   - **Migração:** Mude todos os processadores compatíveis (Room, Hilt, Moshi, Glide) para `ksp(...)` (`com.google.devtools.ksp` `2.3.6+`). Caso exista dependência legada sem `SymbolProcessorProvider`, aplique `id("com.android.legacy-kapt")` apenas naquele módulo.
3. **Novo DSL Público Estrito (`android.newDsl=true`) e Variant API (`androidComponents`):**
   - Classes internas como `BaseExtension` e `ApplicationExtensionImpl` foram ocultadas, e `applicationVariants` / `libraryVariants` foram removidas.
   - **Substituição:** Use `androidComponents { onVariants { variant -> ... } }` e `beforeVariants`.
4. **R8 Simplificado no AGP 9.3+ (`kb://android/agents/skills/performance/r8-analyzer/references/CONFIGURATION`):**

   ```kotlin
   // build.gradle.kts (AGP 9.3+)
   android {
       buildTypes {
           release {
               optimization {
                   enable = true // Ativa code shrinking (R8), resource shrinking e proguard-android-optimize.txt
               }
               proguardFiles("proguard-rules.pro")
           }
       }
   }
   ```

   - Em versões **anteriores ao AGP 9.3** (ex.: AGP 8.13 ou 9.0–9.2), mantenha:

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

   - **Atenção às Keep Rules no AGP 9.0+ (`android.r8.strictFullModeForKeepRules=true`):** `-keep class A` **não** mantém mais o construtor vazio implicitamente; escreva `-keep class A { <init>(); }` quando a instância for criada por reflexão. Além disso, `getDefaultProguardFile("proguard-android.txt")` é **bloqueado** no AGP 9.0+ (`android.r8.proguardAndroidTxt.disallowed=true`).
5. **Template de Transição (`gradle/libs.versions.toml` para Projetos Legados em AGP 8.13 LTS):**
   Caso o projeto ainda não possa subir para o Gradle 9.1+ / AGP 9.x, utilize a última linha 8.x estável:

   ```toml
   [versions]
   agp = "8.13.0"
   kotlin = "2.3.20"
   ksp = "2.3.6"
   # No AGP 8.13, mantenha o plugin kotlin-android:
   [plugins]
   android-application = { id = "com.android.application", version.ref = "agp" }
   kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
   kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
   ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
   ```

---

## 3. Regras Oficiais de Performance no Jetpack Compose (`kb://android/agents/skills/jetpack-compose/jetpack-compose-performance/skill`)

1. **Strong Skipping Mode vs. `@Immutable` / `@Stable` em Coleções:**
   - **NUNCA** adicione `@Immutable`, `@Stable` ou `ImmutableList<T>` a modelos que contenham coleções (`List`, `Set`, `Map`) passados para `LazyColumn`/`LazyRow`/`LazyGrid` com grandes volumes de dados.
   - **Motivo:** Com o *Strong Skipping Mode* ativo por padrão no Kotlin 2.0+, o compilador já pula a recomposição de `kotlin.collections.List` usando igualdade de instância (`===`, custo $O(1)$). Forçar `@Immutable` ou `ImmutableList` obriga o Compose a executar `.equals()` estrutural ($O(N)$) em cada item a cada recomposição, degradando a rolagem.
2. **`computedStateOf` (Compose 1.13+) vs. `derivedStateOf`:**
   - Em Compose `1.13+`, prefira `computedStateOf { scrollState.value > 0 }` para derivações booleanas e filtros de estados que mudam rapidamente (invalidação mais leve que `derivedStateOf`). Em Compose `< 1.13`, use `remember { derivedStateOf { ... } }`.
   - Para expressões primitivas triviais ou leitura de `list.size`, use propriedades/getters diretos sem `derivedStateOf`.
3. **Obrigatoriedade de `key` Primitiva e `contentType` em Layouts Lazy:**

   ```kotlin
   LazyColumn {
       items(
           items = feedItems,
           key = { item -> item.id },             // Primitivo: String, Long ou Int
           contentType = { item -> item.viewType } // Essencial para reuso de slots na composição
       ) { item ->
           FeedItemRow(item = item)
       }
   }
   ```

4. **Adiar Leituras de Estado para Layout/Draw (*Phase Deferral*) e Proibir *Backwards Writes*:**
   - Use `Modifier.offset { IntOffset(x = animatedOffset.roundToPx(), y = 0) }` e `Modifier.graphicsLayer { alpha = animatedAlpha }` em vez das versões não-lambda.
   - Nunca altere um `MutableState` após ele já ter sido lido no mesmo passo de composição (*Backwards Write*).
5. **Substituir `Modifier.composed` por `Modifier.Node`:**
   - `Modifier.composed` causa subcomposição por nó; implemente sempre `ModifierNodeElement<T>` + `Modifier.Node` (`DrawModifierNode`, `LayoutModifierNode`).

---

## 4. Edge-to-Edge, IME e Navegação 3 Adaptativa (`kb://android/agents/skills/system/edge-to-edge/skill`)

```kotlin
// MainActivity.kt — Padrão Android 16 (API 36) Edge-to-Edge + Navigation 3
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge() // Obrigatório antes de setContent
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

## 5. Atalhos da Base de Conhecimento Oficial (`android_docs_fetch`)

- **Upgrade AGP 9:** `kb://android/agents/skills/build-system/agp/agp-9-upgrade/skill`
- **Matriz KMP + AGP 9:** `kb://JetBrains/kotlin-agent-skills/skills/kotlin-tooling-agp9-migration/references/VERSION-MATRIX`
- **Performance Compose:** `kb://android/agents/skills/jetpack-compose/jetpack-compose-performance/skill`
- **Analisador R8:** `kb://android/agents/skills/performance/r8-analyzer/skill`
- **Navigation 3:** `kb://android/agents/skills/navigation/navigation-3/skill`
- **Edge-to-Edge & IME:** `kb://android/agents/skills/system/edge-to-edge/skill`
- **Adaptive Layouts:** `kb://android/agents/skills/jetpack-compose/adaptive/skill`
- **Estratégia de Testes:** `kb://android/agents/skills/testing/testing-setup/skill`
