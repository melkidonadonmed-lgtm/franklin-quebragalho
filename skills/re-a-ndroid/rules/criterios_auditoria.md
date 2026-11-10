# CRITÉRIOS DETERMINÍSTICOS DE AUDITORIA E REJEIÇÃO (`re-a-ndroid` v2.0.0)

Para garantir auditorias Android reprodutíveis, baseadas em evidências físicas do **REA (`Reverse Engineer Anything`)** e do **Android CLI (`ADB`)**, cada achado é classificado sob três marcadores formais:

- `[PASS]`: Requisito validado com evidência rastreável (`Evidence-ID`, dump XML ou logcat) e dentro dos limiares matemáticos.
- `[FAIL]`: Vulnerabilidade de binário/assinatura, função placebo, rota órfã, violação de acessibilidade ($< 48\text{dp}$) ou regressão de latência.
- `[UNVERIFIED]`: Impossibilidade física de verificação (ex.: dispositivo ADB desconectado para teste dinâmico, restrito à análise estática).

---

### Regra 1: Integridade Binária, Assinaturas APK (`v2/v3+`) e Componentes Exportados (Módulos 1 e 2)

- **Critério**: O APK exige esquema de assinatura moderna (`v2` e `v3`/`v3.1`, imune a *Janus*), não habilita `android:debuggable="true"` em release e protege *Activities*, *Services*, *BroadcastReceivers* e *ContentProviders* com `android:exported="false"` (ou permissão explícita)?
- **Teste**:
  - Assinatura exclusivamente `v1` (JAR signing) ou `android:debuggable="true"` em build de produção -> `[FAIL: ASSINATURA_FRACA_OU_DEBUGGABLE_ATIVO]`
  - Componente sensível com `android:exported="true"` sem permissão de proteção -> `[FAIL: COMPONENTE_EXPORTADO_EXPOSTO]`
  - Assinaturas v2/v3 íntegras e superfície do `AndroidManifest.xml` blindada -> `[PASS]`

### Regra 2: Segurança de Rede, SSL Pinning e Erradicação de Código Placebo (Módulos 4 e 5)

- **Critério**: Todas as comunicações de API/WebSocket utilizam TLS (`https://`, `wss://`), implementam validação real de certificado/SSL Pinning e estão livres de funções placebo (`isRooted() -> false`, `verifyToken() -> true`, `checkServerTrusted` vazio) e de dependências com CVEs críticos abertos?
- **Teste**:
  - Método de segurança/autenticação retornando constante booleana fixa (`return true;` / `return false;`) ou `TrustManager` vazio -> `[FAIL: FUNCAO_PLACEBO_DE_SEGURANCA_DETECTADA]`
  - Tráfego em texto claro (`http://`, `ws://`, `cleartextTrafficPermitted="true"`) ou CVE crítico sem patch -> `[FAIL: REDE_INSEGURA_OU_CVE_ABERTO]`
  - Transporte criptografado, dependências íntegras e $\text{FNR} < 0.001$ -> `[PASS]`

### Regra 3: Qualidade de Rotas, Latência de Boot ($L_{\text{cold}}$) e Fluidez Visual (Módulos 3, 6 e 8)

- **Critério**: O tempo médio de *Cold Start* ($L_{\text{cold}}$ via `am start -W`) mantém-se dentro do orçamento de SLA, o grafo de navegação (`NavGraph` / Compose Navigation) não contém rotas órfãs/mortas ($P = 1$) e a confiabilidade funcional E2E atinge $\text{Pass}@k \ge 0.90$?
- **Teste**:
  - Destinos declarados no grafo de navegação sem referências de acionamento na UI -> `[FAIL: ROTA_ORFA_DETECTADA]`
  - Latência de *Cold Start* excessiva ($L_{\text{cold}} > 3000\text{ms}$) ou *jank* severo em `dumpsys gfxinfo` -> `[FAIL: LATENCIA_BOOT_OU_JANK_CRITICO]`
  - Rotas conectadas, boot otimizado e fluxo E2E estável -> `[PASS]`

### Regra 4: Acessibilidade (`contentDescription`), Touch Targets ($\ge 48\text{dp}$) e Haptics (Módulo 7)

- **Critério**: Todos os nós interativos (`clickable="true"`) possuem rótulo legível por leitor de tela (`text` ou `content-desc`), respeitam a área mínima de toque de $48 \times 48\text{dp}$ ($T_{\text{ratio}} = 1.0$) e acionam feedback tátil (`HapticFeedbackConstants`) em ações críticas?
- **Teste**:
  - Elemento clicável sem `contentDescription`/`text` ou com largura/altura $< 48\text{dp}$ no `window_dump.xml` -> `[FAIL: ACESSIBILIDADE_OU_TOUCH_TARGET_INVALIDO]`
  - Conformidade plena de rótulos, dimensões $\ge 48\text{dp}$ e haptics integrados -> `[PASS]`
