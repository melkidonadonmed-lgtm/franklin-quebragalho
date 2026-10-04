import React, { ButtonHTMLAttributes } from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface TactileButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  icon?: React.ReactNode;
  isLoading?: boolean;
}

export const TactileButton: React.FC<TactileButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  isLoading = false,
  disabled,
  className = '',
  ...props
}) => {
  // Configuração ergonômica de dimensões e padding
  const sizeClasses = {
    sm: 'h-9 px-3.5 text-xs gap-1.5',
    md: 'h-11 px-5 text-sm gap-2', // Altura padrão de 44px
    lg: 'h-13 px-6 text-base gap-2.5',
  }[size];

  // Variantes estilizadas segundo o Design System Tátil
  const variantClasses = {
    primary: `
      bg-[var(--accent-action)] text-slate-950 font-semibold
      shadow-[var(--shadow-tactile-button)]
      hover:brightness-110
      active:shadow-[var(--shadow-tactile-button-active)]
      border-t border-[rgba(255,255,255,0.3)]
    `,
    secondary: `
      bg-[var(--surface-card)] text-[var(--text-primary)] font-medium
      shadow-[var(--shadow-tactile-card)]
      hover:bg-[var(--surface-panel)]
      active:shadow-[var(--shadow-tactile-inset)]
      border border-[var(--border-rim)]
      border-t-[var(--border-rim-highlight)]
    `,
    outline: `
      bg-transparent text-[var(--text-primary)] font-medium
      border border-[var(--border-rim-highlight)]
      hover:bg-[rgba(255,255,255,0.04)]
      active:bg-[rgba(255,255,255,0.08)]
    `,
    ghost: `
      bg-transparent text-[var(--text-secondary)] font-medium
      hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.04)]
      active:bg-[rgba(255,255,255,0.08)]
    `,
    danger: `
      bg-[var(--status-danger)] text-white font-semibold
      shadow-[var(--shadow-tactile-button)]
      hover:brightness-110
      active:shadow-[var(--shadow-tactile-button-active)]
      border-t border-[rgba(255,255,255,0.25)]
    `,
  }[variant];

  return (
    <button
      type="button"
      disabled={disabled || isLoading}
      className={`
        relative inline-flex items-center justify-center
        shrink-0 whitespace-nowrap select-none
        rounded-xl
        tracking-wide
        transition-all duration-150 ease-out
        active:scale-[0.98]
        focus-visible:outline-none
        focus-visible:ring-2
        focus-visible:ring-[var(--accent-action)]
        focus-visible:ring-offset-2
        focus-visible:ring-offset-[var(--canvas-bg)]
        disabled:opacity-50 disabled:pointer-events-none disabled:active:scale-100
        ${sizeClasses}
        ${variantClasses}
        ${className}
      `}
      {...props}
    >
      {isLoading ? (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin shrink-0" />
      ) : (
        icon && <span className="shrink-0">{icon}</span>
      )}
      <span>{children}</span>
    </button>
  );
};
