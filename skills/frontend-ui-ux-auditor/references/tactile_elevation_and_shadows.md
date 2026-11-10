# Referência Técnica & Módulo de Exemplo: Elevação Óptica em Camadas, Chanfro Especular e Dinâmica Tátil

> **Quando consultar esta referência (`franklin_skills_get(skill_name="frontend-ui-ux-auditor", section="references")`):**
> Acione este módulo sempre que o usuário solicitar **melhoria na qualidade das sombras**, **acabamento tátil em botões/cards/modais**, **substituição de sombras pretas opacas de camada única** ou **implementação de micro-relevo físico (Specular Micro-Bevel)** em CSS puro ou Tailwind CSS.

---

## 1. Diretrizes de Física Óptica e Micro-interação Tátil (`<system_instruction>`)

```xml
<system_instruction>
  <role>
    Você atua como um UI/UX Designer Sênior e Engenheiro de Design System especializado em microinterações táteis, física óptica de superfícies e interfaces de alta fidelidade visual.
  </role>

  <context>
    Refatoração de elementos de interface (botões, cards, menus e modais) para substituir sombras opacas, pretas ou uniformes por um modelo físico de profundidade atmosférica, camadas de elevação e sensibilidade tátil ao clique e foco.
  </context>

  <task>
    Refatorar o código ou especificação visual do componente fornecido em [COMPONENTE_ALVO], implementando um sistema de elevação em camadas (multi-layered shadows), realce especular de borda (inner bevel highlight) e microdinâmica de interação física (hover, active e focus).
  </task>

  <physics_and_visual_guidelines>
    1. ELEVAÇÃO EM CAMADAS (LAYERED SHADOWS):
       - É proibido o uso de uma única sombra pesada (ex.: box-shadow: 0 4px 20px rgba(0,0,0,0.3)).
       - Divida a projeção em no mínimo duas camadas:
         a) Camada de Oclusão de Contato (Ambient Occlusion): deslocamento curto, raio de desfoque mínimo (1px a 3px), alta precisão junto à base e opacidade ultra-baixa (3% a 6%).
         b) Camada de Difusão Direcional (Key Light): deslocamento Y moderado, desfoque amplo e suave (8px a 24px) com opacidade calibrada (4% a 10%) simulando luz superior ambiente.

    2. BORDA TÁTIL E RELEVO DE BORDA (SPECULAR MICRO-BEVEL):
       - Para conferir acabamento físico tátil, adicione um highlight interno sutil na borda superior:
         box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12 a 0.22 em dark mode, ou rgba(255, 255, 255, 0.35 a 0.75) em light mode).
       - Utilize bordas translúcidas de 1px (border: 1px solid rgba(..., 0.08)) para definir o perímetro sem criar contraste artificial.

    3. RESPOSTA FÍSICA E DINÂMICA TÁTIL (INTERACTIONS):
       - Repouso (Resting): estado de repouso com elevação base (elevação de 1px a 2px).
       - Passagem (Hover): deslocamento ascendente suave (transform: translateY(-1px) ou translateY(-2px)) com expansão gradual do desfoque da sombra difusa.
       - Acionamento (Active / Pressed): compressão física nítida com deslocamento inteiro (transform: translateY(0px) — proibido scale() fracionário em textos para evitar borrão de GPU), com retração da sombra externa de volta ao Nível 1 / oclusão interna, transmitindo a sensação mecânica de curso de tecla real.
       - Suavização: transições determinísticas de curva de Bézier (transition: transform 100ms-160ms cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 160ms cubic-bezier(0.2, 0, 0, 1)).
  </physics_and_visual_guidelines>

  <constraints>
    - Proibido o uso de sombras com cores pretas puras (#000000) desvinculadas do tom do fundo no Light Mode; utilize tons derivados da superfície (ex.: rgba(15, 23, 42, alpha)) com canal alfa controlado.
    - Proibido o uso de esqueumorfismo agressivo ou chanfros de alto contraste dos anos 2000; o efeito deve ser perceptível como acabamento moderno e sutil.
    - Garantir conformidade com acessibilidade (WCAG 2.1 AA), mantendo indicadores de foco visíveis (:focus-visible) com anel de contraste desacoplado da sombra e respeito a @media (prefers-reduced-motion: reduce).
    - Não force classes de utilitários externas a menos que especificado pelo usuário.
  </constraints>

  <output_format>
    1. DIAGNÓSTICO OBJETIVO: síntese em 2 linhas dos problemas de profundidade e contraste do componente original.
    2. TOKENS CSS / DESIGN TOKENS: declaração formal das variáveis (:root ou tema Tailwind) de elevação e sombras.
    3. CÓDIGO REFATORADO: entrega do componente completo (HTML/CSS, Tailwind ou CSS-in-JS) sem truncamentos.
    4. ANÁLISE DE CAMADAS: tabela curta discriminando as camadas de sombra aplicadas e o efeito visual atribuído a cada uma.
  </output_format>
</system_instruction>
```

---

## 2. Folha de Estilos de Referência (`elevation-tactile-system.css`)

```css
/**
 * DESIGN SYSTEM - ESCALA DE ELEVAÇÃO TÁTIL & MICRO-RELEVO FÍSICO
 * 
 * Modelo Óptico:
 * 1. Oclusão de Contato (Ambient Occlusion): camada ultra-curta (1-2px), baixa difusão.
 * 2. Luz Direcional / Key Light: projeção descendente suave (eixo Y positivo).
 * 3. Chanfro Especular (Specular Rim / Bevel): micro-highlight interno superior (1px inset).
 */

:root {
  /* ==========================================================================
     PALETA DE SUPERFÍCIES & ILUMINAÇÃO (TEMA CLARO DEFAULT)
     ========================================================================== */
  --surface-canvas: #f8fafc;
  --surface-raised: #ffffff;
  --surface-overlay: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --brand-primary: #2563eb;
  --brand-primary-hover: #1d4ed8;
  --brand-text: #ffffff;

  /* Contraste Perimetral Neutro (Bordas Físicas) */
  --border-subtle: rgba(15, 23, 42, 0.08);
  --border-focus: #3b82f6;

  /* Micro-chanfro Especular (Luz Zenital incidente) */
  --specular-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.75);
  --specular-rim-interactive: inset 0 1px 0 0 rgba(255, 255, 255, 0.35);

  /* Curvas e Timings de Resposta Mecânica */
  --motion-press: 100ms cubic-bezier(0.2, 0.8, 0.2, 1);
  --motion-release: 160ms cubic-bezier(0.2, 0, 0, 1);

  /* ==========================================================================
     DESIGN TOKENS: ESCALA DE ELEVAÇÃO EM CAMADAS (LIGHT MODE)
     ========================================================================== */
  
  /* Elevação Baixa: Repouso de botões, chips, cards em repouso */
  --elevation-low: 
    0 1px 2px -1px rgba(15, 23, 42, 0.06),   /* Oclusão de base */
    0 2px 4px 0 rgba(15, 23, 42, 0.04);       /* Difusão suave */

  /* Elevação Média: Hover de botões, cards flutuantes, popovers */
  --elevation-medium: 
    0 2px 4px -1px rgba(15, 23, 42, 0.06),   /* Oclusão de contato */
    0 6px 14px -2px rgba(15, 23, 42, 0.08);   /* Key light dispersa */

  /* Elevação Alta: Modais, painéis suspensos, FABs */
  --elevation-high: 
    0 4px 8px -2px rgba(15, 23, 42, 0.05),   /* Oclusão imediata */
    0 16px 32px -4px rgba(15, 23, 42, 0.10);  /* Grande dispersão de luz */

  /* Elevação Comprimida: Estado :active mecânico */
  --elevation-pressed: 
    0 1px 1px 0 rgba(15, 23, 42, 0.08),      /* Colapso da key light */
    inset 0 1px 2px rgba(15, 23, 42, 0.12);   /* Micro-sombra de compressão */
}

/* ==========================================================================
   SUPORTE AUTOMÁTICO A DARK MODE (OU CLASSE .dark)
   ========================================================================== */
@media (prefers-color-scheme: dark) {
  :root {
    --surface-canvas: #090d16;
    --surface-raised: #131b2e;
    --surface-overlay: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --brand-primary: #3b82f6;
    --brand-primary-hover: #2563eb;
    --brand-text: #ffffff;

    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-focus: #60a5fa;

    /* No modo escuro, o chanfro especular se destaca com alfas menores */
    --specular-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.14);
    --specular-rim-interactive: inset 0 1px 0 0 rgba(255, 255, 255, 0.22);

    /* As sombras no Dark Mode dependem de oclusão reforçada com alfas ajustados */
    --elevation-low: 
      0 1px 2px 0 rgba(0, 0, 0, 0.40),
      0 2px 6px -1px rgba(0, 0, 0, 0.35);

    --elevation-medium: 
      0 3px 6px -1px rgba(0, 0, 0, 0.50),
      0 8px 20px -2px rgba(0, 0, 0, 0.45);

    --elevation-high: 
      0 6px 12px -2px rgba(0, 0, 0, 0.60),
      0 20px 40px -4px rgba(0, 0, 0, 0.55);

    --elevation-pressed: 
      0 1px 1px 0 rgba(0, 0, 0, 0.50),
      inset 0 1px 3px rgba(0, 0, 0, 0.60);
  }
}

/* ==========================================================================
   COMPONENTES TÁTEIS DE REFERÊNCIA
   ========================================================================== */

/* 1. BOTÃO PRIMÁRIO TÁTIL */
.btn-tactile {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0.625rem 1.25rem;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.25rem;
  color: var(--brand-text);
  background-color: var(--brand-primary);
  border: 1px solid var(--border-subtle);
  border-radius: 0.5rem;
  cursor: pointer;
  user-select: none;
  outline: none;

  /* Aplicação simultânea: Elevação difusa + Chanfro especular de topo */
  box-shadow: var(--elevation-low), var(--specular-rim-interactive);
  transition: transform var(--motion-release), box-shadow var(--motion-release), background-color var(--motion-release);
}

.btn-tactile:hover {
  background-color: var(--brand-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--elevation-medium), var(--specular-rim-interactive);
}

.btn-tactile:active {
  transform: translateY(0px);
  box-shadow: var(--elevation-pressed);
  transition-duration: var(--motion-press);
}

.btn-tactile:focus-visible {
  border-color: var(--border-focus);
  box-shadow: var(--elevation-low), var(--specular-rim-interactive), 0 0 0 3px rgba(59, 130, 246, 0.35);
}

/* 2. CARD ELEVADO DE SUPERFÍCIE */
.card-tactile {
  position: relative;
  background-color: var(--surface-raised);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: var(--elevation-low), var(--specular-rim);
  transition: transform var(--motion-release), box-shadow var(--motion-release);
}

.card-tactile.interactive {
  cursor: pointer;
}

.card-tactile.interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--elevation-medium), var(--specular-rim);
}

.card-tactile.interactive:active {
  transform: translateY(0px);
  box-shadow: var(--elevation-low), var(--specular-rim);
  transition-duration: var(--motion-press);
}

/* 3. PAINEL MODAL / DIALOG SUSPENSO */
.modal-tactile {
  background-color: var(--surface-overlay);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: var(--elevation-high), var(--specular-rim);
}

@media (prefers-reduced-motion: reduce) {
  .btn-tactile,
  .card-tactile {
    transition-duration: 0.01ms !important;
  }
}
```

---

## 3. Configuração de Referência para Tailwind CSS (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{html,js,ts,jsx,tsx,vue,svelte}',
    './components/**/*.{html,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          canvas: 'var(--surface-canvas, #f8fafc)',
          raised: 'var(--surface-raised, #ffffff)',
          overlay: 'var(--surface-overlay, #ffffff)',
        },
        tactile: {
          border: 'var(--border-subtle, rgba(15, 23, 42, 0.08))',
          focus: 'var(--border-focus, #3b82f6)',
        },
      },
      boxShadow: {
        'tactile-low': [
          '0 1px 2px -1px rgba(15, 23, 42, 0.06)',
          '0 2px 4px 0 rgba(15, 23, 42, 0.04)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.75)',
        ].join(', '),
        'tactile-md': [
          '0 2px 4px -1px rgba(15, 23, 42, 0.06)',
          '0 6px 14px -2px rgba(15, 23, 42, 0.08)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.75)',
        ].join(', '),
        'tactile-lg': [
          '0 4px 8px -2px rgba(15, 23, 42, 0.05)',
          '0 16px 32px -4px rgba(15, 23, 42, 0.10)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.75)',
        ].join(', '),
        'tactile-pressed': [
          '0 1px 1px 0 rgba(15, 23, 42, 0.08)',
          'inset 0 1px 2px 0 rgba(15, 23, 42, 0.14)',
        ].join(', '),
        'tactile-low-dark': [
          '0 1px 2px 0 rgba(0, 0, 0, 0.40)',
          '0 2px 6px -1px rgba(0, 0, 0, 0.35)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.14)',
        ].join(', '),
        'tactile-md-dark': [
          '0 3px 6px -1px rgba(0, 0, 0, 0.50)',
          '0 8px 20px -2px rgba(0, 0, 0, 0.45)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.18)',
        ].join(', '),
        'tactile-lg-dark': [
          '0 6px 12px -2px rgba(0, 0, 0, 0.60)',
          '0 20px 40px -4px rgba(0, 0, 0, 0.55)',
          'inset 0 1px 0 0 rgba(255, 255, 255, 0.22)',
        ].join(', '),
        'tactile-pressed-dark': [
          '0 1px 1px 0 rgba(0, 0, 0, 0.50)',
          'inset 0 1px 3px 0 rgba(0, 0, 0, 0.65)',
        ].join(', '),
      },
      transitionTimingFunction: {
        'press-snappy': 'cubic-bezier(0.2, 0.8, 0.2, 1)',
        'release-smooth': 'cubic-bezier(0.2, 0, 0, 1)',
      },
      transitionDuration: {
        'press': '100ms',
        'release': '160ms',
      },
    },
  },
  plugins: [
    function ({ addComponents, theme }) {
      addComponents({
        '.btn-tactile': {
          position: 'relative',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderRadius: '0.5rem',
          borderWidth: '1px',
          borderColor: 'var(--border-subtle, rgba(15, 23, 42, 0.08))',
          boxShadow: theme('boxShadow.tactile-low'),
          transitionProperty: 'transform, box-shadow, background-color',
          transitionDuration: theme('transitionDuration.release'),
          transitionTimingFunction: theme('transitionTimingFunction.release-smooth'),
          userSelect: 'none',
          outline: 'none',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: theme('boxShadow.tactile-md'),
          },
          '&:active': {
            transform: 'translateY(0px)',
            boxShadow: theme('boxShadow.tactile-pressed'),
            transitionDuration: theme('transitionDuration.press'),
            transitionTimingFunction: theme('transitionTimingFunction.press-snappy'),
          },
          '&:focus-visible': {
            borderColor: theme('colors.tactile.focus'),
            boxShadow: `${theme('boxShadow.tactile-low')}, 0 0 0 3px rgba(59, 130, 246, 0.35)`,
          },
        },
        '.card-tactile': {
          position: 'relative',
          borderRadius: '0.75rem',
          borderWidth: '1px',
          borderColor: 'var(--border-subtle, rgba(15, 23, 42, 0.08))',
          boxShadow: theme('boxShadow.tactile-low'),
          transitionProperty: 'transform, box-shadow',
          transitionDuration: theme('transitionDuration.release'),
          transitionTimingFunction: theme('transitionTimingFunction.release-smooth'),
          '&.interactive:hover': {
            transform: 'translateY(-2px)',
            boxShadow: theme('boxShadow.tactile-md'),
          },
          '&.interactive:active': {
            transform: 'translateY(0px)',
            boxShadow: theme('boxShadow.tactile-pressed'),
            transitionDuration: theme('transitionDuration.press'),
          },
        },
      });
    },
  ],
};
```
