---
name: design-interface-medica-minimalista
description: Define o padrão de UI/UX para aplicações médicas e SaaS de saúde. Deve ser ativada sempre que o usuário solicitar o desenvolvimento, análise ou refatoração do frontend de sistemas médicos, prontuários, receituários ou calculadoras clínicas.
version: "1.0.0"
id: "AST-2026-004"
categoria: "Design"
compatibilidade: ["ChatGPT", "Claude", "Gemini", "ADK"]
data_criacao: "2026-07-30"
tags: ["design", "ui", "ux", "tailwind", "saúde", "minimalista"]
---

# Skill: Design System Médico Executivo & Minimalista

## 🎯 Gatilhos de Ativação (Quando Usar)
- Criação ou alteração de telas para softwares médicos, prontuários ou calculadoras de dosagem.
- Solicitações de componentes de UI para o domínio de saúde e biologia.
- Pedidos de melhoria estética em interfaces web cirúrgicas, clínicas ou laboratoriais.

---

## 📥 Entradas Obrigatórias e Pré-requisitos
1. **Domínio ou Caso de Uso Clínico**: Ex.: prontuário eletrônico, calculadora de infusão, receituário ou laudo laboratorial.
2. **Componentes ou Telas Desejadas**: Formulários clínicos, visualizadores de exames, tabelas de posologia ou dashboards de leitos.
3. **Pilha de Tecnologias**: React/Tailwind, HTML/CSS puro, Next.js ou Vue.

---

## 🔄 Processamento e Fluxo de Design

### 1. Restrições Estritas de Elementos
- **Zero Emojis:** Proibido utilizar emojis na interface. Use apenas ícones vetoriais de linha (`Lucide Icons`, `stroke-width="1.5"`).
- **Proibido Sombras Fortes:** Não utilize `shadow-lg` ou `shadow-xl`. Utilize apenas bordas ultra-finas (`border border-slate-200/80`) com sombras ambientais de 1px (`shadow-[0_1px_2px_0_rgba(0,0,0,0.03)]`).
- **Proibido Cores Saturadas:** Não use azuis ou verdes puros (`#0000FF`, `#00FF00`). Utilize a paleta `Slate` combinada com tons atenuados de `Emerald`, `Amber` e `Rose`.

### 2. Especificação de Componentes (Tailwind CSS)

| Componente | Classes Tailwind Padrão | Comportamento / Regra |
| :--- | :--- | :--- |
| **Fundo da Página** | `bg-slate-50/50 min-h-screen text-slate-900 font-sans` | Base limpa e de baixo contraste |
| **Card / Container** | `bg-white border border-slate-200/80 rounded-lg p-5 shadow-sm` | Isolamento visual sutil |
| **Label / Rótulo** | `block text-[11px] uppercase tracking-wider font-semibold text-slate-500 mb-1.5` | Alta legibilidade em tamanho reduzido |
| **Input / Select** | `h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-900 focus:border-slate-900 focus:outline-none` | Campo preciso com estado de foco sóbrio |
| **Botão Primário** | `h-9 px-4 rounded-md bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium transition-all` | Ação principal discreta e sólida |
| **Botão Secundário**| `h-9 px-4 rounded-md border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium transition-all` | Ação de apoio ou navegação |
| **Badge de Status** | `inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium border` | Usado para status vacinal/clínico |

---

## 📤 Saídas e Entregáveis (Modelo de Saída)
Ao gerar código ou protótipos sob esta Skill, a entrega deve conter:
1. Componentes tipados (TypeScript / JSX) ou HTML com classes utilitárias completas.
2. Checklist de conformidade com o Design System:
   - [ ] Todos os rótulos de campos estão em caixa alta e fonte reduzida (`text-[11px] uppercase`)?
   - [ ] A proporção entre áreas de dados e áreas brancas está espaçada de forma equilibrada (`gap-4` a `gap-6`)?
   - [ ] A visualização do documento impresso/PDF simula com precisão um papel A4 oficial limpo?
   - [ ] NENHUM emoji foi inserido no código HTML ou JS?

---

## 🚫 Limites, Exceções e Quando NÃO Usar
- Não utilizar para interfaces de entretenimento, e-commerce casual ou dashboards saturados/gamificados.
- Não substitui a revisão médica formal de posologias e condutas terapêuticas.
