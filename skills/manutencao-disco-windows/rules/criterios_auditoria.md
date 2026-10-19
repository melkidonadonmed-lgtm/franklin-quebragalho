# Critérios Determinísticos de Auditoria — `manutencao-disco-windows` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M4 (Operações Locais Windows 11 / PowerShell)**:

---

- **`[PASS]` Critério 01 (Preservação de Launchers e Cockpit):** Arquivos essenciais do Desktop (`Cockpit-Melki.html`, scripts `.cmd`, `.lnk` ativos) são protegidos e nunca movidos.
- **`[FAIL: LAUNCHER_AFETADO]` Critério 01:** Tentativa de mover, renomear ou excluir arquivos de launcher na Área de Trabalho.
- **`[UNVERIFIED]` Critério 01:** Diretório Desktop ou Downloads inacessível na sessão atual.

- **`[PASS]` Critério 02 (Simulação Dry-Run Prévia e `-LiteralPath`):** Movimentações de arquivos em Downloads ou Desktop apresentam lista prévia com `-WhatIf` e utilizam `-LiteralPath` para suportar colchetes `[]` e espaços.
- **`[FAIL: MUTACAO_SEM_DRYRUN]` Critério 02:** Execução direta de transferência em massa sem simulação prévia ou uso inseguro de `-Path` em caminhos com caracteres especiais.

- **`[PASS]` Critério 03 (Destino Seguro de Projetos Dev Sem Exclusão):** Projetos inativos em `C:\Users\melki\dev\` são movidos exclusivamente para quarentena/arquivo (`dev\_arquivo\`) sem `Remove-Item -Recurse -Force`.
- **`[FAIL: EXCLUSAO_DESTRUTIVA]` Critério 03:** Execução de exclusão definitiva sem confirmação expressa do usuário.

- **`[PASS]` Critério 04 (Verificação Defensiva de Locks de Processo):** Verifica se arquivos `.exe`/`.msi` ou pastas estão em uso por processos ativos antes de mover.
- **`[FAIL: LOCK_IGNORADO]` Critério 04:** Falha não tratada ao tentar mover arquivo aberto por processo em execução.
