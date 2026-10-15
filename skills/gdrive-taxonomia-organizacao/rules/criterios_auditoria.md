# Critérios Determinísticos de Auditoria: gdrive-taxonomia-organizacao

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Aderência à Taxonomia Canônica Real da Máquina):** Os arquivos são classificados nas pastas numeradas reais de `G:\Meu Drive\` (`01_Modelos_Rapidos`, `02_Protocolos_e_Medicamentos`, `03_Medicina_Faculdade`, `04_Workspace_e_Banco_de_Dados`, `07_Gemini_Gems`, `09_ui_web_kits`, `10_Pessoal`, `16_Documentos_comp_SUS`, `99_Arquivo_Historico`).
- `[FAIL]` **Critério 01:** Criação de pastas paralelas redundantes na raiz de `G:\Meu Drive\` ignorando a árvore oficial existente.

- `[PASS]` **Critério 02 (Padronização de Datas ISO):** Arquivos renomeados adotam estritamente o formato `YYYY-MM-DD` com separadores consistentes.
- `[FAIL]` **Critério 02:** Uso de formatos ambíguos de data (`DD-MM-YY`, `MM/DD/YYYY`).

- `[PASS]` **Critério 03 (Higienização de Caracteres e Uso de `-LiteralPath`):** Nomes higienizados não contêm caracteres ilegais e comandos PowerShell usam `-LiteralPath` ao lidar com nomes contendo colchetes (`[01]Projetos`).
- `[FAIL]` **Critério 03:** Permissão de caracteres especiais ilegais ou uso de `-Path` sem escape em diretórios com colchetes.

- `[PASS]` **Critério 04 (Preservação de Extensão e Sigilo de `15_chaves_api`):** A extensão original do arquivo é mantida idêntica e a pasta `15_chaves_api` nunca é exposta ou copiada para repositórios.
- `[FAIL]` **Critério 04:** Extensão alterada durante renomeação ou leitura indevida de credenciais em `15_chaves_api`.
