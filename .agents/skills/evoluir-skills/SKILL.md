---
name: evoluir-skills
description: >-
  Use esta skill sempre que o usuário quiser criar uma nova skill, testar uma skill existente, registrar histórico de versões ou evoluir o catálogo de habilidades do Franklin Quebra-Galho.
---

# Evolução e Engenharia de Skills 🚀

Metodologia oficial para conceber, desenvolver, testar, versionar e documentar skills personalizadas no Google Antigravity.

---

## 🎯 Quando Usar
- Criação de uma nova automação ou procedimento para o Franklin.
- Teste prático de uma skill recém-criada para verificar sua confiabilidade.
- Atualização de versão (SemVer) e registro de changelog no [MY_SKILLS.md](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/MY_SKILLS.md).
- Refatoração de descrições ou instruções de skills existentes para melhorar ativação.

---

## 🔄 Ciclo de Vida da Skill

```text
💡 Ideia ➔ 📝 Rascunho ➔ 🧪 Em Teste ➔ ✅ Validada ➔ 🚀 Produção
```

1. **💡 Ideia**: O usuário ou o agente identifica uma tarefa repetitiva ou fluxo de trabalho útil.
2. **📝 Rascunho**: Criação da pasta `.agents/skills/<nome>/` e redação inicial do `SKILL.md`.
3. **🧪 Em Teste**: Execução em cenários simulados ou tarefas reais no dia a dia.
4. **✅ Validada**: A skill respondeu adequadamente, sem falhas e com boa experiência de uso.
5. **🚀 Produção**: Adicionada às rotinas fixas e catalogada no `MY_SKILLS.md`.

---

## 📋 Checklist de Criação de Nova Skill

### 1. Nomenclatura e Frontmatter
- Nome em minúsculas com hífens: ex. `organizar-gdrive`, `backup-obsidian`.
- A descrição **DEVE** estar em 3ª pessoa ("Use esta skill sempre que o usuário...").
- A descrição deve conter palavras-chave claras que o modelo usará para decidir ativá-la (*progressive disclosure*).

### 2. Estrutura de Arquivos
```text
.agents/skills/<nome-da-skill>/
├── SKILL.md            # Obrigatório: Instruções passo a passo
├── scripts/            # Opcional: Scripts PowerShell / Node para tarefas pesadas
└── references/         # Opcional: Documentações longas consultadas sob demanda
```

### 3. Protocolo de Testes
Para homologar a skill:
1. Formule uma pergunta de teste típica de usuário.
2. Verifique se o agente ativa a skill correta.
3. Execute os comandos em modo seguro (dry-run).
4. Verifique o resultado gerado.

### 4. Versionamento e Changelog
Sempre que alterar uma skill, atualize [MY_SKILLS.md](file:///c:/Users/melki/Documents/antigravity/wonderful-franklin/MY_SKILLS.md):
- Incremente a versão (ex.: `v1.0.0` ➔ `v1.1.0` para melhorias funcionais, `v1.0.1` para correções).
- Atualize a coluna de Status.
- Registre o que foi alterado na seção de Histórico de Versões.
