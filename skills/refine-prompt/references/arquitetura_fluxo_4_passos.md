# Arquitetura em 4 Passos e Módulos — `refine-prompt`

Fluxo estrutural completo de processamento consumido por [`../SKILL.md`](../SKILL.md), complementando [`diretrizes_zero_trust_owasp.md`](diretrizes_zero_trust_owasp.md), [`taxonomia_epistemica.md`](taxonomia_epistemica.md), [`engenharia_fluidez_e_baixa_entropia.md`](engenharia_fluidez_e_baixa_entropia.md), [`contratos_io_modulos.md`](contratos_io_modulos.md) e [`prompt_sistema_master.md`](prompt_sistema_master.md).

## Fluxograma de Auditoria Epistêmica e Entropia

```text
[Entrada em <untrusted_user_input>]
                 │
                 ▼
[Passo 1: Higienização Zero-Trust & Veredito de Factibilidade (2026)]
                 │
     ┌───────────┴───────────┐
     ▼                       ▼
[Factível]          [Inviável / Obsoleta] ──► [Emite [VEREDITO] + Causa Raiz + Alternativa]
     │
     ▼
[Passo 2: Classificação Epistêmica ([FATO], [INFERÊNCIA], [LACUNA]) + Regime de Entropia]
     │
     ▼
[Passo 3: Aplicação do Módulo de Domínio (M1..M7) + Engenharia de Fluidez/Baixa Entropia]
     │
     ▼
[Passo 4: Portão Determinístico (rules/criterios_auditoria.md) & Entrega]
```

## Módulos de Saída (`contratos_io_modulos.md`)

- **Módulo 1 (Resposta Direta):** `1. SÍESE EXECUTIVA E SOLUÇÃO RESOLVIDA` + `2. NOTA METODOLÓGICA E MATRIZ DE DECISÃO`.
- **Módulo 2 (Artefato Plug-and-Play):** `1. ESCOPO E DIAGNÓSTICO` + `2. ARTEFATO INTEGRAL E CONTÍNUO` (bloco único com variáveis `[NOME_DA_VARIAVEL]`, sem fragmentação) + `3. GUIA DE ACIONAMENTO`.
- **Módulo 3 (Entrevista Socrática):** `1. DIAGNÓSTICO DE AMBIGUIDADE E RISCOS` + `2. PERGUNTAS-CHAVE CIRÚRGICAS (MÁXIMO DE 3 COM OPÇÕES A/B)` + `3. ESBOÇO PRELIMINAR CONDICIONADO`.

## Regimes de Entropia

- **`COGNITIVE_FLUID`:** Interação humana aberta (*Why-First*, prosa adaptativa, zero templates mecânicos forçados).
- **`LOW_ENTROPY_CONTRACT`:** Rotina operacional repetitiva / borda de máquina (contrato estrito, tokens `[NÃO INFORMADO: dado]` / `[PENDENTE: dado]` e campo preliminar `"_pre_flight_check"` gerado antes da saída final em JSON).
