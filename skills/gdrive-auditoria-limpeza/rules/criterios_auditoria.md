# Critérios Determinísticos de Auditoria — `gdrive-auditoria-limpeza` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M4 (Google Drive `G:\Meu Drive`)**:

---

- **`[PASS]` Critério 01 (Prevenção de Perda de Dados e Quarentena):** Nenhuma operação de exclusão definitiva (`Remove-Item -Force`) é emitida; todo descarte é movido para pasta de quarentena datada (`_Quarentena_Descarte\YYYY-MM-DD\`).
- **`[FAIL: EXCLUSAO_DEFINITIVA_DRIVE]` Critério 01:** Comando de remoção irreversível detectado sem quarentena preventiva.
- **`[UNVERIFIED]` Critério 01:** Unidade `G:\Meu Drive\` desmontada ou inacessível no momento da verificação.

- **`[PASS]` Critério 02 (Simulação Dry-Run Obrigatória e `-LiteralPath`):** Toda movimentação em lote apresenta tabela prévia de impacto (`-WhatIf`) e utiliza `-LiteralPath` no PowerShell.
- **`[FAIL: LOTE_SEM_SIMULACAO]` Critério 02:** Movimentação em massa executada sem apresentar a lista prévia dos itens afetados.

- **`[PASS]` Critério 03 (Falsificabilidade de Duplicatas por SHA-256):** Confirmação de duplicatas com validação rigorosa de hash `Get-FileHash -Algorithm SHA256` (mais correspondência de tamanho em bytes).
- **`[FAIL: DUPLICATA_POR_NOME_VAGO]` Critério 03:** Classificação de arquivos como duplicados baseada apenas em semelhança superficial de nome.

- **`[PASS]` Critério 04 (Preservação de Metadados de Sincronização e Sigilo):** Arquivos internos do Google Drive (`desktop.ini`, `.tmp.drivedownload`, `.gdoc`, `.gsheet`) e a pasta `15_chaves_api` são preservados e nunca corrompidos ou expostos.
- **`[FAIL: ARQUIVO_SISTEMA_AFETADO]` Critério 04:** Tentativa de mover arquivos internos de sincronização ou expor `15_chaves_api`.
