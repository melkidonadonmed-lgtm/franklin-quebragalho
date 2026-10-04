# Diretrizes para Elaboração da Matriz de Decisão Go/No-Go

Este documento estabelece as diretrizes para a formulação de portões de qualidade e critérios de avanço determinísticos pelo `high-level-context-planner`.

---

## 1. Princípio da Falsificabilidade em Portões de Qualidade

Critérios de aceite não podem se basear em avaliações subjetivas ("verificar se ficou bom", "testar funcionamento geral"). Devem ser expressos em asserções estritamente falsificáveis:
- Códigos de saída de terminal (`$LASTEXITCODE -eq 0`).
- Existência de caminhos ou arquivos no disco (`Test-Path`).
- Presença de campos obrigatórios em payloads ou schemas JSON.
- Status booleano emitido por testes unitários ou de integração.

---

## 2. Estrutura Canônica de um Portão Go/No-Go

Para cada fase planejada, a matriz deve definir:

1. **Condição de Aprovação (Go)**: O estado factual verificável que autoriza a transição para a próxima fase.
2. **Condição de Bloqueio (No-Go)**: O desvio, erro de terminal, estouro de timeout ou quebra de contrato que impede a continuação.
3. **Rota de Contingência**: A ação alternativa imediata a ser tomada sem travar o operador em loops cegos:
   - Acionar `gap-analyzer-auditor` para RCA automático.
   - Reverter para checkpoint anterior de backup.
   - Suspender para alinhamento interativo com o desenvolvedor (`ask_question`).

---

## 3. Matriz Padronizada de Transições

| Fase | Condição Go (Aprovação) | Condição No-Go (Bloqueio) | Rota de Contingência |
| :--- | :--- | :--- | :--- |
| **Fase 0: Pré-requisitos** | Variáveis presentes, caminhos validados e schemas compilados sem erro. | Dependência ausente ou variáveis de ambiente indefinidas. | Parar e solicitar insumos ao desenvolvedor via `ask_question`. |
| **Fases Intermediárias** | Script executado com exit code 0 e asserção de estado pós-modificação comprovada. | Falha de compilação, exceção de runtime ou violação de contrato de dados. | Disparar `gap-analyzer-auditor` com trace de execução e logs. |
| **Fase Final: Release** | Suíte de validação aprovada (`validate_skills.py` 100% PASS) e índice reindexado. | Inconformidade de schema ou falha em testes de regressão. | Bloqueio de release e geração de relatório de gaps. |
