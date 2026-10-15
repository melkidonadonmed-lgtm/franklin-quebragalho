# Especificação dos Módulos das Subskills de Auditoria de Código (Física 3D, Sanitização e Testes)

Este documento detalha os **5 Módulos de Subskills** que compõem o grupo de agentes auditores de qualidade de código. Cada subskill opera sob a arquitetura de divulgação progressiva e isolamento de contexto (`context: fork`), possuindo regras estritas de verificação, algoritmos de teste e rúbrica de pontuação individual.

---

## 1. Módulo Subskill: `static-sanitization-auditor`

### 1.1 Metadados da Subskill
* **Nome:** `static-sanitization-auditor`
* **Finalidade:** Realizar varredura estática no AST (Abstract Syntax Tree) para eliminar código morto, funções duplicadas, estruturas inalcançáveis e vazamento de memória em laços críticos de animação.
* **Peso no Escore Global (\(w_1\)):** **20%**
* **Ferramentas Utilizadas:** `static_ast_parser.py` (Python), `js_ts_ast_parser.js` (JS/TS Node.js).

### 1.2 Regras de Verificação Estrita
1. **Alocação de Memória em Laço Crítico (`ALLOC_IN_LOOP`):** Identifica instanciação de objetos (`new Vector3()`, `new Matrix4()`, `np.zeros()`) dentro das funções de laço (`update`, `render`, `step`, `animate`, `tick`, `requestAnimationFrame`).
2. **Funções Duplicadas (`DUPLICATE_FUNCTION`):** Compara a AST normalizada do corpo das funções. Se duas funções possuem estruturas de nós idênticas (mesmo alterando nomes de variáveis locais), sinaliza duplicação.
3. **Funções Mortas / Código Inalcançável (`DEAD_CODE_FUNCTION`):** Mapeia todas as funções declaradas e cruza com a lista de símbolos invocados em todo o projeto.
4. **Variáveis Declaradas Não Utilizadas (`UNUSED_VARIABLE`):** Identifica alocação de registradores na memória sem leitura posterior.

### 1.3 Algoritmo e Matriz de Pontuação (\(s_1 \in [0, 100]\))
A nota inicia em **100** e sofre deduções acumulativas com base nos erros encontrados:

$$\text{Nota Bruta } (s_1) = \max\left(0, 100 - \sum \text{Penalidades}\right)$$

| Código da Falha | Descrição | Severidade | Penalidade por Ocorrência |
| :--- | :--- | :--- | :--- |
| `ALLOC_IN_LOOP` | Instanciação de objeto/vetor no laço 3D | Crítica | **-30 pontos** |
| `DUPLICATE_FUNCTION` | Função sintaticamente idêntica a outra | Alta | **-20 pontos** |
| `DEAD_CODE_FUNCTION` | Função declarada que nunca é chamada | Média | **-10 pontos** |
| `UNUSED_VARIABLE` | Variável sem referência de leitura | Baixa | **-5 pontos** |

---

## 2. Módulo Subskill: `architecture-hardcoded-auditor`

### 2.1 Metadados da Subskill
* **Nome:** `architecture-hardcoded-auditor`
* **Finalidade:** Auditar a modularidade do projeto, separação entre motor de física/math e camada de visualização/canvas, e caçar números mágicos (hardcoded values).
* **Peso no Escore Global (\(w_2\)):** **15%**
* **Ferramentas Utilizadas:** Parser AST de Literais e Validador de Acoplamento.

### 2.2 Regras de Verificação Estrita
1. **Caça a Números Mágicos (`HARDCODED_MAGIC_NUMBER`):** Detecta constantes numéricas literais (ex: `9.81`, `0.01667`, `1000`) inseridas diretamente dentro de equações ou funções operacionais sem atribuição a variáveis globais ou de configuração.
2. **Violação de Modularidade / Acoplamento 3D:** Detecta quando classes de física ou matemática contêm referências diretas a instâncias de renderização (`canvas`, `WebGLRenderingContext`, `THREE.Mesh`, `document.getElementById`).
3. **Falta de Injeção de Parâmetros:** Verifica se as entidades de simulação usam configurações rígidas em vez de receberem um dicionário/objeto de configuração no construtor.

### 2.3 Algoritmo e Matriz de Pontuação (\(s_2 \in [0, 100]\))

$$\text{Nota Bruta } (s_2) = \max\left(0, 100 - \sum \text{Penalidades}\right)$$

| Código da Falha | Descrição | Severidade | Penalidade por Ocorrência |
| :--- | :--- | :--- | :--- |
| `PHYSICS_RENDER_COUPLING` | Código de física manipulando elementos de tela/DOM | Crítica | **-35 pontos** |
| `HARDCODED_MAGIC_NUMBER` | Número mágico inserido em equações sem constante nomeada | Baixa/Média | **-10 pontos** |
| `RIGID_CONSTRUCTOR` | Entidade física sem injeção de parâmetros de configuração | Média | **-15 pontos** |

---

## 3. Módulo Subskill: `physics-3d-math-auditor`

### 3.1 Metadados da Subskill
* **Nome:** `physics-3d-math-auditor`
* **Finalidade:** Auditar rigorosamente a integridade da simulação física 3D, equações de integração, álgebra vetorial e estabilidade numérica contra erros de floating point.
* **Peso no Escore Global (\(w_3\)):** **25%**
* **Ferramentas Utilizadas:** AST Inspector de Expressões Matemáticas e Analisador Numérico.

### 3.2 Regras de Verificação Estrita
1. **Atualização Sem Delta Time (`MISSING_DELTA_TIME`):** Valida se toda modificação incremental de posição (`pos += vel`) contém multiplicação pelo delta time (`dt` ou `deltaTime`).
2. **Normalização Insegura (`UNCHECKED_NORMALIZE`):** Verifica se chamadas ao método `.normalize()` são precedidas por um guardrail que confirma magnitude maior que zero (`||v|| > EPSILON`), prevenindo infecção por `NaN`.
3. **Uso de Ângulos de Euler para Rotação Acumulada (`EULER_GIMBAL_LOCK`):** Verifica se acúmulos de rotação contínuos usam Euler em vez de Quaternions ou matrizes de rotação.
4. **Comparação Estrita de Floats (`STRICT_FLOAT_COMPARE`):** Detecta o uso de igualdade direta (`==` ou `===`) entre números de ponto flutuante.
5. **Ausência de Amortecimento Físico (`MISSING_DAMPING`):** Garante que simulações de corpos rígidos possuam coeficientes de atrito ou arrasto (*drag*).

### 3.3 Algoritmo e Matriz de Pontuação (\(s_3 \in [0, 100]\))

$$\text{Nota Bruta } (s_3) = \max\left(0, 100 - \sum \text{Penalidades}\right)$$

| Código da Falha | Descrição | Severidade | Penalidade por Ocorrência |
| :--- | :--- | :--- | :--- |
| `MISSING_DELTA_TIME` | Incremento de posição/velocidade sem fator de tempo (`dt`) | Crítica | **-40 pontos** |
| `UNCHECKED_NORMALIZE` | Normalização de vetor sem checagem de vetor nulo | Alta | **-25 pontos** |
| `EULER_GIMBAL_LOCK` | Rotações 3D contínuas usando Ângulos de Euler | Alta | **-20 pontos** |
| `STRICT_FLOAT_COMPARE` | Comparação direta de float com `==` ou `===` | Média | **-15 pontos** |
| `MISSING_DAMPING` | Falta de coeficiente de atrito/amortecimento em corpos | Média | **-15 pontos** |

---

## 4. Módulo Subskill: `deterministic-tests-auditor`

### 4.1 Metadados da Subskill
* **Nome:** `deterministic-tests-auditor`
* **Finalidade:** Executar a suíte de testes dinâmicos e determinísticos em ambiente isolado (`context: fork`), medindo o comportamento físico em tempo de execução e a métrica \(Pass@k\).
* **Peso no Escore Global (\(w_4\)):** **20%**
* **Ferramentas Utilizadas:** `physics_test_runner.py` (Test Runner Nativizado).

### 4.2 Baterias de Teste Executadas
1. **Independência de Framerate (60Hz vs 120Hz):** Executa a mesma cena física em dois framerates distintos e mede se a variação da posição final permanece abaixo da tolerância (\(< 0.1\text{m}\)).
2. **Conservação de Energia Total:** Mede a energia mecânica (\(E = E_k + E_p\)) ao longo do tempo para garantir ausência de criação fantasma de energia (\(E_{\text{final}} \le E_{\text{inicial}}\)).
3. **Resistência a Contaminação por NaN:** Injeta força zero e posições limites para garantir que o vetor não retorne `NaN` ou `Infinity`.
4. **Verificação de Atravessamento (Tunneling):** Simula projetéis rápidos contra colidroes finos para garantir retenção do corpo rígido.
5. **Métrica de Reprodutibilidade \(Pass@k\) (\(k=10\)):** Executa a simulação 10 vezes em threads isoladas e valida se todas geram um hash de estado final idêntico.

### 4.3 Algoritmo e Matriz de Pontuação (\(s_4 \in [0, 100]\))
A nota deste módulo reflete diretamente a taxa de aprovação das suítes de testes em tempo de execução:

$$s_4 = \left( \frac{\text{Quantidade de Testes Aprovados}}{\text{Total de Testes Executados}} \right) \times 100$$

* Se todos os 5 testes determinísticos passarem: **\(s_4 = 100\)**.
* Se 1 teste falhar (ex: Teste de FPS Independence): **\(s_4 = 80\)**.

---

## 5. Módulo Subskill (Observador de Estado): `state-checker-observer`

### 5.1 Metadados da Subskill
* **Nome:** `state-checker-observer`
* **Finalidade:** Atuar como o nó de auditoria principal do grupo de subagentes. Monitora a execução dos subagentes executores, valida se os alertas gerados são reais (eliminação de Falsos Positivos), garante cobertura de 100% da base de código e calcula a Nota Normalizada Final (\(S_{\text{norm}}\)).
* **Peso no Escore Global (\(w_5\)):** **20% (Controle de Qualidade & Consolidação)**

### 5.2 Algoritmo de Operação do Observador
1. **Fase de Inspecção de Trajetória:** Recebe as saídas de `static-sanitization-auditor`, `architecture-hardcoded-auditor`, `physics-3d-math-auditor` e `deterministic-tests-auditor`.
2. **Filtro Anti-Alucinação (Validação Cruzada):**
   * Se o Subagente 1 acusou `ALLOC_IN_LOOP` na linha X, o Observador relê a AST na linha X para confirmar se a linha está realmente dentro de um laço de repetição. Caso não esteja, o problema é desconsiderado como **Falso Positivo**.
3. **Consolidação do Escore Normalizado Final (\(S_{\text{norm}}\)):**

$$S_{\text{norm}} = \sum_{j=1}^{4} w_j \cdot s_j + w_5 \cdot s_{\text{observador}}$$

Onde \(s_{\text{observador}}\) avalia a cobertura total dos testes e a coerência da arquitetura.

### 5.3 Estrutura de Saída do Relatório Consolidado pelo Observador
O Observador compila a nota final e gera a matriz explicativa para o usuário:

```markdown
# 🛡️ Relatório Final de Auditoria Integrada

**Escore Normalizado Final (\(S_{\text{norm}}\)):** **[VALOR / 100]**

### Breakdown por Módulo de Subskill:
- 🧹 **Sanitização Estática:** [s_1] / 100 (Peso: 20%)
- 🏗️ **Arquitetura & Hardcoded:** [s_2] / 100 (Peso: 15%)
- 📐 **Física 3D & Matemática:** [s_3] / 100 (Peso: 25%)
- 🧪 **Testes Determinísticos:** [s_4] / 100 (Peso: 20%)
- 👁️ **Qualidade & Observabilidade:** [s_5] / 100 (Peso: 20%)
```
