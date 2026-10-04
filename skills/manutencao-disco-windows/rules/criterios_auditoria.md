# Critérios Determinísticos de Auditoria: manutencao-disco-windows

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Preservação de Launchers e Cockpit):** Arquivos essenciais do Desktop (`Cockpit-Melki.html`, scripts `.cmd`) são protegidos e nunca movidos.
- `[FAIL]` **Critério 01:** Tentativa de mover ou renomear arquivos de launcher do desenvolvedor na Área de Trabalho.

- `[PASS]` **Critério 02 (Simulação Dry-Run Prévia):** Movimentações de arquivos em Downloads ou Desktop apresentam lista prévia com `-WhatIf`.
- `[FAIL]` **Critério 02:** Execução direta de comandos de transferência sem simulação exibida ao usuário.

- `[PASS]` **Critério 03 (Destino Seguro de Projetos Dev):** Projetos inativos em `dev/` são movidos exclusivamente para `dev/_arquivo/` sem deleção.
- `[FAIL]` **Critério 03:** Execução de comando de exclusão direta de qualquer pasta de projeto dentro de `C:\Users\melki\dev\`.

- `[PASS]` **Critério 04 (Tratamento de Arquivos em Uso):** Verificação defensiva de locks de arquivo antes de operações de movimentação.
- `[FAIL]` **Critério 04:** Falha silenciosa de comando de movimentação decorrente de arquivo bloqueado por processo ativo.
