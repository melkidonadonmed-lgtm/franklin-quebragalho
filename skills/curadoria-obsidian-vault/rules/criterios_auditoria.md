# Critérios Determinísticos de Auditoria — `curadoria-obsidian-vault` (`v1.2.0`)

Regras falsificáveis com marcadores determinísticos (`[PASS]`, `[FAIL]`, `[UNVERIFIED]`) sob o Módulo **M5 (Obsidian Vault `C:\Users\melki\dev\notes` & MemPalace)**:

---

- **`[PASS]` Critério 01 (Preservação Integral de Notas Não-Vazias):** Nenhuma nota com conteúdo autoral é apagada ou truncada; qualquer arquivamento move para `Arquivo\` com simulação prévia.
- **`[FAIL: PERDA_DE_CONTEUDO_VAULT]` Critério 01:** Remoção ou truncamento de nota contendo texto, decisões ou links legítimos.
- **`[UNVERIFIED]` Critério 01:** Caminho do cofre `C:\Users\melki\dev\notes` inacessível.

- **`[PASS]` Critério 02 (Proteção Estrita da Pasta `.obsidian/`):** O diretório `.obsidian/` é categoricamente excluído de varreduras destrutivas ou mutações automáticas.
- **`[FAIL: CORRUPCAO_CONFIG_OBSIDIAN]` Critério 02:** Modificação ou remoção não solicitada de arquivos internos de configuração em `.obsidian/`.

- **`[PASS]` Critério 03 (Falsificabilidade de Anexos Órfãos via `vault_hygiene_scanner.py`):** Comprovação determinística de que o anexo não possui nenhuma referência `![[...]]` ou `![](...)` em todo o vault antes de propor realocação para `Arquivo\_anexos_orfaos`.
- **`[FAIL: FALSO_ORFAO]` Critério 03:** Classificação de anexo referenciado como órfão sem varredura completa de links.

- **`[PASS]` Critério 04 (Integridade de Frontmatter YAML, Paridade de Projetos e MemPalace):** Validação de YAML válido (`tags`, `date` ISO), paridade com `dev\tools\check-vault-projects.ps1` e sincronização final via `mempalace mine "C:\Users\melki\dev\notes"`.
- **`[FAIL: YAML_INVALIDO_OU_DESINCRONIZADO]` Critério 04:** Injeção de frontmatter malformado ou omissão de sincronização com o MemPalace após curadoria.
