import React, { useEffect } from 'react';
import { AlertCircle, CheckCircle2, Info, TriangleAlert, X } from 'lucide-react';
import { ToastMessage, ToastVariant } from '../../types';

export interface NotificationToastProps {
  toast: ToastMessage;
  onDismiss: (id: string) => void;
}

export const NotificationToast: React.FC<NotificationToastProps> = ({ toast, onDismiss }) => {
  const { id, type, title, description, durationMs = 5000 } = toast;

  // Auto-dismiss temporizado
  useEffect(() => {
    if (durationMs > 0) {
      const timer = setTimeout(() => {
        onDismiss(id);
      }, durationMs);
      return () => clearTimeout(timer);
    }
  }, [id, durationMs, onDismiss]);

  // Fechamento acessível via tecla Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onDismiss(id);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [id, onDismiss]);

  const variantStyles: Record<
    ToastVariant,
    { icon: React.ReactNode; borderColor: string; barColor: string }
  > = {
    info: {
      icon: <Info className="w-5 h-5 text-[var(--accent-action)]" />,
      borderColor: 'border-[var(--accent-action)]/30',
      barColor: 'bg-[var(--accent-action)]',
    },
    success: {
      icon: <CheckCircle2 className="w-5 h-5 text-[var(--status-success)]" />,
      borderColor: 'border-[var(--status-success)]/30',
      barColor: 'bg-[var(--status-success)]',
    },
    warning: {
      icon: <TriangleAlert className="w-5 h-5 text-[var(--status-warning)]" />,
      borderColor: 'border-[var(--status-warning)]/30',
      barColor: 'bg-[var(--status-warning)]',
    },
    danger: {
      icon: <AlertCircle className="w-5 h-5 text-[var(--status-danger)]" />,
      borderColor: 'border-[var(--status-danger)]/30',
      barColor: 'bg-[var(--status-danger)]',
    },
  };

  const currentVariant = variantStyles[type];

  return (
    <div
      role="alert"
      aria-live="assertive"
      className={`
        relative flex items-start gap-3.5 p-4
        w-full max-w-md
        bg-[var(--surface-panel)]
        text-[var(--text-primary)]
        rounded-2xl
        border ${currentVariant.borderColor}
        shadow-[var(--shadow-tactile-raised)]
        transition-all duration-200 ease-out
        overflow-hidden
      `}
    >
      {/* Barra de acento visual lateral */}
      <div className={`absolute left-0 top-0 bottom-0 w-1 ${currentVariant.barColor}`} />

      {/* Ícone de status */}
      <div className="shrink-0 mt-0.5">{currentVariant.icon}</div>

      {/* Conteúdo textual */}
      <div className="flex-1 min-w-0 pr-2">
        <h4 className="text-sm font-semibold tracking-wide text-[var(--text-primary)]">
          {title}
        </h4>
        {description && (
          <p className="mt-1 text-xs text-[var(--text-secondary)] leading-relaxed">
            {description}
          </p>
        )}
      </div>

      {/* Botão semântico de dispensar */}
      <button
        type="button"
        aria-label="Dispensar notificação"
        onClick={() => onDismiss(id)}
        className="
          shrink-0 p-1
          text-[var(--text-muted)]
          hover:text-[var(--text-primary)]
          hover:bg-[rgba(255,255,255,0.06)]
          rounded-lg
          transition-colors duration-150
          focus-visible:outline-none
          focus-visible:ring-2
          focus-visible:ring-[var(--accent-action)]
        "
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
