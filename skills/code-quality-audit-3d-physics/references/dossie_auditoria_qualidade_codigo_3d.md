# Dossiê Técnico e Especificação Mestra: Skill de Auditoria de Qualidade de Código (Física 3D, Análise Estática & Testes Determinísticos)

Este documento compila a especificação completa da **Skill de Auditoria e Sanitização de Código para Sistemas com Física 3D, Computação Gráfica e Engenharia Numérica**. Ele reúne todas as regras de verificação, sistemas de pontuação, arquitetura de subagentes, especificações de módulos, ferramentas estáticas/dinâmicas desenvolvidas e templates de diagnóstico.

---

## 1. Visão Geral e Arquitetura Global do Sistema de Auditoria

A skill foi projetada para avaliar motores de física, simulações e aplicações 3D (trabalhando em Python, C++, WebGL, Three.js, JavaScript ou TypeScript). O objetivo principal é identificar problemas de performance em tempo real (picos de *Garbage Collector*), instabilidades numéricas, dependência de *frame rate*, falta de determinismo e acoplamento arquitetural.

### Fórmula do Escore Normalizado Ponderado Global (\(S_{\text{norm}}\))

A nota final do projeto é expressa em uma escala de **0 a 100**, calculada pela fórmula do escore ponderado:

$$S_{\text{norm}} = \sum_{j=1}^{M} w_j \cdot s_j$$

Onde:
* \(M = 5\) é o número de dimensões/módulos de auditoria.
* \(w_j\) é o peso relativo da dimensão \(j\), com \(\sum w_j = 1.0\) (\(100\%\)).
* \(s_j \in [0, 100]\) é a pontuação bruta obtida na dimensão \(j\).

### Tabela de Dimensões Globais e Pesos

| Dimensão de Auditoria | Módulo de Subskill Responsável | Peso Global (\(w_j\)) | Foco Principal de Verificação |
| :--- | :--- | :--- | :--- |
| **1. Sanitização Estática & Memory Cleanup** | `static-sanitization-auditor` | **20%** | Código morto, funções duplicadas, vazamentos de memória e alocações dentro do laço 3D (`render`/`update`). |
| **2. Modularidade & Ausência de Hardcoded** | `architecture-hardcoded-auditor` | **15%** | Desacoplamento físico-visual, ausência de números mágicos e injeção de dependências. |
| **3. Física 3D & Matemática Numérica** | `physics-3d-math-auditor` | **25% a 30%** | Independência de framerate, Delta Time (\(dt\)), Quaternions, tolerâncias de ponto flutuante e conservação física. |
| **4. Testabilidade & Testes Determinísticos** | `deterministic-tests-auditor` | **20%** | Baterias de simulação dinâmica em tempo de execução e taxa de reprodutibilidade \(Pass@k\). |
| **5. Observabilidade & Controle de Estado** | `state-checker-observer` | **20%** | Validação cruzada (eliminação de falsos positivos), cobertura de arquivos e consolidação da nota final. |

---

## 2. Detalhamento Específico: Dimensão de Física 3D & Matemática Numérica (Peso: 25% a 30%)

A dimensão de **Física 3D e Matemática Numérica** possui isolamento prioritário para garantir que motores de física e simulações gráficas mantenham estabilidade computacional e rigor acadêmico/físico.

### Estrutura Interna das Sub-dimensões de Física 3D

A pontuação da dimensão de física (\(s_{\text{Física}} \in [0, 100]\)) é dividida internamente em 5 sub-dimensões:

$$s_{\text{Física}} = \sum_{k=1}^{5} w_k \cdot S_k$$

| Sub-dimensão Técnica | Peso Interno (\(w_k\)) | Requisitos e Variáveis Obrigatórias | Equações Formais / Validações |
| :--- | :--- | :--- | :--- |
| **1. Integração Temporal & Delta Time** | **25%** | `dt` / `deltaTime`, `accumulator`, `fixedDeltaTime`, `subSteps`. | \(\vec{p}_{t+dt} = \vec{p}_t + \vec{v}_t \cdot dt\)<br>\(\vec{p}_{t+dt} = 2\vec{p}_t - \vec{p}_{t-dt} + \vec{a}_t \cdot dt^2\) |
| **2. Álgebra Vetorial & Rotações 3D** | **25%** | Quaternions (\(q = w + xi + yj + zk\)), Matrizes \(4 \times 4\), `dot()`, `cross()`. | \(\hat{v} = \frac{\vec{v}}{\|\vec{v}\|}\)<br>Vedação contra *Gimbal Lock* |
| **3. Leis de Conservação & Estabilidade** | **20%** | `mass` (\(m > 0\)), `invMass` (\(1/m\)), `gravity` (\(\vec{g}\)), `drag`, `restitution` (\(e\)). | \(\vec{F} = m\vec{g} - c_{\text{drag}}\vec{v}\)<br>\(J = \frac{-(1+e)(\vec{v}_{\text{rel}} \cdot \hat{n})}{\frac{1}{m_A} + \frac{1}{m_B}}\) |
| **4. Detecção de Colisão & CCD** | **15%** | Broadphase (AABB / Octree), `collisionNormal`, `penetrationDepth`, `CCD`. | Prevenção de *Tunneling* em corpos rápidos |
| **5. Robustez Numérica & Float** | **15%** | `EPSILON` (\(10^{-6}\)), `maxSpeed`, `Number.isNaN()`. | \(\|\vec{a} - \vec{b}\| < \epsilon\)<br>Imunidade a divisão por zero |

### Matriz de Penalidades por Severidade (Física 3D)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE DEDUÇÕES DE FÍSICA 3D                        │
├───────────────────┬───────────────────────────────┬───────────────────────┤
│ Nível de Falha    │ Impacto na Nota do Subcritério│ Ação do Subagente     │
├───────────────────┼───────────────────────────────┼───────────────────────┤
│ CRÍTICO           │ Dedução de -40 a -100 pontos  │ Reprova o subcritério │
│                   │                               │ e exige refatoração.  │
├───────────────────┼───────────────────────────────┼───────────────────────┤
│ ALTO              │ Dedução de -25 a -39 pontos   │ Alerta de risco de    │
│                   │                               │ instabilidade no log. │
├───────────────────┼───────────────────────────────┼───────────────────────┤
│ MÉDIO             │ Dedução de -15 a -24 pontos   │ Recomendação de       │
│                   │                               │ otimização matemática.│
├───────────────────┼───────────────────────────────┼───────────────────────┤
│ BAIXO             │ Dedução de -5 a -14 pontos    │ Sugestão de boas      │
│                   │                               │ práticas de código.   │
└───────────────────┴───────────────────────────────┴───────────────────────┘
```

Principais penalidades aplicadas:
* ❌ **Atualização de Posição sem Delta Time (`MISSING_DELTA_TIME`):** **-100 pontos** no subcritério (Falha Crítica).
* ❌ **Uso de Ângulos de Euler para acúmulo contínuo de rotação 3D (`EULER_GIMBAL_LOCK`):** **-50 pontos**.
* ❌ **Normalização de vetor sem checar magnitude zero (`UNCHECKED_NORMALIZE`):** **-40 pontos**.
* ❌ **Comparação direta de floats com igualdade estrita (`STRICT_FLOAT_COMPARE`):** **-40 pontos**.
* ❌ **Objetos velozes atravessando colidroes por falta de Continuous Collision Detection:** **-40 pontos**.
* ⚠️ **Falta de coeficiente de amortecimento (*drag/damping*):** **-30 pontos**.

---

## 3. Arquitetura do Grupo de Subagentes e Observador de Estado

A auditoria é realizada de forma paralela e modular por **5 subagentes especializados**, orquestrados sob a supervisão contínua do **Subagente Observador (*State Checker & Audit Observer*)**.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    SUBAGENTE ORQUESTRADOR DE AUDITORIA                    │
└───────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
│  SUBAGENTE 1:     │       │  SUBAGENTE 2:     │       │  SUBAGENTE 3:     │
│  Sanitização &    │       │  Arquitetura &    │       │  Física 3D &      │
│  Análise Estática │       │  Hardcoded        │       │  Matemática       │
└───────────────────┘       └───────────────────┘       └───────────────────┘
          │                           │                           │
          └───────────────────────────┼───────────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     SUBAGENTE 4: TESTES DETERMINÍSTICOS                   │
└───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                  SUBAGENTE OBSERVADOR & STATE CHECKER                     │
│  • Valida convergência dos achados • Impede alucinações de subagentes    │
│  • Garante sincronização de estado • Compila o Escore Normalizado Final   │
└───────────────────────────────────────────────────────────────────────────┘
```

### Detalhamento dos 5 Módulos de Subskills

#### Módulo 1: `static-sanitization-auditor` (Peso: 20%)
* **Função:** Varredura estática AST para detectar código morto, funções duplicadas e alocações de memória no laço 3D.
* **Erros Mapeados:**
  * `ALLOC_IN_LOOP` (-30 pts): Instanciação de objetos (`new Vector3()`, `Matrix4()`) dentro do laço `update`/`render`.
  * `DUPLICATE_FUNCTION` (-20 pts): Funções com estrutura AST idêntica.
  * `DEAD_CODE_FUNCTION` (-10 pts): Funções declaradas que nunca são chamadas.
* **Fórmula da Nota:** \(s_1 = \max(0, 100 - \sum \text{Penalidades})\)

#### Módulo 2: `architecture-hardcoded-auditor` (Peso: 15%)
* **Função:** Avaliar o desacoplamento entre regras de física e renderização, além de caçar números mágicos.
* **Erros Mapeados:**
  * `PHYSICS_RENDER_COUPLING` (-35 pts): Código de física manipulando elementos do DOM/Canvas diretamente.
  * `RIGID_CONSTRUCTOR` (-15 pts): Classes sem injeção de parâmetros de configuração.
  * `HARDCODED_MAGIC_NUMBER` (-10 pts): Literais numéricos em equações sem constante nomeada.
* **Fórmula da Nota:** \(s_2 = \max(0, 100 - \sum \text{Penalidades})\)

#### Módulo 3: `physics-3d-math-auditor` (Peso: 25%)
* **Função:** Auditar equações físicas, independência de framerate, Quaternions e imunidade a erros numéricos.
* **Erros Mapeados:**
  * `MISSING_DELTA_TIME` (-40 pts): Incrementos de posição sem multiplicação por `dt`.
  * `UNCHECKED_NORMALIZE` (-25 pts): Normalização sem checar `||v|| > 0`.
  * `EULER_GIMBAL_LOCK` (-20 pts): Acúmulo de rotação usando Euler.
  * `STRICT_FLOAT_COMPARE` (-15 pts): Comparação estrita de floats (`==` / `===`).
* **Fórmula da Nota:** \(s_3 = \max(0, 100 - \sum \text{Penalidades})\)

#### Módulo 4: `deterministic-tests-auditor` (Peso: 20%)
* **Função:** Executar a suíte de testes dinâmicos e medir a taxa de aprovação funcional e a métrica \(Pass@k\).
* **Baterias de Testes Executadas:**
  1. Independência de Framerate (60Hz vs 120Hz).
  2. Conservação de Energia Total.
  3. Imunidade a NaN e Divisão por Zero.
  4. Verificação de Atravessamento de Colisores (*Tunneling*).
  5. Reprodutibilidade Determinística \(Pass@k\) (\(k=10\)).
* **Fórmula da Nota:** \(s_4 = \left( \frac{\text{Testes Aprovados}}{\text{Total de Testes Executados}} \right) \times 100\)

#### Módulo 5 (Observador): `state-checker-observer` (Peso: 20%)
* **Função:** Nó central de observabilidade. Realiza validação cruzada para eliminar falsos positivos, verifica cobertura de arquivos (100%) e consolida o Escore Normalizado Final (\(S_{\text{norm}}\)).
* **Algorithmic Flow:**
  1. Coleta saídas dos Subagentes 1 a 4.
  2. Inspeciona o AST e os logs de execução para filtrar falsos alertas.
  3. Compila a nota ponderada global \(S_{\text{norm}}\).

---

## 4. Ferramental Técnico Desenvolvido e Implementado

O ecossistema de auditoria conta com 3 ferramentas prontas e funcionais integradas à skill:

### 1. Analisador AST Python (`static_ast_parser.py`)
Utiliza o módulo nativo `ast` do Python para inspecionar a árvore sintática de arquivos `.py` sem executá-los, identificando alocações em laço, falta de `dt`, números mágicos, comparações estritas de float e funções duplicadas/mortas.

### 2. Analisador AST JavaScript / TypeScript (`js_ts_ast_parser.js`)
Analisador estático desenvolvido em Node.js focado em ecossistemas WebGL, Three.js e Babylon.js. Examina arquivos `.js` e `.ts` em busca de instâncias de `THREE.Vector3` ou `THREE.Matrix4` criadas no laço de animação (`requestAnimationFrame`), falta de `dt` e normalizações inseguras.

### 3. Suíte de Testes Determinísticos 3D (`physics_test_runner.py`)
Executa simulações dinâmicas de corpos rígidos em tempo real, testando invariantes físicos como independência de framerate, conservação de energia mecânica, imunidade a `NaN`, retenção de colisão e reprodutibilidade estrita de estado (\(Pass@k\)).

---

## 5. Formato Padrão do Relatório de Diagnóstico (Template de Problemas)

Todo problema identificado pela Skill deve ser apresentado ao usuário seguindo este formato estruturado:

```markdown
### 🚨 [ID_PROBLEMA] — [TITULO SUCINTO DO ERRO]
* **Dimensão Atingida:** [Física 3D / Sanitização / Modularidade / Hardcoded / Testes]
* **Severidade:** [Crítica / Alta / Média / Baixa]
* **Localização:** `caminho/do/arquivo.ext:linha`

#### 1. Descrição Detalhada do Problema e Causa Raiz
* Explicação técnica precisa do erro e POR QUE ele compromete a estabilidade ou performance do projeto.

#### 2. A MELHOR Forma de Resolver e Justificativa Técnica
* Trecho de código refatorado com as melhores práticas.
* **Por que é a melhor forma:** Detalhamento dos ganhos em Garbage Collection, independência de FPS ou estabilidade matemática.

#### 3. Resultado Esperado Após a Correção
* Métricas quantitativas esperadas (ex: 0 B/s de alocação de memória no laço render, 100% de invariância em framerates distintos).
```

---

## 6. Exemplos de Diagnósticos Resolvidos

### Exemplo 1: Alocação de Memória no Laço 3D
```markdown
### 🚨 [ERR-001] — Alocação de Objeto 3D no Laço de Animação
* **Dimensão Atingida:** Sanitização Estática & Memory Cleanup
* **Severidade:** Crítica
* **Localização:** `src/render/loop.ts:42`

#### 1. Descrição Detalhada do Problema e Causa Raiz
O código instancia `new THREE.Vector3()` dentro da função `animate()`, executada a cada quadro. Isso gera centenas de objetos temporários descartáveis por segundo na Heap.
* **Causa Raiz:** Ausência de reaproveitamento de memória para vetores de cálculo temporário.

#### 2. A MELHOR Forma de Resolver e Justificativa Técnica
```typescript
// Reutilização de objeto pré-alocado (Scratchpad estático)
const TEMP_VECTOR = new THREE.Vector3();

function animate(dt: number) {
  TEMP_VECTOR.copy(entity.position).addScaledVector(entity.velocity, dt);
  mesh.position.copy(TEMP_VECTOR);
}
```
* **Por que é a melhor forma:** Reduz a alocação de memória no laço para 0 bytes, eliminando engasgos (*stuttering*) causados pelas pausas do Garbage Collector.

#### 3. Resultado Esperado
* **Taxa de Alocação:** Reduzida de 15 MB/s para 0 B/s durante a animação.
```

### Exemplo 2: Atualização Física Sem Delta Time
```markdown
### 🚨 [ERR-002] — Atualização de Posição Sem Delta Time (Dependência de Framerate)
* **Dimensão Atingida:** Física 3D & Matemática Numérica
* **Severidade:** Crítica
* **Localização:** `physics/particle.py:88`

#### 1. Descrição Detalhada do Problema e Causa Raiz
A posição da partícula é incrementada com `self.position += self.velocity`, sem multiplicar por `dt`. A velocidade da simulação varia conforme a taxa de atualização do monitor (ex: 60Hz vs 144Hz).

#### 2. A MELHOR Forma de Resolver e Justificativa Técnica
```python
def update(self, dt: float):
    # Posição escalada proporcionalmente ao tempo real decorrido
    self.position += self.velocity * dt
```
* **Por que é a melhor forma:** Garante que a partícula percorra a mesma distância física no mesmo intervalo de tempo real em qualquer dispositivo.

#### 3. Resultado Esperado
* **Independência de FPS:** Variação de posição final menor que 0.01m entre 60Hz e 120Hz no teste determinístico.
```

---

## 7. Resumo do Escore Global de um Projeto Auditado (Exemplo de Saída)

```markdown
# 🛡️ Relatório Final de Auditoria de Qualidade de Código

**Escore Normalizado Final (\(S_{\text{norm}}\)):** **84.5 / 100** (Aprovado com Ressalvas)

### Breakdown por Módulo de Subskill:
- 🧹 **Sanitização Estática:** 90.0 / 100 (Peso: 20%) — 1 alocação temporária detectada.
- 🏗️ **Arquitetura & Hardcoded:** 85.0 / 100 (Peso: 15%) — 2 números mágicos em equações de atrito.
- 📐 **Física 3D & Matemática:** 73.5 / 100 (Peso: 25%) — Falta de Fixed Timestep e normalização insegura.
- 🧪 **Testes Determinísticos:** 100.0 / 100 (Peso: 20%) — 5/5 testes aprovados.
- 👁️ **Qualidade & Observabilidade:** 80.0 / 100 (Peso: 20%) — Validação cruzada concluída sem alucinações.
```
