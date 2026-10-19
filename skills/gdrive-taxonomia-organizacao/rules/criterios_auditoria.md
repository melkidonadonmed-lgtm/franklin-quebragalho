# Critérios Determinísticos de Auditoria — `gdrive-taxonomia-organizacao` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M4 (Taxonomia Google Drive `G:\Meu Drive`)**:

---

- **`[PASS]` Critério 01 (Aderência à Taxonomia Canônica Numerada Real):** Os arquivos são classificados estritamente nas pastas numeradas reais de `G:\Meu Drive\` (`01_Modelos_Rapidos`, `02_Protocolos_e_Medicamentos`, `03_Medicina_Faculdade`, `04_Workspace_e_Banco_de_Dados`, `07_Gemini_Gems`, `09_ui_web_kits`, `10_Pessoal`, `16_Documentos_comp_SUS`, `99_Arquivo_Historico`).
- **`[FAIL: PASTA_PARALELA_INVENTADA]` Critério 01:** Criação de pastas paralelas redundantes na raiz de `G:\Meu Drive\` ignorando a árvore oficial existente.
- **`[UNVERIFIED]` Critério 01:** Unidade `G:\Meu Drive\` não montada ou caminho inacessível.

- **`[PASS]` Critério 02 (Padronização de Datas ISO `YYYY-MM-DD`):** Arquivos renomeados adotam estritamente o prefixo/sufixo ISO `YYYY-MM-DD` com separadores padronizados.
- **`[FAIL: DATA_AMBIGUA]` Critério 02:** Uso de formatos ambíguos de data (`DD-MM-YY`, `MM/DD/YYYY`).

- **`[PASS]` Critério 03 (Higienização de Caracteres, `-LiteralPath` e Dry-Run):** Nomes higienizados não contêm caracteres ilegais, comandos PowerShell usam `-LiteralPath` (para lidar com colchetes `[01]Projetos`) e toda renomeação/movimentação em lote exibe simulação prévia (`-WhatIf`).
- **`[FAIL: PATH_SEM_ESCAPE_OU_SEM_DRYRUN]` Critério 03:** Uso de `-Path` sem escape em diretórios com colchetes ou mutação em lote sem simulação prévia.

- **`[PASS]` Critério 04 (Preservação de Extensão e Sigilo de `15_chaves_api`):** A extensão original do arquivo é mantida idêntica e a pasta `15_chaves_api` nunca é exposta ou copiada para repositórios.
- **`[FAIL: EXTENSAO_ALTERADA_OU_SEGREDO_EXPOSTO]` Critério 04:** Extensão corrompida durante renomeação ou leitura indevida de credenciais em `15_chaves_api`.
