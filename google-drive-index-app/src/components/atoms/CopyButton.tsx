import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';

interface CopyButtonProps {
  textToCopy: string;
  label?: string;
}

export const CopyButton: React.FC<CopyButtonProps> = ({ textToCopy, label = 'Copiar ID' }) => {
  const [copied, setCopied] = useState<boolean>(false);
  const { showToast } = useDrive();
  const copyTimerRef = React.useRef<ReturnType<typeof setTimeout> | null>(null);

  React.useEffect(() => {
    return () => {
      if (copyTimerRef.current) {
        clearTimeout(copyTimerRef.current);
      }
    };
  }, []);

  const handleCopy = async (e: React.MouseEvent) => {
    e.stopPropagation();

    // Feedback tátil via Vibration API caso suportado pelo dispositivo
    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try {
        navigator.vibrate(40);
      } catch {
        // Ignora caso não permitido
      }
    }

    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      showToast(`ID copiado: ${textToCopy}`);
      if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
      copyTimerRef.current = setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback para navegadores sem API Clipboard moderna
      const textarea = document.createElement('textarea');
      textarea.value = textToCopy;
      textarea.style.position = 'fixed';
      textarea.style.top = '0';
      textarea.style.left = '0';
      textarea.style.opacity = '0';
      textarea.style.pointerEvents = 'none';
      document.body.appendChild(textarea);
      try {
        textarea.focus();
        textarea.select();
        document.execCommand('copy');
        setCopied(true);
        showToast(`ID copiado: ${textToCopy}`);
        if (copyTimerRef.current) clearTimeout(copyTimerRef.current);
        copyTimerRef.current = setTimeout(() => setCopied(false), 2000);
      } catch {
        showToast('Não foi possível copiar o ID.', 'error');
      } finally {
        if (textarea.parentNode) {
          document.body.removeChild(textarea);
        }
      }
    }
  };

  return (
    <button
      onClick={handleCopy}
      title={label}
      aria-label={`${label}: ${textToCopy}`}
      className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-mono rounded-md bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-sky-300 border border-slate-700/60 transition-all active:scale-95"
    >
      {copied ? (
        <>
          <Check className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-emerald-400 font-medium">Copiado!</span>
        </>
      ) : (
        <>
          <Copy className="w-3.5 h-3.5 text-slate-400 group-hover:text-sky-400" />
          <span className="truncate max-w-[90px] sm:max-w-[130px]">{textToCopy}</span>
        </>
      )}
    </button>
  );
};
