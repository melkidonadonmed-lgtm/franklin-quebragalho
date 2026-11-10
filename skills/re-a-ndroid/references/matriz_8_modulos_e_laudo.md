# Referência Técnica Completa: 8 Módulos, Playbook CLI/MCP e Template de Laudo (`re-a-ndroid` v2.0.0)

## 1. Detalhamento dos 8 Módulos Especializados de Auditoria

### Módulo 1: Propósito Geral e Arquitetura do App

- **Análise Contextual:** Mapeamento do domínio de negócio da aplicação, público-alvo, permissões solicitadas e arquitetura estrutural (MVVM, MVI, Clean Architecture).
- **Inventário de Componentes:** Identificação de todas as *Activities*, *Services*, *BroadcastReceivers* e *ContentProviders* declarados e exportados (`android:exported="true"`) no `AndroidManifest.xml`.

### Módulo 2: Inspeção Estática de Binários, SDKs e Assinaturas (via REA)

- **Descompilação e DEX Parsing:** Leitura de bytecode descompilado via REA/JADX (`inspect_android_package`, `search_android_classes`, `inspect_android_class`, `inspect_android_method`), extração de bibliotecas nativas (`lib/*.so`) e identificação de frameworks cruzados (Flutter, React Native, Unity, Kotlin Multiplatform).
- **SDKs de Terceiros e Analytics:** Catalogação de bibliotecas de anúncios, telemetria e autenticação.
- **Auditoria de Assinatura:** Validação dos esquemas de assinatura do APK (v1, v2, v3, v3.1) para garantir imunidade contra adulteração ou ataque *Janus* (CVE-2017-13156).

### Módulo 3: Inspeção Dinâmica e Visual em Tempo Real (via Android CLI / ADB)

- **Monitoramento de Processo:** Ingestão de métricas de CPU, memória heap/native e threads ativas via `adb shell top` e `adb shell dumpsys meminfo <PACKAGE_NAME>`.
- **Inspeção Visual e Layout Dump:** Extração da árvore estrutural da interface via `adb shell uiautomator dump` e análise de aninhamento excessivo de views/nodes.
- **Logcat & Rastreamento de Erros:** Filtro contínuo de logs em tempo real (`adb logcat *:E` / MCP `read_adb_logcat`) para captura de exceções não tratadas (*NullPointerException*, *ANR*, *StrictMode*).

### Módulo 4: Análise de Pacotes, Vulnerabilidades e Reparo Determinístico

- **Verificação de Dependências:** Comparação dos pacotes Gradle/Maven identificados contra bases conhecidas de vulnerabilidades (OSV.dev, NVD, GitHub Security Advisories).
- **Plano de Atualização & Patching:** Formulação de recomendações de atualização sem regressão de versão em `gradle/libs.versions.toml` ou `build.gradle.kts`, priorizando patches de segurança críticos.

### Módulo 5: Chamadas de API, WebSockets e Detecção de Funções Placebo

- **Interceptação de Tráfego:** Inspeção de endpoints HTTP/REST, conexões de longa duração em WebSockets (`ws://`, `wss://`) e chamadas gRPC/RPC.
- **Validação de Segurança de Rede:** Verificação da presença de SSL Pinning (`network_security_config.xml`, `CertificatePinner` do OkHttp ou `TrustManager` customizado) e detecção de transmissões em texto claro (`http://`, `cleartextTrafficPermitted="true"`).
- **Detecção de Código Placebo / Fake:** Localização de métodos mockados ou estáticos (ex.: `boolean isRooted() { return false; }`, `boolean verifyToken() { return true; }` ou `checkServerTrusted` vazio) que introduzem vulnerabilidades críticas de contorno de segurança.

### Módulo 6: Qualidade de Rotas, Latência e Detectores de Rotas Órfãs

- **Medição de Tempo de Inicialização:** Obtenção exata das latências *Cold Start* e *Warm Start* utilizando `adb shell am start -W -n "<PACKAGE>/<ACTIVITY>"`.
- **Rotas Órfãs e Mortas:** Identificação de telas/destinos definidos em grafos de navegação (`NavGraph` XML ou rotas tipadas Jetpack Navigation 3 / Compose) que não possuem gatilhos de acionamento válidos na UI (`trace_android_references`).
- **Gargalos de Navegação:** Detecção de transições que causam retenção indevida de memória ou bloqueio na thread principal (*Main Thread*).

### Módulo 7: Acessibilidade, Interatividade e Resposta Tátil

- **Rótulos Legíveis (`contentDescription`):** Verificação da presença de descrições textuais em elementos gráficos interativos (`ImageButton`, `Icon`, nodes com `clickable="true"` e `text=""`).
- **Dimensões do Target de Toque:** Garantia de que todos os botões e áreas clicáveis respeitam a área mínima recomendada de $48 \times 48\text{dp}$.
- **Resposta Multissensorial (*Haptic Feedback*):** Confirmação da integração com as APIs de vibração do sistema (`HapticFeedbackConstants`, `LocalHapticFeedback` no Compose ou `Vibrator`/`VibrationEffect`) em momentos críticos de confirmação ou erro.

### Módulo 8: Testes E2E e Composição de Layout (Render Performance)

- **Automação de Fluxos E2E:** Simulação automatizada de interações do usuário (toques, deslizes, preenchimento de formulários) via scripts ADB e inspeção de estado pós-ação.
- **Análise de Fluidez Visual (*Jank Rate*):** Medição da taxa de quadros perdidos (*dropped frames* / *janky frames*) durante animações ou rolagem de listas complexas via `adb shell dumpsys gfxinfo <PACKAGE_NAME> framestats`.

---

## 2. Playbook de Comandos REA CLI/MCP & ADB

### Etapa 1: Ingestão e Descompilação Estática (REA)

```bash
# Resumo estrutural do APK e geração de bundle de evidências
rea inspect-android-package "[CAMINHO_DO_APK]" --detail summary --evidence_output ./apk-summary.json --json

# Validação dos esquemas de assinatura digital (v1, v2, v3, v3.1)
rea inspect-apk-signature "[CAMINHO_DO_APK]" --json
```

### Etapa 2: Inspeção Dinâmica e Visual em Tempo Real (ADB)

```bash
# Medir Cold/Warm Start (WaitTime / TotalTime em ms)
adb shell am start -W -n "[PACKAGE_NAME]/[LAUNCHER_ACTIVITY]"

# Extrair árvore de acessibilidade e bounds da UI atual
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml ./window_dump.xml

# Coletar estatísticas de renderização e jank de frames
adb shell dumpsys gfxinfo "[PACKAGE_NAME]" framestats
```

### Etapa 3: Execução do Validador Determinístico Local (`scripts/rea_android_auditor.py`)

```bash
python skills/re-a-ndroid/scripts/rea_android_auditor.py --self-test
python skills/re-a-ndroid/scripts/rea_android_auditor.py --window-dump ./window_dump.xml --dpi 420 --json
```

---

## 3. Matriz do Laudo Final de Auditoria (Template Self-Refine)

```markdown
# 📋 LAUDO DE AUDITORIA DE APP ANDROID: RE-A-NDROID

## METADADOS DA AUDITORIA
- **Aplicativo:** `[PACKAGE_NAME]`
- **Versão:** `[VERSION_NAME] ([VERSION_CODE])`
- **Hash SHA-256 do APK:** `[HASH_SHA256]`
- **Esquema de Assinatura:** `[v1/v2/v3/v3.1 Status]`
- **Dispositivo de Teste:** `[Modelo / Versão do Android / API Level]`

---

## 1. TABELA CONSOLIDADA DE ACHADOS E CORREÇÕES

| ID | Categoria | Componente / Rota | Problema Detectado | Nível de Risco | Evidência Rastreável | Ação Corretiva Determinística |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Binário / SDK | `libnative.so` | Dependência `vulnerable-sdk:1.2` (CVE-2025-XXXX) | 🔴 Crítico | `apk-summary.json#m1` | Atualizar dependência para versão `1.4.0`. |
| **PLC-01** | Código Placebo | `RootChecker.java` | Método `isDeviceRooted()` retorna estático `false` | 🔴 Crítico | `classes.dex:L104` | Substituir por verificação real via Play Integrity API / checagem nativa. |
| **ACC-01** | Acessibilidade | `btn_submit` | Ausência de `contentDescription` em botão gráfico | 🟡 Médio | `window_dump.xml:L42` | Inserir `android:contentDescription="@string/btn_submit_desc"`. |
| **PERF-01**| Desempenho | `/CheckoutActivity` | Latência de boot a frio de 3800ms ($TotalTime$) | 🟡 Médio | `am_start.log:L12` | Otimizar inicialização assíncrona de SDKs com `AppStartup` / `Dispatchers.IO`. |
| **NAV-01** | Rotas | `/legacy_payment` | Rota órfã com parâmetros de teste hardcoded | 🟢 Baixo | `NavGraph.xml:L88` | Remover rota não utilizada do grafo de navegação. |

---

## 2. MÉTRICAS MATEMÁTICAS CALCULADAS
- **Confiabilidade Funcional ($\text{Pass}@k$):** `98.5%` (para $n=10, k=1$)
- **Latência Média de Boot A Frio ($L_{\text{cold}}$):** `2100 ms`
- **Taxa de Conformidade de Acessibilidade ($A_{\text{rate}}$):** `84.2%`
- **Razão de Touch Target Válido ($T_{\text{ratio}}$):** `91.0%` ($\ge 48\text{dp}$)
- **Densidade Ciclomática de Rotas ($M_{\text{rotas}}$):** `14`
- **Taxa de Falsos Negativos em Segurança ($\text{FNR}$):** `0.0000` ($< 0.001$)

---

## 3. INSTRUÇÕES DETERMINÍSTICAS DE REPARO PARA O DEEP CODER

### Reparo 1: Eliminação de Função Placebo em `RootChecker.java`
- **Arquivo Alvo:** `app/src/main/java/com/example/app/security/RootChecker.java`
- **Ação:** Substituir implementação simulada por verificação real de integridade (Play Integrity API e inspeção de binários `su` / propriedades `ro.build.tags`).

### Reparo 2: Correção de Acessibilidade no Layout `activity_main.xml`
- **Arquivo Alvo:** `app/src/main/res/layout/activity_main.xml`
- **Ação:** Ajustar dimensões mínimas dos botões para $48 \times 48\text{dp}$ (`minWidth="48dp"`, `minHeight="48dp"`) e adicionar atributos `contentDescription` para leitores de tela (TalkBack).
```
