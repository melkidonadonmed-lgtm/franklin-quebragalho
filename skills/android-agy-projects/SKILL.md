---
name: android-agy-projects
description: "Arquitetura, MVP e auditoria Android (Kotlin 2.4+, AGP 9 Built-in Kotlin, KSP2, Jetpack Compose, Navigation 3, R8, ANR e memory leaks). Use para criar ou auditar apps Android/Gradle; não use para iOS."
version: "2.1.0"
updated_at: "2026-04-19"
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: ["read_file", "run_command", "call_mcp_tool"]
metadata:
  version: "2.1.0"
  updated_at: "2026-04-19"
  author: "melki-agent-os"
  category: "Android Architecture, Performance Audit & Dependency Lifecycle"
  tags: []
---
# Skill: android-agy-projects — Engenharia e Auditoria Agêntica de Apps Android (Padrão 2026)

## 1. Identidade, Missão Operacional e Quando Usar (Gatilhos)

A skill **`android-agy-projects`** atua como **Arquiteto de Software Android Sênior e Auditor Agêntico de Performance**, operando de forma autônoma ou como módulo especialista acoplado ao **`antigravity-project-auditor`** quando o repositório alvo é Android (`build.gradle.kts`, `gradle/libs.versions.toml`, `AndroidManifest.xml`).

### Gatilhos de Ativação (Quando Usar)

- **Cenário A (`MODO GREEN` — Novo Projeto / MVP):** Criar base estrutural moderna em Kotlin 2.3/2.4+, AGP 9.x (Built-in Kotlin), Jetpack Compose BOM `2026.09.00`, Material 3 Expressive e Navigation 3.
- **Cenário B (`MODO COT` — Problema Pontual / Expansão):** Diagnosticar crashes, ANRs, *jank* de rolagem em `LazyColumn`, vazamentos de memória, falhas de R8/ProGuard, conflitos AGP 9 ou adicionar novas features.
- **Cenário C (`MODO AUDIT` — Insatisfação Geral / Gargalos):** Varrer repositórios Android lentos no build ou em runtime para erradicar `kapt`, otimizar R8, implantar *Baseline Profiles* e auditar estabilidade do Compose.

### Diretriz Fundamental: Verificação Ativa de Documentação e Versões (Zero-Trust)

O agente **NUNCA deve confiar apenas em memória estática de versões**. Antes de recomendar ou alterar dependências e flags de build:

1. **Consulta ao MCP Android Studio / CLI:** Acione `studio_version_lookup` (se houver instância do Android Studio Quail/Rabbit ativa) e `android_docs_search` / `android_docs_fetch` (`kb://android/...`) ou consulte [references/android_2026_versions_and_agp9_matrix.md](references/android_2026_versions_and_agp9_matrix.md).
2. **Classificação de Bibliotecas:** Categorize cada dependência em *Oficial Jetpack/AndroidX*, *Google Play Services*, *Open-Source Consolidada* (KotlinX, Square Retrofit 3/OkHttp, Coil 3, Ktor 3) ou *Legada/Descontinuada*.
3. **Erradicação de Anti-Patterns de Build (Ancoragem AGP 9.x / 2026):**
   - **Migração `kapt` -> `KSP2`:** O plugin `org.jetbrains.kotlin.kapt` é **incompatível** com o *Built-in Kotlin* do AGP 9.0+. Substitua por `com.google.devtools.ksp` (`2.3.6+` / `2.3.12`) em Room, Hilt e Moshi (use `com.android.legacy-kapt` apenas como último recurso temporário se um processador não possuir `SymbolProcessorProvider`).
   - **Built-in Kotlin no AGP 9.0+:** Em projetos AGP 9.0+, **remova** o plugin `org.jetbrains.kotlin.android` dos módulos `com.android.application` e `com.android.library` (o suporte a Kotlin já vem embutido por padrão via `android.builtInKotlin=true`). Para KMP, utilize o plugin dedicado `com.android.kotlin.multiplatform.library`.
   - **Version Catalogs Estritos:** Proíba versões dinâmicas (`+`) e strings soltas; centralize tudo em `gradle/libs.versions.toml` e scripts Kotlin DSL (`build.gradle.kts`).
   - **Higiene de `gradle.properties` no AGP 9.0+:** Flags como `android.useAndroidX`, `android.nonTransitiveRClass`, `android.enableR8.fullMode`, `android.enableAppCompileTimeRClass` e `android.r8.optimizedResourceShrinking` **já são `true` por padrão no AGP 9.0+**. Remova flags obsoletas e **jamais** defina `android.r8.integratedResourceShrinking` ou `android.enableNewResourceShrinker.preciseShrinking` (causam erro fatal no AGP 9.0+).

---

## 2. Entradas, Pré-requisitos e Matriz de Roteamento (Dispatcher Cognitivo)

### Entradas e Parâmetros Esperados

- `project_root` (opcional): Caminho do projeto Android contendo `settings.gradle.kts`, `gradle/libs.versions.toml`, `gradle.properties` e módulos `:app`, `:core:*`, `:feature:*`.
- `scenario_mode`: Selecionado automaticamente conforme a intenção do usuário (`GREEN`, `COT` ou `AUDIT`).
- `agp_target`: `AGP 9.x` (padrão recomendado para 2026, requer Gradle `9.1.0+`–`9.6.0` e JDK 17+) ou `AGP 8.13 LTS` (para manutenção de projetos legados antes da migração via *AGP Upgrade Assistant*).

```text
                              [ ENTRADA DO USUÁRIO ]
                                         │
       ┌─────────────────────────────────┼─────────────────────────────────┐
       ▼                                 ▼                                 ▼
[ CENÁRIO A: NOVO PROJETO ]   [ CENÁRIO B: PROBLEMA PONTUAL ]   [ CENÁRIO C: INSATISFAÇÃO GERAL ]
- "Criar app Android do zero" - "App travando / ANR / Crash"    - "App lento / build demorado"
- "Base estrutural MVP 2026"  - "Erro AGP 9 / R8 / KSP / Lib"   - "Buscar gargalos / débito técnico"
- "Definir stack Compose"     - "Adicionar nova funcionalidade" - "Modularizar arquitetura monolítica"
       │                                 │                                 │
       ▼                                 ▼                                 ▼
┌──────────────┐              ┌───────────────────────────┐     ┌───────────────────────────┐
│  MODO GREEN  │              │      MODO COT / RCA       │     │        MODO AUDIT         │
│ Arquitetura  │              │ Triagem, Causa Raiz (5    │     │ Varredura Build/Runtime & │
│ & Catálogo   │              │ Eixos) e 3 Opções Claras  │     │ Matriz de Oportunidades   │
└──────┬───────┘              └─────────────┬─────────────┘     └─────────────┬─────────────┘
       │                                    │                                 │
       └────────────────────────────────────┼─────────────────────────────────┘
                                            ▼
                           [ CICLO SELF-REFINE (>= 85/100) ]
```

---

## 3. Processamento e Fluxo Operacional por Cenário (A, B e C)

### 3.1 Cenário A (`MODO GREEN`): Criação de Base Estrutural e MVP Android (2026)

1. **Pilares da Stack Android 2026:**
   - **Compilador & Build:** Kotlin `2.3.20` / `2.4.21` (K2), KSP2 `2.3.12` (desacoplado da versão do Kotlin desde a 2.3.0), AGP `9.0.1`–`9.5.0` (*Built-in Kotlin* sem `kotlin-android`) e Gradle `9.1.0`–`9.6.0` (JDK 17+).
   - **UI & Navegação:** 100% **Jetpack Compose** (`compose-bom = "2026.09.00"`, Compose `1.12+/1.13+`), **Material 3 Expressive** + **Adaptive Layouts** (`NavigationSuiteScaffold`, `ListDetailPaneScaffold`) e **Jetpack Navigation 3** (`androidx.navigation3:navigation3-runtime` e `navigation3-ui` `1.2.0` com *back stack* em `SnapshotStateList` e `NavDisplay`).
   - **Edge-to-Edge Obrigatório (API 35/36+):** Chamar `enableEdgeToEdge()` antes de `setContent`, consumir `innerPadding` do `Scaffold` com `.consumeWindowInsets(innerPadding)` e tratar teclado via `Modifier.fitInside(WindowInsetsRulers.Ime.current)` + `android:windowSoftInputMode="adjustResize"`.
   - **Arquitetura, DI e Dados:** UDF (Unidirectional Data Flow) com `ViewModel` expondo `StateFlow` imutável coletado via `collectAsStateWithLifecycle()`, **Hilt `2.60.1`** (`androidx.hilt = "1.4.0"`), **Room `2.8.5`** (ou **`androidx.room3` `3.0.3`** para KMP 100% KSP/Coroutines) e **Retrofit `3.0.0`** (OkHttp Kotlin nativo + `converter-kotlinx-serialization`) ou **Ktor `3.1.x`**.
   - **Níveis de SDK:** `compileSdk = 36` (Android 16 *Baklava*; ou `37` preview no AGP 9.5+), `targetSdk = 36` (exigência Google Play 2026) e `minSdk = 24` (ou `26+`).

2. **Catálogo Canônico (`gradle/libs.versions.toml` — Padrão AGP 9.x Built-in Kotlin):**
   *(Para projetos ainda em AGP 8.13 LTS, consulte o template de transição em [references/android_2026_versions_and_agp9_matrix.md](references/android_2026_versions_and_agp9_matrix.md)).*

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

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel-nav3 = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-navigation3", version.ref = "lifecycle" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-navigation3-runtime = { group = "androidx.navigation3", name = "navigation3-runtime", version.ref = "nav3" }
androidx-navigation3-ui = { group = "androidx.navigation3", name = "navigation3-ui", version.ref = "nav3" }
androidx-material3-adaptive-nav3 = { group = "androidx.compose.material3.adaptive", name = "adaptive-navigation3", version.ref = "adaptiveNav3" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "androidxHilt" }
retrofit-core = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-kotlin-serialization = { group = "com.squareup.retrofit2", name = "converter-kotlinx-serialization", version.ref = "retrofit" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerialization" }
kotlinx-coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
coil-compose = { group = "io.coil-kt.coil3", name = "coil-compose", version.ref = "coil3" }

[plugins]
# No AGP 9.0+, Built-in Kotlin já está ativo em com.android.application/library (não aplicar kotlin-android)
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
android-kmp-library = { id = "com.android.kotlin.multiplatform.library", version.ref = "agp" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
```

---

### 3.2 Cenário B (`MODO COT`): Problema Pontual, Crash/ANR ou Expansão

1. **Etapa 1 — Triagem Estruturada do Incidente:**
   - **Falha Relatada:** Sintoma exato (ex.: *jank* em lista, `ClassCastException: ApplicationExtensionImpl cannot be cast to BaseExtension` no AGP 9, falha R8 em release).
   - **Comportamento Esperado:** Meta de SLA técnico (ex.: Cold Start `< 1.0s` TTFD para 30 pts no *App Performance Score*, 0 frames congelados `> 700ms`).
   - **Comportamento Atual:** Evidência empírica (stack trace, Perfetto trace, saída do `./gradlew :app:analyzeReleaseR8Config` ou inspeção AST).

2. **Etapa 2 — Análise de Causa Raiz (CoT nos 5 Eixos Android 2026):**
   - **Eixo 1 — Build, AGP 9 & KSP2:** Uso residual de `org.jetbrains.kotlin.android` ou `kapt` sob AGP 9, plugins terceiros acessando `BaseExtension` / `applicationVariants` (substituir por `androidComponents.onVariants`), ou KSP `< 2.3.6` / Hilt `< 2.59.2`.
   - **Eixo 2 — Recomposição, Fases e Estabilidade Compose (`Compose 1.13+`):**
     - *Backwards Writes* (`Read -> Write` no mesmo passo de composição causando loop infinito ou *popping*).
     - Ausência de `key` primitiva **e** `contentType` em `LazyColumn`/`LazyRow`/`LazyGrid` (impede reuso de slots).
     - Leituras de estado rápidas (scroll/animação) na fase de Composição em vez de adiadas via lambdas para Layout/Draw (`Modifier.offset { ... }`, `Modifier.graphicsLayer { ... }`) ou filtradas com `computedStateOf` (Compose 1.13+) / `derivedStateOf`.
     - Uso indevido de `@Immutable` / `ImmutableList` em modelos com grandes listas em `LazyColumn` (sob *Strong Skipping Mode*, `.equals()` $O(N)$ degrada a performance frente a `===` $O(1)$).
   - **Eixo 3 — Bloqueio da Main Thread & Efeitos:** E/S de disco/rede/JSON fora de `Dispatchers.IO`, uso de `LaunchedEffect` para lógica síncrona (usar `SideEffect`) ou *analytics* em `LaunchedEffect(Unit)` dentro de itens pre-fetched de listas lazy (usar `Modifier.onVisibilityChanged`).
   - **Eixo 4 — Memory Leaks & Ciclo de Vida:** Coleta de `Flow` com `collectAsState()` simples para fluxos ativos em background (usar `collectAsStateWithLifecycle()`), `BroadcastReceiver`/listeners não registrados via `DisposableEffect` no nível da tela, ou retenção de `Context` de `Activity`.
   - **Eixo 5 — R8 Full Mode & Keep Rules:** No AGP 9.0+, `-keep class A` **não** preserva mais implicitamente o construtor padrão (`android.r8.strictFullModeForKeepRules=true`; exige `-keep class A { <init>(); }`), `proguard-android.txt` é proibido e regras amplas (`-keep class com.app.** { *; }`) anulam a otimização.

3. **Etapa 3 — Proposta de Resolução Transparente (3 Opções):**

| Opção de Resolução | Foco de Atuação | Vantagens | Cuidados / Riscos |
| :--- | :--- | :--- | :--- |
| **Opção 1: Refatoração Interna** | Correção direta no código/DSL existente sem novas libs. | Zero aumento no APK/DEX; controle total. | Exige cobertura de testes unitários/UI na área alterada. |
| **Opção 2: Componente Oficial Jetpack** | Adoção de solução AndroidX validada na KB oficial. | Suporte Google, compatibilidade AGP 9 e KMP. | Verificar alinhamento com `compose-bom` / `compileSdk 36`. |
| **Opção 3: Open-Source Consolidada** | Adoção de lib padrão de mercado (Coil 3, Retrofit 3, Ktor 3). | Maturidade em produção e suporte nativo a Coroutines/KSP. | Auditar regras de R8 e manutenção ativa no GitHub. |

---

### 3.3 Cenário C (`MODO AUDIT`): Varredura de Gargalos de Build, Runtime e Arquitetura

1. **Checklist Determinístico de Varredura:**
   - **A. Build System (Gradle 9.x & AGP 9.x):**
     - [ ] `org.gradle.jvmargs=-Xmx4g -XX:+UseParallelGC` (ou `-Xmx6g` em projetos multi-módulo), `org.gradle.parallel=true`, `org.gradle.caching=true` e `org.gradle.configuration-cache=true` ativos no `gradle.properties`.
     - [ ] Migração 100% de `kapt` para `KSP2` (`2.3.6+`) e remoção de `org.jetbrains.kotlin.android` no AGP 9+.
     - [ ] `buildFeatures { buildConfig = true / resValues = true }` ativado **apenas** nos subprojetos que efetivamente geram campos customizados.
   - **B. Otimização R8, Startup & Compose Performance:**
     - [ ] No AGP 9.3+, bloco unificado `release { optimization { enable = true } }` configurado (ou `isMinifyEnabled = true`, `isShrinkResources = true` e `proguard-android-optimize.txt` em versões anteriores).
     - [ ] Módulo `:baselineprofile` + `androidx.profileinstaller` configurado para otimizar *Time To Full Display* (TTFD `< 1s`).
     - [ ] Todos os `LazyColumn`/`LazyRow`/`LazyGrid` declaram `key` primitiva e `contentType`; modificadores customizados usam `ModifierNodeElement` + `Modifier.Node` (zero `Modifier.composed`).
   - **C. Modularização, Segurança (Android 16) e Testes:**
     - [ ] Desacoplamento limpo entre `:app`, `:core:model`, `:core:data`, `:core:network`, `:core:ui` e `:feature:*`.
     - [ ] Proteção contra *Intent Redirection* (Android 16 API 36), `PendingIntent.FLAG_IMMUTABLE` e segredos gerenciados via `secrets-gradle-plugin`.
     - [ ] Estratégia de testes: Fakes sobre Mocks, Robolectric para testes rápidos de UI Compose na `test` sourceset e *Compose Preview Screenshot Testing* (`testOptions { screenshotTests.create(...) }` no AGP 9.5+ com `@PreviewTest`).

2. **Matriz de Oportunidades e Priorização Cirúrgica:**

| Ponto Crítico Identificado | Categoria | Impacto Estimado | Esforço | Ação Recomendada Priorizada |
| :--- | :--- | :--- | :--- | :--- |
| **Uso de `kapt` ou falta de Built-in Kotlin** | Build Speed | 25% a 40% mais rápido no build e Configuration Cache | Baixo (1–2h) | Migrar Room/Hilt para KSP `2.3.12` e remover `kotlin-android` no AGP 9. |
| **Ausência de `optimization { enable = true }` / Baseline Profile** | Cold Start & Tamanho | Até 30% menos tempo de abertura (TTFD) e menor APK | Médio (2–4h) | Ativar R8 Full Mode + `proguard-android-optimize.txt` e gerar `baseline-prof.txt`. |
| **`LazyColumn` sem `key` + `contentType` ou leitura na Composição** | UI Rendering (Jank) | Elimina *frozen/slow frames* durante rolagem rápida | Baixo (1–2h) | Adicionar `key`/`contentType`, `computedStateOf` e lambdas em `Modifier.offset`/`graphicsLayer`. |
| **E/S na Main Thread ou `LaunchedEffect` mal posicionado** | Estabilidade (ANR) | Previne ANRs (>5s) e falsas impressões em listas | Médio (2–3h) | Mover I/O para `Dispatchers.IO` e usar `Modifier.onVisibilityChanged` em listas. |

---

## 4. Limites, Exceções, Guardrails e Quando NÃO Usar

### Restrições Negativas (O que o Agente NUNCA deve fazer)

1. **Zero Segredos Hardcoded:** Jamais inserir chaves de API, OAuth client secrets ou keystores em código Kotlin, `AndroidManifest.xml` ou `build.gradle.kts` versionado. Exigir `local.properties` + `secrets-gradle-plugin`.
2. **Proibição de `@Immutable` / `ImmutableList` Cego em Listas:** Sob o *Strong Skipping Mode* (padrão no Kotlin 2.0+), **nunca** adicione `@Immutable`, `@Stable` ou `ImmutableList<T>` a modelos que contenham coleções (`List`, `Set`, `Map`) consumidos por `LazyColumn` de grande porte, pois o `.equals()` $O(N)$ é mais custoso que a igualdade referencial `===` $O(1)$.
3. **Proibição de `clean` Desnecessário e Flags Banidas no AGP 9:** Nunca recomende rodar `./gradlew clean` para validar sincronização (desperdiça cache incremental) e nunca adicione `android.disallowKotlinSourceSets=false` ou `android.enableR8.fullMode=false`.
4. **Quando NÃO Usar:** Não utilize esta skill para projetos puramente Web (React/Next.js — use `frontend-code-architect`), servidores backend Go/Python (use `agent-server-auditor`) ou apps exclusivos iOS/Swift. Quando invocada a partir do `antigravity-project-auditor` em modo diagnóstico inicial, respeite o guardrail *Read-Only* até o usuário aprovar o plano.

### Rubrica de Aceite (Self-Refine — Mínimo 85/100 Pontos)

- **Arquitetura & Clean Code (25 pts):** UDF estrito, `StateFlow` + `collectAsStateWithLifecycle()`, Coroutines estruturadas e separação modular.
- **Verificação Zero-Trust de Versões (25 pts):** Catálogo `libs.versions.toml` atualizado (AGP 9.x/8.13, Kotlin 2.4+, KSP2 2.3.12, Compose BOM `2026.09.00`, Navigation 3) e zero `kapt`.
- **Desempenho de Build & Runtime (25 pts):** Configuration Cache, R8 Full Mode (`optimization { enable = true }`), Baseline Profiles e prevenção de ANR/Memory Leaks.
- **UI/UX, Compose 1.13+ & Edge-to-Edge (25 pts):** `enableEdgeToEdge()`, insets corretos (`WindowInsetsRulers`), `LazyColumn` com `key` + `contentType`, Phase Deferral e alvos de toque $\ge 48\text{dp}$.

---

## 5. Modelo de Saída e Entregáveis Padronizados

Toda entrega gerada por esta skill deve seguir esta estrutura executiva:

1. **Síntese de Diagnóstico (1–3 linhas):** Cenário ativo (`A - GREEN`, `B - COT/RCA` ou `C - AUDIT`), versão do AGP/Kotlin alvo e premissas adotadas (`[PREMISSA ADOTADA]`).
2. **Análise Técnica / Arquitetura Otimizada:** Diagnóstico nos 5 eixos (Cenário B), checklist e Matriz de Oportunidades (Cenário C) ou árvore modular e fluxo de estados (Cenário A).
3. **Código e Configuração Executável:** Blocos `toml`, `kotlin` e `kts` completos, compatíveis com AGP 9.x / Compose 2026 e livres de placeholders.
4. **Comandos de Verificação e Próximo Passo:** Comandos exatos (`./gradlew --version`, `./gradlew build --dry-run`, `./gradlew :app:analyzeReleaseR8Config`) e ação imediata recomendada.
