---
name: android-agy-projects
description: "Design, scaffold MVPs, and audit Android projects (Kotlin 2.4+, AGP 9 Built-in Kotlin, KSP2, Jetpack Compose, Navigation 3, R8 Full Mode, ANR, and memory leaks). Use to build or audit Android/Gradle apps. Do NOT use for iOS, web Next.js (ui-clean-worker), or APK reverse engineering (re-a-ndroid)."
compatibility: "Antigravity 2.0, FastMCP, Python 3.12+, Go 1.24+"
allowed-tools: read_file write_file edit_file run_command
metadata:
  version: "2.1.0"
  updated_at: "2026-11-16"
  author: "Franklin"
  category: "Android Architecture, Performance Audit & Dependency Lifecycle"
  tags: "android-agy-projects, android, app, gradle, agp, agp9, agp-9, kotlin, kotlin-k2, ksp2, compose, jetpack, jetpack-compose, navigation, navigation-3, r8, anr, memory, leaks, auditar, criar"
---

# `android-agy-projects` (`v2.1.0`) — Android Engineering & Audit (2026)

Senior Android Architect & Performance Auditor for Kotlin/Gradle repos, standalone or coupled with `system-project-auditor`.

## 1. Overview & Scope

- **Scenario A (`GREEN`):** Kotlin `2.3/2.4+`, AGP 9.x (Built-in Kotlin), Compose BOM `2026.09.00`, Material 3 Expressive, Navigation 3.
- **Scenario B (`COT`):** 5-Axis RCA (AGP 9/KSP2, Compose recomposition, Main Thread/ANR, Memory Leaks, R8 Full Mode).
- **Scenario C (`AUDIT`):** Drop `kapt`, enable R8 Full Mode, Baseline Profiles, and `:core:*`/`:feature:*` modules.
- **When NOT to Use:** Do NOT use for iOS, web React/Next.js (`ui-clean-worker`), Python/Go (`agent-server-auditor`), or APK reverse engineering (`re-a-ndroid`).

## 2. Inputs & Prerequisites

- **`project_root`** (`settings.gradle.kts`, `gradle/libs.versions.toml`, `gradle.properties`), **`scenario_mode`** (`GREEN`/`COT`/`AUDIT`), **`agp_target`** (`AGP 9.x` / Gradle `9.1–9.6`, JDK 17+ or `AGP 8.13 LTS`).

## 3. Step-by-Step Procedure

Consult [`references/android_2026_versions_and_agp9_matrix.md`](references/android_2026_versions_and_agp9_matrix.md) and [`references/android_5_axes_and_checklist.md`](references/android_5_axes_and_checklist.md):

1. **Zero-Trust Checks:** Verify versions via `studio_version_lookup`/`android_docs_search`; remove `org.jetbrains.kotlin.android` and `kapt` on AGP 9.0+; ban `+` versions and deprecated flags (`android.r8.integratedResourceShrinking`, `android.enableR8.fullMode=false`).
2. **Scenario A (`GREEN`):** Pin Kotlin `2.3.20`/`2.4.21`, KSP2 `2.3.12`, AGP `9.0.1`–`9.5.0`, `compileSdk`/`targetSdk = 36`, Compose BOM `"2026.09.00"`, Nav3 `1.2.0`, `enableEdgeToEdge()`, `WindowInsetsRulers.Ime`, UDF (`ViewModel` + `collectAsStateWithLifecycle()`), Hilt `2.60.1`, Room `2.8.5` (`androidx.room3` `3.0.3` KMP), Retrofit `3.0.0`, Coil `3.1.0`.
3. **Scenario B (`CoT + ToT`):** Define SLA (`TTFD < 1.0s`, 0 frozen frames `>700ms`) + evidence; trace root causes across all 5 Axes (`CoT`) and compare 3 `ToT` resolution branches (Internal Refactor vs. Jetpack Official vs. Mature OSS).
4. **Scenario C (`ReAct AUDIT + RAW`):** Audit Configuration Cache, KSP2, `optimization { enable = true }`, `:baselineprofile`, `LazyColumn` (`key` + `contentType`), API 36 Intent Redirection, `PendingIntent.FLAG_IMMUTABLE`, and `secrets-gradle-plugin`; verify mutations via `./gradlew build --dry-run` (RAW).

## 4. Gotchas & Edge Cases

- Never add `@Immutable`/`ImmutableList` blindly to large `LazyColumn` collections under Strong Skipping Mode ($O(N)$ `.equals()` penalty).
- Never run `./gradlew clean` for sync; under `system-project-auditor`, stay Read-Only until HITL; zero hardcoded secrets.

## 5. Output Schema & Validation Criteria

Emit per [`rules/audit_criteria.md`](rules/audit_criteria.md) (`>= 85/100`: UDF `25` + AGP 9/KSP2 `25` + Build/R8/ANR `25` + Compose/48dp `25`): Synthesis (`[ASSUMPTION ADOPTED]`), 5-Axis Matrix, placeholder-free snippets, and `./gradlew --version`, `./gradlew build --dry-run`, `./gradlew :app:analyzeReleaseR8Config`.

## 6. User Communication Rule

All direct responses, 5-axis diagnoses, clarifying questions, and summaries to the end user MUST be in **Portuguese (Brazil / `pt-BR`)**, unless explicitly requested otherwise.
