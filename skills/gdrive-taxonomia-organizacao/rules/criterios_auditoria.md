# Critérios Determinísticos de Auditoria: gdrive-taxonomia-organizacao

Regras falsificáveis com marcadores booleanos determinísticos:

- `[PASS]` **Critério 01 (Aderência à Taxonomia Canônica):** Pastas de primeiro nível seguem o padrão numerado oficial (`01_Projetos`, `02_Documentos_Pessoais`, etc.).
- `[FAIL]` **Critério 01:** Criação de pastas arbitrárias na raiz fora da convenção numerada.

- `[PASS]` **Critério 02 (Padronização de Datas ISO):** Arquivos renomeados adotam estritamente o formato `YYYY-MM-DD` com separadores consistentes.
- `[FAIL]` **Critério 02:** Uso de formatos ambíguos de data (`DD-MM-YY`, `MM/DD/YYYY`).

- `[PASS]` **Critério 03 (Higienização de Caracteres Especiais):** Nomes higienizados não contêm caracteres ilegais para sincronização multiplataforma (`#`, `%`, `*`, `?`, etc.).
- `[FAIL]` **Critério 03:** Permissão de caracteres especiais em nomes de novos arquivos ou pastas organizadas.

- `[PASS]` **Critério 04 (Preservação de Extensão):** A extensão original do arquivo é mantida idêntica sem truncamento.
- `[FAIL]` **Critério 04:** Extensão corrompida ou alterada durante o processo de renomeação.
