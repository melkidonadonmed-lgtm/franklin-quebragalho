# Taxonomia de Causa-Raiz (RCA) e Classificação de Anomalias

Este documento especifica a taxonomia analítica aplicada pelo `gap-analyzer-auditor` para dissecação de falhas em processos de IA e engenharia de software.

---

## 1. Classificação Epistêmica da Evidência

Antes de qualquer conclusão diagnóstica, toda linha de raciocínio deve ser demarcada:

| Marcador | Definição | Critério de Aceite |
| :--- | :--- | :--- |
| **`[FATO]`** | Evidência documental explícita | Registro comprovado no log, código fonte, retorno de chamada HTTP ou mensagem de erro textual. |
| **`[INFERÊNCIA]`** | Dedução analítica causal | Conexão lógica entre os fatos observados e o comportamento esperado do sistema. |
| **`[LACUNA]`** | Ausência de dado crítico | Ponto de incerteza onde o log foi truncado, omitido ou não contém insumos suficientes para confirmação. |

---

## 2. Os 4 Vetores de Causa-Raiz (Root Cause Vectors)

### Vetor 1: Falha de Contexto / Injeção (Prompt & Data)
- **Sintomas**: Parâmetros ausentes, alucinação de entidades, quebra de formatação de saída, contaminação entre turnos (*context drift*) ou tentativa de injeção de prompt.
- **Diagnóstico Típico**: Prompts sem separação clara de papéis, ausência de delimitação em tags XML, schemas JSON permissivos demais.

### Vetor 2: Falha de Ferramenta / Protocolo MCP (Tools & Connectors)
- **Sintomas**: Erros 4xx/5xx de APIs externas, estouro de tempo limite (*timeout*), retorno de dados malformados, violação de tipos em argumentos de ferramentas.
- **Diagnóstico Típico**: Discrepância na especificação do MCP (ex.: ferramentas sem suporte a schema v2026-07-28), falta de tratamento defensivo de retornos vazios.

### Vetor 3: Gargalo de Arquitetura (Execution Graph & Performance)
- **Sintomas**: Loops de orquestração sem critério de parada, chamadas recursivas redundantes, consumo excessivo da janela de contexto (*token budget exceeded*), bloqueios síncronos em threads de I/O.
- **Diagnóstico Típico**: Dependência circular entre nós do grafo de agentes, ausência de parâmetros de corte (`max_iterations`, `timeoutMs`).

### Vetor 4: Risco de Segurança e Confiabilidade (Zero-Trust & Safety)
- **Sintomas**: Comandos que executam deleções não confirmadas (`rm -rf`, `DROP TABLE`), credenciais expostas em texto aberto, geração de código sem sandbox.
- **Diagnóstico Típico**: Ausência de aprovação humana (*Human-in-the-Loop* - HITL), falha em callbacks `BeforeToolCallback` de sanitização.

---

## 3. Matriz de Severidade e Status do Veredito

- **`CRÍTICO`**: Falha bloqueante que inviabilizou a conclusão da tarefa, risco de perda irreversível de dados ou vulnerabilidade de segurança. Exige parada imediata e intervenção.
- **`ALERTA`**: Falha em etapa secundária, recuperação parcial com degradação de funcionalidade ou inconsistência latente de schema.
- **`SUBÓTIMO`**: O fluxo foi concluído, porém com ineficiência mensurável (consumo desnecessário de tokens, latência elevada ou complexidade excessiva).
- **`CONFORME`**: Processo auditado sem brechas ou inconsistências detectadas contra o plano original.
