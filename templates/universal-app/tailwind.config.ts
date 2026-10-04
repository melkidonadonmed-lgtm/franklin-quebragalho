import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        canvas: {
          bg: 'var(--canvas-bg)',
        },
        surface: {
          card: 'var(--surface-card)',
          panel: 'var(--surface-panel)',
          sunken: 'var(--surface-sunken)',
        },
        rim: {
          DEFAULT: 'var(--border-rim)',
          highlight: 'var(--border-rim-highlight)',
          subtle: 'var(--border-subtle)',
        },
        font: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)',
        },
        accent: {
          action: 'var(--accent-action)',
          focus: 'var(--accent-focus)',
        },
        status: {
          success: 'var(--status-success)',
          warning: 'var(--status-warning)',
          danger: 'var(--status-danger)',
        },
      },
      boxShadow: {
        'tactile-inset': 'var(--shadow-tactile-inset)',
        'tactile-card': 'var(--shadow-tactile-card)',
        'tactile-raised': 'var(--shadow-tactile-raised)',
        'tactile-button': 'var(--shadow-tactile-button)',
        'tactile-button-active': 'var(--shadow-tactile-button-active)',
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          'sans-serif',
        ],
      },
    },
  },
  plugins: [],
};

export default config;
