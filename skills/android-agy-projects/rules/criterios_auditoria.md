# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`android-agy-projects` v2.1.0)

Para garantir diagnósticos objetivos, falsificáveis e ancorados na documentação oficial do Android Studio (2026), o agente avalia cada entrega sob três marcadores estritos:

- `[PASS]`: Requisito integralmente atendido e compatível com AGP 9.x / Kotlin 2.3–2.4+ / Compose BOM `2026.09.00`.
- `[FAIL]`: Violação direta de regra de build, anti-pattern de recomposição, dependência obsoleta (`kapt`) ou falha de segurança.
- `[UNVERIFIED]`: Impossibilidade de verificação por ausência de acesso ao arquivo `libs.versions.toml` ou `build.gradle.kts`.

---

### Regra 1: Verificação Zero-Trust de Versões, Built-in Kotlin (AGP 9.x) e Erradicação do `kapt`

- **Critério**: O projeto utiliza Version Catalogs (`gradle/libs.versions.toml`) com versões estáticas atualizadas, substituiu `kapt` por `com.google.devtools.ksp` (`2.3.6+` / `2.3.12`) e, quando em AGP 9.0+, removeu o plugin redundante/incompatível `org.jetbrains.kotlin.android` em favor do *Built-in Kotlin*?
- **Teste**:
  - Uso de `kapt` em Room/Hilt/Moshi ou versões dinâmicas (`18.+`) -> `[FAIL: KAPT_OU_VERSAO_DINAMICA_DETECTADA]`
  - Aplicação manual de `org.jetbrains.kotlin.android` em módulo `com.android.application` sob AGP 9.0+ com `android.newDsl=true` -> `[FAIL: PLUGIN_KOTLIN_ANDROID_CONFLITANTE_AGP9]`
  - Catálogo `libs.versions.toml` íntegro, KSP2 ativo e plugins compatíveis com a versão do AGP -> `[PASS]`

### Regra 2: Estabilidade do Jetpack Compose (`1.12+/1.13+`), *Phase Deferral* e Layouts Lazy

- **Critério**: Os containers `LazyColumn`/`LazyRow`/`LazyGrid` declaram `key` primitiva e `contentType`, as leituras de estado rápidas são adiadas para Layout/Draw via lambdas (`Modifier.offset { ... }`, `Modifier.graphicsLayer { ... }`), não há *Backwards Writes* e não foram adicionadas anotações `@Immutable`/`ImmutableList` em modelos com grandes coleções sob *Strong Skipping Mode*?
- **Teste**:
  - `items(...)` em `LazyColumn` sem `key` ou sem `contentType` -> `[FAIL: LAZY_SEM_KEY_OU_CONTENT_TYPE]`
  - Adição de `@Immutable` / `@Stable` / `ImmutableList` em modelo contendo `List`/`Set`/`Map` de grande porte para `LazyColumn` -> `[FAIL: PENALIDADE_EQUALS_ON_STRONG_SKIPPING]`
  - Uso de `Modifier.composed` legado em vez de `ModifierNodeElement` + `Modifier.Node` -> `[FAIL: MODIFIER_COMPOSED_LEGADO]`
  - Recomposição otimizada, fases respeitadas e slots reutilizáveis -> `[PASS]`

### Regra 3: Otimização R8 Full Mode, Higiene do `gradle.properties` e Baseline Profiles

- **Critério**: O build `release` ativa o R8 com `optimization { enable = true }` (AGP 9.3+) ou `isMinifyEnabled = true` + `isShrinkResources = true` + `proguard-android-optimize.txt` (pré-AGP 9.3), sem `proguard-android.txt` e sem flags banidas no AGP 9.0+ (`android.r8.integratedResourceShrinking`, `android.enableR8.fullMode=false`)?
- **Teste**:
  - Presença de `android.enableR8.fullMode=false` ou uso de `proguard-android.txt` -> `[FAIL: R8_DESATIVADO_OU_NAO_OTIMIZADO]`
  - Presença de propriedades banidas no AGP 9.0 (`android.r8.integratedResourceShrinking` ou `android.enableNewResourceShrinker.preciseShrinking`) -> `[FAIL: PROPRIEDADE_GRADLE_BANIDA_AGP9]`
  - R8 Full Mode ativo, regras de keep estritas (`<init>();` quando aplicável) e Configuration Cache habilitado -> `[PASS]`

### Regra 4: Edge-to-Edge (API 35/36+), Navegação 3 e Concorrência Segura

- **Critério**: As `ComponentActivity` chamam `enableEdgeToEdge()` antes de `setContent`, aplicam insets sem padding duplo (`WindowInsets.safeDrawing` / `WindowInsetsRulers.Ime.current`), coletam fluxos com `collectAsStateWithLifecycle()` e isolam I/O em `Dispatchers.IO`?
- **Teste**:
  - Operação de banco/rede/JSON na Main Thread ou dentro do corpo de um `@Composable` -> `[FAIL: BLOQUEIO_MAIN_THREAD_OU_SIDE_EFFECT_NO_BODY]`
  - Ausência de `enableEdgeToEdge()` ou falta de tratamento de insets/IME em telas com `compileSdk >= 35` -> `[FAIL: VIOLACAO_EDGE_TO_EDGE_API36]`
  - Edge-to-Edge, Navigation 3 / Type-Safe Navigation e Coroutines estruturadas em conformidade -> `[PASS]`

### Regra 5: Segurança Android 16 (API 36), Segredos e Estrutura de Resposta

- **Critério**: Nenhum segredo foi hardcoded no código/manifesto (uso de `secrets-gradle-plugin`), `PendingIntent`s e lançamentos de `Intent` seguem o endurecimento contra *Intent Redirection* do Android 16, e a resposta entregou os 4 blocos obrigatórios (Síntese, Análise/Matriz, Código Executável e Próximo Passo)?
- **Teste**:
  - Chave de API ou token hardcoded em Kotlin, XML ou `build.gradle.kts` -> `[FAIL: SEGREDO_HARDCODED_ANDROID]`
  - Omissão da análise de causa raiz (Cenário B) ou da Matriz de Oportunidades (Cenário C) -> `[FAIL: ENTREGA_INCOMPLETA]`
  - Segurança validada e entregável completo com pontuação Self-Refine $\ge 85/100$ -> `[PASS]`
