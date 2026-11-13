# Playbook Detalhado — 5 Eixos Android 2026, Opções COT e Matriz AUDIT (`android-agy-projects`)

Complemento técnico de [`SKILL.md`](../SKILL.md) para diagnóstico aprofundado (Cenários B e C). Veja também [`android_2026_versions_and_agp9_matrix.md`](android_2026_versions_and_agp9_matrix.md).

## 1. Cenário B (`MODO COT`) — Os 5 Eixos de Causa Raiz (Android 2026)

1. **Eixo 1 — Build, AGP 9 & KSP2:** Remover `org.jetbrains.kotlin.android` e `kapt`; plugins terceiros com `BaseExtension` / `applicationVariants` devem migrar para `androidComponents.onVariants`; exigir KSP `2.3.6+` e Hilt `2.59.2+`.
2. **Eixo 2 — Recomposição, Fases & Estabilidade Compose (`1.13+`):** Evitar *Backwards Writes* (`Read -> Write` no mesmo frame); exigir `key` primitiva + `contentType` em `LazyColumn`/`LazyRow`/`LazyGrid`; adiar scroll/animação com lambdas (`Modifier.offset { ... }`, `graphicsLayer { ... }`) + `computedStateOf` / `derivedStateOf`; **proibir** `@Immutable` / `ImmutableList` cego em grandes coleções de listas sob *Strong Skipping Mode* (`.equals()` $O(N)$ vs `===` $O(1)$).
3. **Eixo 3 — Main Thread & Efeitos:** Mover E/S para `Dispatchers.IO`, usar `SideEffect` para lógica síncrona pós-composição e `Modifier.onVisibilityChanged` em vez de `LaunchedEffect(Unit)` dentro de itens lazy pre-fetched.
4. **Eixo 4 — Memory Leaks & Ciclo de Vida:** Substituir `collectAsState()` por `collectAsStateWithLifecycle()` em fluxos contínuos; descadastrar `BroadcastReceiver`/listeners em `DisposableEffect`; nunca reter `Context` de `Activity`.
5. **Eixo 5 — R8 Full Mode & Keep Rules:** No AGP 9.0+ (`android.r8.strictFullModeForKeepRules=true`), `-keep class A` exige `{ <init>(); }` explícito; `proguard-android.txt` é proibido; evitar `-keep class com.app.** { *; }`.

## 2. Opções de Resolução (`MODO COT`)

| Opção | Foco | Vantagens | Cuidados |
| :--- | :--- | :--- | :--- |
| **Opção 1: Refatoração Interna** | Correção direta na DSL/código existente | Zero aumento no APK/DEX | Cobertura de testes na área alterada |
| **Opção 2: Jetpack Oficial** | Solução AndroidX da KB oficial | Suporte Google, AGP 9 e KMP | Alinhar `compose-bom` / `compileSdk 36` |
| **Opção 3: Open-Source Consolidada** | Coil 3, Retrofit 3, Ktor 3 | Maturidade + Coroutines/KSP2 | Auditar regras R8 |

## 3. Matriz de Oportunidades e Checklist (`MODO AUDIT`)

| Ponto Crítico | Categoria | Impacto | Ação Priorizada |
| :--- | :--- | :--- | :--- |
| **`kapt` ou falta de Built-in Kotlin** | Build Speed | 25–40% build mais rápido | Migrar para KSP `2.3.12` e remover `kotlin-android` |
| **Sem `optimization { enable = true }` / Baseline Profile** | Startup / APK | Até -30% TTFD (`< 1s`) | Ativar R8 Full Mode + `androidx.profileinstaller` |
| **`LazyColumn` sem `key`/`contentType` ou I/O na Main** | Jank / ANR | Zero *frozen frames* `>700ms` | Lambdas em `offset`/`graphicsLayer` + `Dispatchers.IO` |

- **Build & Segurança:** `org.gradle.jvmargs=-Xmx4g`, `parallel=true`, `caching=true`, `configuration-cache=true`, `buildFeatures` sob demanda, proteção *Intent Redirection* (API 36), `PendingIntent.FLAG_IMMUTABLE`, `secrets-gradle-plugin`, Fakes > Mocks e `@PreviewTest` (AGP 9.5+).
