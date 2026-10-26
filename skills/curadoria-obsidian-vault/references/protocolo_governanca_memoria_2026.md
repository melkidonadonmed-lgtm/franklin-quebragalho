# Protocolo de Engenharia de Contexto, Auditoria e Governança de Memória (2026)

> **Escopo:** Referência canônica Tier 3 para a skill `curadoria-obsidian-vault` e para o ecossistema simbiótico `Obsidian Vault` (`C:\Users\melki\dev\notes`) + `MemPalace` (`wing: notes`) + `Knowledge Graph SQLite`.

---

## 1. Dinâmica da Atenção e Prevenção da Dispersão de Tokens

Modelos baseados em transformers computam o mecanismo de atenção ponderando chaves e consultas via:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Quando memórias obsoletas, prolixas ou contraditórias permanecem ativas na sala `memoria` (`1.40x`) ou `projetos` (`1.35x`), o somatório do denominador do $\text{softmax}$ acumula posições espúrias (**dispersão atencional**), reduzindo a probabilidade destinada às regras do sistema e parâmetros da tarefa atual.

---

## 2. Taxonomia e Segregação Estrita em 4 Camadas Operacionais

1. **Memória de Trabalho (*Working Memory*)**:
   - Estado volátil da sessão ativa, objetivos imediatos e variáveis em execução (`temp:` invocation-scoped state).
   - Ruído conversacional transitório nunca deve ser persistido no cofre.
2. **Memória Semântica (*Semantic Memory*)**:
   - Fatos duradouros, preferências estáveis e topologia atual: `Memória/Ambiente Dev (PC atual).md`, `Memória/Preferências de Trabalho com Agentes.md` e `Projetos/Repositórios na Máquina.md`.
   - Atualizada **in-place** sempre que uma versão de runtime, contagem de repositórios/skills ou regra estrutural mudar.
3. **Memória Episódica (*Episodic Memory*)**:
   - Marcos cronológicos e histórico de decisões: `Memória/Decisões.md`, `Diário/AAAA-MM-DD.md` e gavetas `hall_diary` no MemPalace.
   - **Teto de Particionamento (`< 25 KB`)**: Sempre que `Memória/Decisões.md` ultrapassar `25 KB`, as entradas anteriores às últimas decisões vigentes devem ser movidas para `Arquivo/Decisões - Histórico Vol. N.md` (`type: arquivo`, `status: arquivado`).
4. **Memória Procedural (*Procedural Memory*)**:
   - Rotinas determinísticas, contratos `AGENTS.md`, `SKILL.md` e scripts validados (`vault_palace_search.py`, `vault_kg_hydrator.py`, `vault_hygiene_scanner.py`, `sync-dev-workspace.ps1`).

---

## 3. Higienização Temporal e Resolução de Conflitos (*Temporal Invalidation*)

- **Metadados Obrigatórios**: Toda nota em `Memória/` e `Projetos/` deve conter YAML frontmatter com `title`, `date: YYYY-MM-DD`, `status: ativo | arquivado | desatualizado` e `tags`.
- **Invalidação Suave (*Soft Delete*)**:
  - Notas superadas recebem `type: historico` ou `type: arquivo` e `status: desatualizado` ou `status: arquivado`.
  - O motor JIT [`vault_palace_search.py`](../scripts/vault_palace_search.py) rebaixa automaticamente qualquer nota com `type in ("historico", "arquivo")` ou `status in ("desatualizado", "obsoleto", "arquivado")` para a sala `"arquivo"` (multiplicador `0.60x` em vez de `1.35x`–`1.40x`).
- **Higiene do Grafo SQLite ([`vault_kg_hydrator.py`](../scripts/vault_kg_hydrator.py))**:
  - Ignorar `[[Wikilinks]]` dentro de blocos de código/crases e placeholders genéricos (`wikilinks`, `nome da nota`, `projeto`).
  - Limpar triplas órfãs (`DELETE FROM triples; DELETE FROM entities;`) antes de reidratar os 4 espelhos `knowledge_graph.sqlite3`.
- **Sincronização Sem Lock SQLite no Windows**:
  - Quando `mempalace-mcp.exe` estiver ativo na sessão, utilize as ferramentas MCP `mempalace_mine(source="C:\\Users\\melki\\dev\\notes", wing="notes")`, `mempalace_sync(apply=true, project_dir="C:\\Users\\melki\\dev\\notes", wing="notes")` e `mempalace_delete_drawer` em vez de invocar `mempalace mine` via subprocesso concorrente.

---

## 4. Esquema JSON Padronizado de Saída da Auditoria de Memória

Quando solicitado um laudo estruturado de auditoria e governança de memória, produza a saída seguindo rigorosamente o contrato abaixo:

```json
{
  "analise_geral": {
    "total_entradas_analisadas": 0,
    "entradas_ativas_consolidadas": 0,
    "entradas_invalidadas_ou_purgadas": 0,
    "tokens_economizados_estimados": 0
  },
  "banco_otimizado": [
    {
      "id": "MEM-001",
      "categoria": "semantica | episodica | procedural | trabalho",
      "fato_consolidado": "Declaração atômica, precisa e concisa do fato.",
      "escopo": "usuario | projeto | tarefa_especifica",
      "status": "ativo | obsoleto | purgado",
      "data_criacao": "YYYY-MM-DDTHH:MM:SSZ",
      "data_atualizacao": "YYYY-MM-DDTHH:MM:SSZ",
      "confianca": 0.95,
      "gatilhos_de_ativacao": ["tag1", "termo_chave", "condicao_de_tarefa"],
      "motivo_auditoria": "Resumo da ação realizada (consolidação, invalidação temporal ou expurgo)."
    }
  ],
  "diretrizes_para_o_orquestrador_de_recuperacao": {
    "limite_maximo_tokens_memoria": 800,
    "score_minimo_relevancia": 0.75,
    "regras_de_expurgo": "Critérios para evitar recuperação desnecessária na sessão ativa."
  }
}
```
