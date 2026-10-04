---
name: redator-tecnico-markdown
description: >-
  Redige relatorios executivos, notas tecnicas, atas de decisao e roadmaps estruturados em Markdown (.md) de alta fidelidade visual, com frontmatter YAML, caixas de alerta GitHub, tabelas ricas e compatibilidade plena com Obsidian.
version: 1.0.0
updated_at: 2026-10-04
author: DocMaker & Melki
category: Documentacao Tecnica e Redacao Estruturada
---

# 1. NOME DA SKILL
`redator-tecnico-markdown` (Redação Técnica Estruturada, Notas Executivas e Documentação no Padrão Obsidian/GitHub).

---

## 2. GATILHOS DE ATIVAÇÃO (QUANDO USAR)

Ative e execute esta skill sempre que:
- O usuário solicitar: "redija um relatório técnico", "crie uma nota para o Obsidian sobre este tema", "elabore uma ata de decisão de arquitetura (ADR)", "escreva a documentação do projeto em Markdown", "estruture um roadmap executivo em .md".
- For necessário transformar notas brutas, resumos de reuniões ou rascunhos conceituais em documentos profissionais prontos para arquivo ou publicação.
- Como etapa prévia antes da conversão para PDF, para garantir que o Markdown possua formatação semântica perfeita.

### Quando NÃO Usar
- Para compilar ou converter Markdown para arquivos PDF (utilize `conversor-html-pdf`).
- Para desenhar especificamente diagramas de fluxo ou árvores de diretórios (utilize `organizador-fluxo-arvore-arquivos`).
- Para criar skills do Antigravity (utilize `evoluir-skills`).

---

## 3. ENTRADAS ESPERADAS E PRÉ-REQUISITOS

- `topic_or_draft` (obrigatório): Tema, rascunho de texto, atas ou código a ser documentado.
- `document_type` (opcional): `relatorio_executivo`, `nota_tecnica`, `adr_decisao`, `roadmap`, `guia_instalacao`. Padrão: `nota_tecnica`.
- `output_path` (opcional): Destino do arquivo `.md` resultante (padrão: `C:\Users\melki\Documents\Obsidian Vault\00_Inbox\` ou diretório do projeto).
- `frontmatter_metadata` (opcional): Dicionário de metadados adicionais (`tags`, `aliases`, `author`).

---

## 4. DIRETRIZES DE FORMATAÇÃO E BLINDAGEM DE LAYOUT

Todo documento técnico em Markdown gerado por esta skill segue os padrões da governança global:

### 4.1. Lei da Linha em Branco (Blank Line Law)
- Inserção obrigatória de linha em branco antes e depois de títulos (`#` a `######`), listas ordenadas e não-ordenadas, tabelas completas, citações em bloco (`>`) e cercas de código (três crases).

### 4.2. Cabeçalho Frontmatter YAML Canônico
Toda nota deve iniciar com metadados estruturados:
```yaml
---
title: "[TÍTULO_DO_DOCUMENTO]"
date: YYYY-MM-DD
author: "DocMaker & Melki"
tags:
  - categoria/subcategoria
status: "concluido"
aliases:
  - "[Sinônimo_Busca]"
---
```

### 4.3. Caixas de Alerta Estilizadas (GitHub Alerts)
Utilizar exclusivamente os marcadores canônicos suportados no Obsidian e GitHub:
- `> [!NOTE]` Informações e contexto de apoio.
- `> [!IMPORTANT]` Requisitos e passos fundamentais.
- `> [!TIP]` Boas práticas e ganhos de produtividade.
- `> [!WARNING]` Riscos conhecidos e limitações técnicas.
- `> [!CAUTION]` Operações de alto risco e prevenção de perda.

### 4.4. Tabelas Ricas com Alinhamento Explícito
- Cabeçalhos de tabela com alinhamento explícito (`| :--- | :---: | :--- |`).
- Proibição de quebras brutas de linha dentro de células; utilizar `<br>` se necessário.
- Escape de barras verticais (`\|`) quando ocorrem dentro do texto das células.

---

## 5. PROCESSO PASSO A PASSO (EXECUÇÃO DE REDAÇÃO)

### Passo 1: Triagem do Objetivo e Estrutura do Documento
Identificar o propósito e delimitar a hierarquia de seções:
- Visão Geral / Sumário Executivo.
- Diagnóstico Técnico / Motivação.
- Especificação Detalhada com Tabelas e Código.
- Recomendações e Próximos Passos.

### Passo 2: Redação com Validação de Sintaxe
Construir o documento aplicando a Lei da Linha em Branco e escape estrito de símbolos angulares soltos (`<`, `>`).

### Passo 3: Revisão de Metadados e Gravação
Gravar o arquivo `.md` no local designado e verificar a integridade da codificação UTF-8:
```powershell
Set-Content -Path $outputPath -Value $markdownContent -Encoding utf8
```

---

## 6. SAÍDAS E ENTREGÁVEIS (MODELO DE SAÍDA)

A resposta final da skill entrega:
1. **Documento Markdown Formatado:**
   - Arquivo `.md` gravado no disco com metadados YAML e formatação completa.
2. **Resumo das Seções Redigidas:**
   - Visão sintética dos tópicos abordados e tags atribuídas.
3. **Link Clicável Local:**
   - Link no padrão `file:///` apontando diretamente para o arquivo gerado.

---

## 7. EXCEÇÕES E LIMITES (QUANDO NÃO USAR)

- NUNCA embutir scripts maliciosos ou tags `<script>` não filtradas no Markdown.
- NUNCA inventar dados fictícios em atas técnicas; rotular incertezas como `[UNVERIFIED]`.
- Esta skill gera **apenas** o arquivo Markdown; para exportação em PDF, delegue para `conversor-html-pdf`.
