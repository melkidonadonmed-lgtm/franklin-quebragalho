---
name: android-agy-projects
description: "Arquitetura, MVP e auditoria Android (Kotlin 2.4+, AGP 9 Built-in Kotlin, KSP2, Jetpack Compose, Navigation 3, R8, ANR e memory leaks). Use para criar ou auditar apps Android/Gradle; não use para iOS."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
metadata:
  version: "2.1.0"
  updated_at: "2026-11-13"
  author: "melki-agent-os"
  category: "Android Architecture, Performance Audit & Dependency Lifecycle"
  tags: ["android", "agp-9", "kotlin-k2", "ksp2", "jetpack-compose", "navigation-3", "r8"]
---
# Skill: `android-agy-projects` — Engenharia & Auditoria Android (Padrão 2026)

Atua como Arquiteto Android Sênior e Auditor de Performance para bases Kotlin/Gradle, autônoma ou acoplada a `auditoria-projetos-sistema`. Matrizes de versões e os 5 eixos detalhados constam em [`references/android_2026_versions_and_agp9_matrix.md`](references/android_2026_versions_and_agp9_matrix.md) e [`references/android_5_eixos_e_checklist.md`](references/android_5_eixos_e_checklist.md).

## 1. Gatilhos e Verificação Ativa (Zero-Trust)

- **Cenário A (`MODO GREEN` — Novo Projeto/MVP):** Kotlin `2.3/2.4+`, AGP 9.x (Built-in Kotlin), Compose BOM `2026.09.00`, Material 3 Expressive e Navigation 3.
- **Cenário B (`MODO COT` — Crash/ANR/Expansão):** Triagem e RCA nos 5 Eixos (AGP 9/KSP2, recomposição Compose, Main Thread/ANR, Memory Leaks, R8 Full Mode).
- **Cenário C (`MODO AUDIT` — Gargalos/Build):** Erradicar `kapt`, otimizar R8, *Baseline Profiles* e modularização `:core:*` / `:feature:*`.
- **Invariantes Zero-Trust:** Nunca confie apenas em memória de versões — consulte `studio_version_lookup`, `android_docs_search` ou `references/`; remova `org.jetbrains.kotlin.android` e `kapt` no AGP 9.0+; proíba `+` em `gradle/libs.versions.toml` e flags banidas (`android.r8.integratedResourceShrinking`, `android.enableNewResourceShrinker.preciseShrinking`, `android.disallowKotlinSourceSets=false`, `android.enableR8.fullMode=false`).

## 2. Entradas e Pré-requisitos

- `project_root` (opcional): Raiz contendo `settings.gradle.kts`, `gradle/libs.versions.toml`, `gradle.properties` e módulos `:app`/`:core:*`/`:feature:*`.
- `scenario_mode`: `GREEN`, `COT` ou `AUDIT` (inferido da demanda).
- `agp_target`: `AGP 9.x` (Gradle `9.1.0+`–`9.6.0`, JDK 17+) ou `AGP 8.13 LTS`.

## 3. Processamento e Fluxo por Cenário

1. **Cenário A (`MODO GREEN`):**
   - Kotlin `2.3.20`/`2.4.21`, KSP2 `2.3.12`, AGP `9.0.1`–`9.5.0`, `compileSdk = 36` (`37` preview), `targetSdk = 36`, `minSdk = 24+`.
   - 100% Compose (`compose-bom = "2026.09.00"`), Navigation 3 (`1.2.0` + `NavDisplay`), `enableEdgeToEdge()`, `.consumeWindowInsets(innerPadding)` e `WindowInsetsRulers.Ime`.
   - UDF (`ViewModel` + `StateFlow` / `collectAsStateWithLifecycle()`), Hilt `2.60.1`, Room `2.8.5` (`androidx.room3` `3.0.3` em KMP), Retrofit `3.0.0` / Ktor `3.1.x`, Coil `3.1.0`.
2. **Cenário B (`MODO COT/RCA`):** Defina falha, SLA (`TTFD < 1.0s`, 0 frozen frames `>700ms`) e evidência (stack trace, Perfetto, `./gradlew :app:analyzeReleaseR8Config`); investigue os **5 Eixos** e proponha **3 opções** conforme [`references/android_5_eixos_e_checklist.md`](references/android_5_eixos_e_checklist.md).
3. **Cenário C (`MODO AUDIT`):** Audite Configuration Cache, KSP2, `release { optimization { enable = true } }`, `:baselineprofile`, `LazyColumn` (`key` + `contentType`), `Intent Redirection`, `PendingIntent.FLAG_IMMUTABLE` e `secrets-gradle-plugin`.

## 4. Limites, Exceções e Rubrica (`>= 85/100`)

- **Guardrails ([`rules/criterios_auditoria.md`](rules/criterios_auditoria.md)):** Zero segredos no código/`AndroidManifest.xml`, zero `@Immutable`/`ImmutableList` em grandes listas de `LazyColumn`, proibido `./gradlew clean` para sync; via `auditoria-projetos-sistema`, opere *Read-Only* até aprovação.
- **Não Use Para:** Web React/Next (`frontend-code-architect`), Python/Go (`agent-server-auditor`), iOS ou engenharia reversa de APK (`re-a-ndroid`).
- **Aceite (`>= 85/100`):** UDF (`25`) + Zero-Trust AGP 9/KSP2 (`25`) + Build/R8/ANR (`25`) + Compose/Edge-to-Edge/48dp (`25`).

## 5. Saídas e Entregáveis

Síntese (Cenário, versões e `[PREMISSA ADOTADA]`), diagnóstico nos 5 eixos/matriz, blocos `toml`/`kotlin`/`kts` sem placeholders e verificação (`./gradlew --version`, `./gradlew build --dry-run`, `./gradlew :app:analyzeReleaseR8Config`).
