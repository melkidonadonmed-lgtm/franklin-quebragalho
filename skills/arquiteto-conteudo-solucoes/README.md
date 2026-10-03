# Arquiteto de Conteúdo e Soluções 🏛️

> **Versão:** 2.2.0  
> **Status:** ✅ Validada  
> **Compatibilidade:** Google Antigravity, MCP, Padrão Agent Skills 2026

O **Arquiteto de Conteúdo e Soluções** é uma skill autônoma de alta performance projetada para traduzir demandas (curtas, complexas ou ambíguas) em artefatos técnicos de alta fidelidade: engenharia de prompts, códigos tipados com ReAct, especificações modulares de skills e roadmaps estruturados em fases.

---

## 🧭 Os 4 Modos Operacionais (Taxonomia Rigorosa)

Toda resposta do Arquiteto declara obrigatoriamente na **primeira linha** o modo ativo:

| Modo | Nome | Gatilho | Regra de Execução |
| :--- | :--- | :--- | :--- |
| **Modo A** | **Execução Direta** | Pedidos claros, objetivos ou imperativos ("crie", "gere", "escreva"). | **Zero perguntas.** Entrega a solução integral imediatamente. |
| **Modo B** | **Refinamento Colaborativo** | Pedidos vagos, com lacunas críticas ("me ajude a pensar", "o que acha?"). | **Máximo de 2 perguntas** estratégicas e proposta de versão refinada. |
| **Modo C** | **Planejamento Estruturado** | Demandas complexas multietapas ("crie plano", "monte roadmap"). | Fases numeradas, dependências, esforço e **Fase 0 de Validação obrigatória**. |
| **Modo D** | **Auto-Reflexão Pré-Entrega** | Ativado ao final de qualquer entrega técnica. | Seção `# AUTO-REFLEXAO DO AGENTE` com auditoria e gestão de context rot. |

---

## 📁 Estrutura de Arquivos da Skill

Seguindo o princípio de **Divulgação Progressiva**, a skill é modularizada para evitar diluição de atenção (*Lost in the Middle*):

```text
arquiteto-conteudo-solucoes/
├── SKILL.md                          # Contrato nuclear (taxonomia, gatilhos e fluxo decisório)
├── README.md                         # Guia de arquitetura, uso e governança (este arquivo)
├── references/                       # Conhecimento factual estático lido sob demanda
│   ├── diretrizes_especializadas.md  # Frameworks setoriais (CLAREZA, 8 Pilares em inglês, clínica, ReAct)
│   └── checklist_validacao.md        # Checklist silencioso pré-renderização
├── rules/                            # Regras de corte estritas e critérios determinísticos
│   └── criterios_auditoria.md        # Retornos booleanos padronizados: [PASS], [FAIL], [UNVERIFIED]
└── evals/                            # Casos de teste empíricos (zero simulação no chat)
    └── evals.json                    # Casos de teste com entradas reais e asserções esperadas
```

---

## 🛡️ Governança Anti-Alucinação

Para assegurar conformidade técnica rigorosa, a skill opera sob os seguintes invariantes:
- **Proibição de Dados Sintéticos**: Nunca inventar bibliotecas, APIs, métodos inexistentes ou notas percentuais subjetivas ("100% seguro").
- **Validações Falsificáveis**: Toda checagem técnica deve basear-se em evidência direta e retornar:
  - `[PASS]`: Requisito comprovado contra documentação ou entrada.
  - `[FAIL]`: Requisito descumprido com motivo demonstrado.
  - `[UNVERIFIED]`: Não verificável por omissão de insumos.
- **Prompts Visuais**: Prompts para Midjourney/DALL-E/Veo/Sora são gerados **estritamente em inglês** aplicando os 8 Pilares Visuais (Subject, Environment, Lighting, Composition, Style, Palette, Flags, Negative Constraints).
- **Código e Agentes**: Todo código deve conter type hints estritos, tratamento defensivo de exceções e limites de iteração (`max_steps`).

---

## 🧪 Casos de Teste (`evals/evals.json`)

| ID do Teste | Cenário Avaliado | Asserção Principal |
| :--- | :--- | :--- |
| `TC-01-MODO-A-EXECUCAO-DIRETA` | Verbo imperativo e direto | Declara Modo A, 0 perguntas, type hints incluídos. |
| `TC-02-MODO-B-REFINAMENTO-ESTRUTURADO` | Pedido ambíguo / vago | Declara Modo B, <= 2 perguntas, proposta preliminar. |
| `TC-03-MODO-C-FASE-ZERO` | Demanda de roadmap / plano | Declara Modo C, presença obrigatória de Fase 0. |
| `TC-04-ANTI-ALUCINACAO-STATUS-DETERMINISTICO` | Solicitação de auditoria com nota percentual | Rejeita nota simulada e usa `[PASS]`/`[FAIL]`/`[UNVERIFIED]`. |

---

## 🔗 Links Úteis no Workspace

- [SKILL.md Principal](file:///c:/Users/melki/dev/franklin-quebragalho/.agents/skills/arquiteto-conteudo-solucoes/SKILL.md)
- [Critérios de Auditoria](file:///c:/Users/melki/dev/franklin-quebragalho/.agents/skills/arquiteto-conteudo-solucoes/rules/criterios_auditoria.md)
- [Diretrizes Especializadas](file:///c:/Users/melki/dev/franklin-quebragalho/.agents/skills/arquiteto-conteudo-solucoes/references/diretrizes_especializadas.md)
- [Manifesto de Skills](file:///c:/Users/melki/dev/franklin-quebragalho/MY_SKILLS.md)
