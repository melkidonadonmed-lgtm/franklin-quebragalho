---
name: evoluir-skills
description: >-
  Use esta skill sempre que o usuário quiser criar uma nova skill, testar uma skill existente, registrar histórico de versões ou evoluir o catálogo de habilidades do Franklin Quebra-Galho com critérios anti-alucinação e validações determinísticas.
license: MIT
metadata:
  version: "1.1.0"
  author: "SkillCraft & Melki"
  category: "Engenharia e Governança de Skills"
  updated_at: "2026-10-04"
  tags:
    - "skills"
    - "evals"
    - "ciclo-de-vida"
    - "governanca"
version: 1.1.0
updated_at: 2026-10-04
author: SkillCraft & Melki
category: Engenharia e Governança de Skills
---

# Evolução e Engenharia de Skills 🚀

Metodologia oficial para conceber, desenvolver, testar, versionar e documentar skills personalizadas no Google Antigravity e no ecossistema Franklin Quebra-Galho.

---

## 🎯 Quando Usar (Gatilhos de Ativação)
- Criação de uma nova automação ou procedimento especializado para o Franklin.
- Teste prático de uma skill recém-criada para verificar sua confiabilidade e ativação.
- Atualização de versão (SemVer) e registro de changelog no [MY_SKILLS.md](file:///c:/Users/melki/dev/franklin-quebragalho/MY_SKILLS.md).
- Refatoração de descrições ou instruções de skills existentes para melhorar divulgação progressiva e mitigar alucinações.

---

## 🚫 Limites, Exceções e Quando NÃO Usar
- Não usar para desenvolvimento de software genérico que não constitua uma habilidade reutilizável do agente.
- Não usar para mutações em lote sem testes empíricos em `evals/`.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Nome da Skill**: slug em minúsculas separado por hífens.
2. **Descrição do Propósito**: texto em 3ª pessoa explicando o que faz e quando ativar.
3. **Escopo de Operação**: definição de fluxos, ferramentas e restrições.

---

## 🔄 Ciclo de Vida da Skill

```text
💡 Ideia ➔ 📝 Rascunho ➔ 🧪 Em Teste ➔ ✅ Validada ➔ 🚀 Produção
```

1. **💡 Ideia**: O usuário ou o agente identifica uma tarefa repetitiva, regra de negócio ou fluxo de trabalho útil.
2. **📝 Rascunho**: Criação da pasta `.agents/skills/<nome>/` e redação inicial do `SKILL.md` com YAML frontmatter.
3. **🧪 Em Teste**: Execução em cenários simulados ou testes reais usando asserções estruturadas (`evals/evals.json`).
4. **✅ Validada**: A skill respondeu adequadamente, sem alucinações, com critérios determinísticos aprovados.
5. **🚀 Produção**: Adicionada às rotinas fixas e catalogada no manifesto [MY_SKILLS.md](file:///c:/Users/melki/dev/franklin-quebragalho/MY_SKILLS.md).

---

## 📋 Princípios de Engenharia de Skills (Padrão 2026)

### 1. Divulgação Progressiva (Progressive Disclosure)
- Mantenha o `SKILL.md` nuclear enxuto (foco no fluxo decisório, gatilhos e formato de saída).
- Mova tabelas densas, regras setoriais extensas e manuais de consulta para a pasta `references/`.

### 2. Rejeição a Validações Vazias e Auditorias Inventadas
- **Proibição Estrita**: Nunca utilize instruções vagas como "valide se os dados estão corretos" ou "gere uma auditoria confirmando 100% de segurança".
- **Critérios Falsificáveis**: As validações devem residir em `rules/criterios_auditoria.md` baseadas em lógica booleana, checagens de campos obrigatórios ou schemas delimitados.
- **Status Determinísticos**: Obrigatoriamente utilizar apenas:
  - `[PASS]` (Aprovado com evidência documental)
  - `[FAIL]` (Reprovado com causa demonstrada)
  - `[UNVERIFIED]` (Não verificável por falta de insumo)

### 3. Avaliação Empírica Real (`evals/`)
- Testes não devem ser simulações ficcionais no chat.
- Defina casos de teste com entradas reais e comportamento esperado no arquivo `evals/evals.json`.

---

## 📁 Estrutura Canônica de Diretórios

```text
.agents/skills/<nome-da-skill>/
├── SKILL.md            # Obrigatório: Contrato nuclear, frontmatter YAML, fluxo e saídas
├── references/         # Opcional: Conhecimento factual imutável (tabelas, manuais, schemas)
├── rules/              # Opcional: Critérios de corte e regras de auditoria determinísticas
├── scripts/            # Opcional: Scripts PowerShell / Node para tarefas pesadas ou locais
└── evals/              # Opcional: Casos de teste reais com asserções (evals.json)
```

---

## 🛠️ Checklist de Criação e Atualização

### 1. Nomenclatura e Frontmatter
- Nome em minúsculas com hífens: ex. `organizar-gdrive`, `validador-clinico`.
- A descrição **DEVE** estar em 3ª pessoa ("Use esta skill sempre que o usuário...").
- A descrição deve conter palavras-chave claras que o modelo usará para decidir ativá-la.

### 2. Espelhamento Obrigatório
- Todas as skills em `.agents/skills/<nome>/` devem ser espelhadas em `skills/<nome>/` para manter consistência entre o agente nativo e a raiz do projeto.

### 3. Versionamento Semântico e Changelog
Sempre que alterar uma skill, atualize [MY_SKILLS.md](file:///c:/Users/melki/dev/franklin-quebragalho/MY_SKILLS.md):
- Incremente a versão (ex.: `v1.0.0` ➔ `v1.1.0` para novas capacidades, `v1.0.1` para correções).
- Atualize a coluna de Status (`💡 Ideia`, `🧪 Em Teste`, `✅ Validada`, `🚀 Produção`).
- Registre o que foi alterado na seção de Histórico de Versões.

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
Toda evolução de skill deve entregar:
1. Arquivo `SKILL.md` atualizado com YAML frontmatter válido.
2. Arquivos `rules/criterios_auditoria.md` e `evals/evals.json` implementados.
3. Pasta espelhada de forma paritária em `skills/<nome-da-skill>/`.
4. Registro de versão e changelog atualizados em `MY_SKILLS.md`.
5. Validação via `scripts/validate_skills.py` com código de retorno 0 (`[PASS]`).
