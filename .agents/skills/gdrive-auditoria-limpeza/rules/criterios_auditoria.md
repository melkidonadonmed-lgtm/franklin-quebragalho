# Critérios Determinísticos de Auditoria: gdrive-auditoria-limpeza

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Prevenção de Perda de Dados):** Nenhuma operação de exclusão definitiva (`Remove-Item -Force`) é emitida; todo descarte é redirecionado para pasta de quarentena.
- `[FAIL]` **Critério 01:** Comando de remoção irreversível detectado sem quarentena preventiva.

- `[PASS]` **Critério 02 (Simulação Obrigatória):** Toda movimentação em lote apresenta simulação prévia (Dry-Run / `-WhatIf`) antes de tocar no disco.
- `[FAIL]` **Critério 02:** Movimentação em massa executada sem apresentar a lista prévia dos itens afetados.

- `[PASS]` **Critério 03 (Falsificabilidade de Duplicatas):** Confirmação de duplicatas com validação rigorosa de hash SHA-256 ou correspondência estrita de tamanho + nome.
- `[FAIL]` **Critério 03:** Classificação de arquivos como duplicados baseada apenas em semelhança vaga de nome de arquivo.

- `[PASS]` **Critério 04 (Preservação de Sistema):** Arquivos especiais do Google Drive (`desktop.ini`, `.tmp.drivedownload`) são ignorados e preservados.
- `[FAIL]` **Critério 04:** Tentativa de mover arquivos internos do cliente de sincronização do Google Drive.
