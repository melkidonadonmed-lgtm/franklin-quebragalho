# Guia de Referência: Critérios de Aprimoramento, Avaliação e Expansibilidade (Padrão 2026)

Este documento constitui o **Tier 3 (Referência Sob Demanda)** da skill `aprimoramento-expansibilidade-agentes-skills`, reunindo as formulações matemáticas, padrões de projeto (Envelope Pattern, Context Forking, Memória em 3 Camadas, MCP/A2A) e a Matriz Comparativa de Maturidade (Níveis 1 a 4).

---

## 1. Critérios de Aprimoramento e Ciclo de Qualidade (*Refinement & Evaluation*)

### 1.1. Avaliação Estruturada (*Eval-Driven Iteration*) e Métricas Formais

1. **Conjuntos de Testes com/sem Skill (*Baseline vs. Treatment*)**:
   - Executa-se o mesmo conjunto fixo de casos (`evals/evals.json`) em duas configurações idênticas:
     - **Baseline ($B$)**: Sem a skill ativada (ou com a versão anterior $v_{n-1}$).
     - **Treatment ($T$)**: Com a nova versão da skill ($v_n$) ativada.
   - Calcula-se o ganho líquido de resolução frente ao custo marginal de tokens e latência:
     $$\Delta \text{PassRate} = \text{PassRate}(T) - \text{PassRate}(B), \quad \text{Eficiência} = \frac{\Delta \text{PassRate}}{\Delta \text{Tokens}}$$

2. **Estimador Matemático Não Enviesado $\text{Pass}@k$**:
   - Para validação funcional de código e scripts gerados, gera-se $n \ge k$ amostras por tarefa e conta-se o número $c$ de amostras que passam em todos os testes unitários:
     $$\text{Pass}@k = 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}}$$

3. **Matriz de Confusão para Guardrails e Redução de Falsos Negativos ($\text{FNR}$)**:
   - Para filtros de segurança, prevenção de perda de dados (DLP) e detecção de *prompt injection*:
     $$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad \text{FNR} = \frac{FN}{TP + FN}$$
   - Em agentes com permissão de escrita ou mutação em disco/bancos transacionais, a tolerância a falsos negativos deve ser estritamente calibrada para **$\text{FNR} < 0.001$**.

4. **Avaliadores `LLM-as-a-Judge` Normalizados ($S_{\text{norm}}$)**:
   - Para avaliar qualidade holística (estrutura, clareza, ergonomia, aderência contratual), utiliza-se um modelo juiz de **família diferente do modelo gerador** (evitando viés de autoavaliação) sobre $M$ critérios ortogonais com pesos $w_i$:
     $$S_{\text{norm}} = \frac{\sum_{i=1}^{M} w_i \cdot s_i}{\sum_{i=1}^{M} w_i \cdot s_{\max}} \times 100 \in [0, 100]$$

---

### 1.2. Diagnóstico de Trajetórias e Transcrições (`transcript.jsonl`)

- **Inspeção de Trajetória**: Analisar os eventos `PLANNER_RESPONSE` e `tool_calls` em `transcript.jsonl`. Se o agente chama ferramentas erradas, repete buscas ou ignora referências, a instrução está ambígua ou mal posicionada.
- **Instruções Enxutas (*Lean Instructions*) e o "Porquê"**:
  - Diretivas baseadas em raciocínio causal (*"Use cópias físicas em vez de junctions no Windows porque scanners Go ignoram reparse points `d----l`"* ) superam regras em caixa-alta (*"SEMPRE COPIE PASTAS"*).
  - Se o $\text{PassRate}$ estagnar ou cair após adicionar novas regras, a skill atingiu **sobre-restrição (*over-constraining*)** — remova regras redundantes.
- **Extração de Lógica Repetitiva para `scripts/`**:
  - Se as transcrições mostram o agente gerando repetidamente o mesmo script Python/PowerShell em tempo de execução (ex: parser de YAML, calculador de hash SHA-256, gerador de tabela), extraia e versione esse código na pasta `scripts/` da skill.

---

### 1.3. Otimização do Gatilho de Ativação (*Trigger Optimization*)

Para calibrar o campo `description` (Tier 1) sem disparos falsos:

| Eixo da Matriz de Teste | Exemplos de Variação Exigidos | Métrica Alvo |
| :--- | :--- | :--- |
| **Consultas Positivas (`should-trigger`)** | Fraseado formal, casual, com typos, implícito (sem citar o nome da skill) e com caminhos reais de arquivos. | $\text{Trigger Rate} \ge 0.90$ |
| **Consultas Negativas Limítrofes (`should-not-trigger` / *Near-Misses*)** | Tarefas do mesmo domínio mas de responsabilidade de outra skill irmã (ex: auditar catálogo vs. criar skill; analisar UI vs. refatorar código UI). | $\text{False Trigger Rate} \le 0.05$ |
| **Divisão Treino / Validação (*Train/Val Split*)** | 70% das queries usadas para ajustar a `description`; 30% retidas (unseen) para testar generalização e impedir *overfitting*. | $\Delta(\text{Train}, \text{Val}) < 0.10$ |

---

### 1.4. Otimização Automatizada (`GEPA` / Google ADK) e Densidade de Atenção (Softmax)

- **Otimização Programática (`adk optimize` / `GEPA`)**: Utilizar evolução guiada por pareto/reflexão sobre traces de falha para refinar iterativamente `system_instruction` e descrições de tools, combinada com **Simulação Sintética de Usuário Multiturno** (personas com objetivos parciais, mudanças de escopo e entradas ruidosas).
- **Maximização da Densidade de Atenção (Softmax)**:
  - No mecanismo de autoatenção:
    $$\alpha_{ij} = \frac{\exp(q_i \cdot k_j / \sqrt{d_k})}{\sum_{l=1}^{N} \exp(q_i \cdot k_l / \sqrt{d_k})}$$
  - Cada bloco irrelevante injetado na janela aumenta $N$ e infla o denominador $\sum_{l=1}^{N} \exp(\dots)$, reduzindo a massa de probabilidade $\alpha_{ij}$ dedicada aos tokens críticos de controle e segurança. Manter o Tier 2 enxuto evita *Context Drift* em execuções longas (20–50 passos).

---

## 2. Padrões de Expansibilidade e Arquitetura Extensível (*Extensibility & Scaling*)

### 2.1. Padrão Envelope (*Envelope Pattern* / Action Routing Polimórfico)

Em vez de registrar dezenas de ferramentas separadas que saturam o Tier 1 do modelo, exponha um contrato Envelope único validado por Pydantic:

```python
from typing import Any, Literal
from pydantic import BaseModel, Field


class SkillActionEnvelope(BaseModel):
    """Interface polimórfica mestre (Envelope Pattern) para roteamento determinístico."""
    action: Literal["diagnose", "refactor", "evaluate", "export"] = Field(
        ..., description="Operação atômica a ser despachada pelo motor interno da skill."
    )
    target_path: str = Field(..., description="Caminho relativo ou identificador do recurso alvo.")
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Parâmetros específicos validados pelo sub-schema correspondente à action."
    )
    dry_run: bool = Field(
        default=True,
        description="Se True, simula o impacto sem aplicar mutações destrutivas."
    )
```

### 2.2. Bifurcação de Contexto (`Context Forking`) e Memória em 3 Camadas

1. **Isolamento via `context: fork` (`invoke_subagent`)**:
   - Tarefas de exploração pesada (varredura de dezenas de arquivos, debugging iterativo, leitura de logs extensos) rodam em janela bifurcada. O subagente absorve todo o ruído intermediário e devolve ao agente principal apenas um resumo estruturado assinado (`< 500` tokens).
2. **Memória Tripartida**:
   - **Camada 1 — Scratchpad Transitório**: Raciocínio local do turno (`scratch/`).
   - **Camada 2 — Estado de Sessão**: Estado vivo da tarefa (`.context/CURRENT_STATE.md`, `.sessions/harness_checkpoints.json`).
   - **Camada 3 — Memory Bank de Longo Prazo**: Notas canônicas no Obsidian (`dev/notes/`) indexadas no MemPalace com proveniência, data ISO e verificação de integridade.

### 2.3. Interoperabilidade (`MCP` + `A2A`) e Governança Centralizada

- **Barramento MCP (JSON-RPC 2.0)**: Servidores isolados (`stdio` ou `Streamable HTTP`) expondo `tools`, `resources` e `prompts` com schemas tipados.
- **Protocolo A2A (`/.well-known/agent-card.json`)**: Metadados padronizados de capacidade, autenticação e contrato de hand-off entre agentes de domínios distintos.
- **Precedência de Escopo e HITL**:
  - Resolução determinística de colisão: `Workspace (.agents/skills/) > Global User (~/.gemini/config/skills/) > Builtin`.
  - Portões `HITL`: Leitura (`Read-Only`) livre; mutação reversível auditada; ações críticas/destrutivas bloqueadas até confirmação humana explícita.

---

## 3. Matriz Comparativa Completa: 4 Níveis de Maturidade Agêntica

| Dimensão de Análise | Nível 1: Prompt Monolítico | Nível 2: Agente de Produto | Nível 3: Context & Intent Eng. | Nível 4: Specification Eng. (Corporativo) |
| :--- | :--- | :--- | :--- | :--- |
| **Escopo / Escala** | Individual / Consulta única | Produto estático / Chatbot | Time / Produto complexo | Corporação / Sistema Multiagente |
| **Arquitetura da Regra** | Regras acumuladas no System Prompt | Instruções fixas do produto | Perfil enxuto + `SKILL.md` modular + Tools | Grafo multiagente com *Specification Corpus* |
| **Divulgação de Contexto** | Envia tudo a cada turno | Janela estática cheia de logs | **Divulgação progressiva em 3 Tiers** | Filtros semânticos + Roteamento dinâmico |
| **Validação de Qualidade** | Avaliação empírica ("parece inteligente") | Casos manuais isolados | **Evals com baselines e métricas ($\text{Pass}@k$)** | Esteiras CI/CD contínuas + `LLM-as-a-Judge` ($S_{\text{norm}}$) |
| **Interoperabilidade** | Código/função customizada ad-hoc | Conectores proprietários | **Servidores MCP e SDKs padronizados** | Barramento MCP + Protocolo A2A e Registros |
