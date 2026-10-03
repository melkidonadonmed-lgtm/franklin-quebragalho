import React, { useState, useEffect } from 'react';
import { X, Key, ExternalLink, ShieldCheck, Check, Info, Trash2 } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';

export const ConfigModal: React.FC = () => {
  const {
    isConfigModalOpen,
    setIsConfigModalOpen,
    clientId,
    setClientId,
    loginWithGoogle,
    logout,
    isAuthenticated,
    clearError,
    showToast,
    dataSourceMode
  } = useDrive();

  const [inputVal, setInputVal] = useState<string>('');
  const inputRef = React.useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isConfigModalOpen) {
      setInputVal(clientId);
      const timer = setTimeout(() => {
        inputRef.current?.focus();
        inputRef.current?.select();
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [isConfigModalOpen, clientId]);

  // Fechar com tecla Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isConfigModalOpen) {
        setIsConfigModalOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isConfigModalOpen, setIsConfigModalOpen]);

  if (!isConfigModalOpen) return null;

  const currentOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:5173';

  const handleSaveAndConnect = async () => {
    const cleaned = inputVal.trim().replace(/^["']|["']$/g, '');
    if (!cleaned) {
      showToast('Por favor, insira um Client ID válido.', 'error');
      return;
    }
    setClientId(cleaned);
    setIsConfigModalOpen(false);
    showToast('Client ID salvo com sucesso! Iniciando autenticação...', 'info');
    // Dispara login imediatamente passando o Client ID digitado (elimina bug de stale closure)
    loginWithGoogle(cleaned);
  };

  const handleSaveOnly = () => {
    const cleaned = inputVal.trim().replace(/^["']|["']$/g, '');
    const wasDifferent = cleaned !== clientId;
    setClientId(cleaned);
    setIsConfigModalOpen(false);
    if (wasDifferent && isAuthenticated) {
      logout();
      showToast('Client ID alterado. Sessão anterior encerrada.', 'info');
    } else {
      showToast(cleaned ? 'Client ID salvo com sucesso!' : 'Configurações atualizadas.', 'success');
    }
  };

  const handleClear = () => {
    setClientId('');
    setInputVal('');
    clearError();
    if (isAuthenticated) {
      logout();
    }
    setIsConfigModalOpen(false);
    showToast('Client ID removido. Operando em Modo Demonstração.', 'info');
  };

  const handleContinueDemo = () => {
    setIsConfigModalOpen(false);
    clearError();
    if (isAuthenticated) {
      logout();
    } else {
      showToast('Operando em Modo Demonstração com arquivos clínicos.', 'info');
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in"
      onClick={() => setIsConfigModalOpen(false)}
    >
      <div
        className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 relative space-y-5"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Cabeçalho */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Key className="w-5 h-5" />
            </div>
            <div>
              <h2 id="modal-title" className="text-base sm:text-lg font-bold text-slate-100">
                Configuração do Google Drive API
              </h2>
              <p className="text-xs text-slate-400">
                Conecte seu Google Client ID para sincronização em tempo real
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsConfigModalOpen(false)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            aria-label="Fechar modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Status Atual */}
        <div className="flex items-center justify-between px-3.5 py-2.5 rounded-xl bg-slate-950/70 border border-slate-800/80 text-xs">
          <span className="text-slate-400">Status atual:</span>
          {dataSourceMode === 'google-drive' ? (
            <span className="inline-flex items-center gap-1.5 font-semibold text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Conectado à Google Drive API v3
            </span>
          ) : clientId ? (
            <span className="inline-flex items-center gap-1.5 font-semibold text-sky-400">
              <ShieldCheck className="w-4 h-4 text-sky-400" />
              Client ID Configurado (Pronto para conectar)
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 font-semibold text-amber-400">
              <Info className="w-4 h-4 text-amber-400" />
              Modo Demonstração Ativo (Mock)
            </span>
          )}
        </div>

        {/* Campo de Entrada */}
        <div className="space-y-2">
          <label htmlFor="client-id-input" className="block text-xs font-semibold text-slate-300">
            Google OAuth 2.0 Client ID (Aplicativo da Web)
          </label>
          <input
            ref={inputRef}
            id="client-id-input"
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSaveAndConnect();
              }
            }}
            placeholder="ex: 123456789012-abc...apps.googleusercontent.com"
            className="w-full px-3.5 py-2.5 bg-slate-950 text-slate-100 text-xs sm:text-sm font-mono rounded-xl border border-slate-700 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 transition-all placeholder:text-slate-600"
          />
          <p className="text-[11px] text-slate-500">
            Também pode ser definido via variável de ambiente <code className="text-slate-400 font-mono">VITE_GOOGLE_CLIENT_ID</code>.
          </p>
        </div>

        {/* Guia Rápido de Configuração */}
        <div className="p-3.5 rounded-xl bg-slate-950/50 border border-slate-800 space-y-2 text-xs text-slate-400">
          <div className="flex items-center justify-between text-slate-300 font-medium">
            <span className="flex items-center gap-1.5">
              <Info className="w-4 h-4 text-sky-400" />
              Requisitos no Google Cloud Console:
            </span>
            <a
              href="https://console.cloud.google.com/apis/credentials"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-[11px] text-sky-400 hover:text-sky-300 underline"
            >
              Abrir Console
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
          <ul className="list-disc list-inside space-y-1 text-[11px] text-slate-400">
            <li>
              Ative a <strong className="text-slate-300">Google Drive API</strong> no seu projeto.
            </li>
            <li>
              Crie uma credencial de <strong className="text-slate-300">ID do cliente OAuth (Aplicativo da Web)</strong>.
            </li>
            <li>
              Adicione a origem em JavaScript autorizada:{' '}
              <code className="text-sky-300 font-mono bg-slate-900 px-1 py-0.5 rounded">
                {currentOrigin}
              </code>
            </li>
            <li>
              Escopo solicitado:{' '}
              <code className="text-sky-300 font-mono bg-slate-900 px-1 py-0.5 rounded">
                .../auth/drive.readonly
              </code>
            </li>
          </ul>
        </div>

        {/* Botões de Ação */}
        <div className="space-y-2 pt-2 border-t border-slate-800">
          <div className="flex flex-col sm:flex-row items-center gap-2">
            <button
              onClick={handleSaveAndConnect}
              className="w-full sm:flex-1 py-2.5 px-4 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-semibold text-xs sm:text-sm transition-all shadow-lg shadow-sky-500/20 flex items-center justify-center gap-2"
            >
              <Check className="w-4 h-4" />
              Salvar e Conectar Google
            </button>
            <button
              onClick={handleSaveOnly}
              className="w-full sm:w-auto py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs sm:text-sm border border-slate-700 transition-all"
            >
              Salvar Apenas
            </button>
          </div>

          <div className="flex items-center justify-between pt-1">
            <button
              onClick={handleContinueDemo}
              className="text-xs text-slate-400 hover:text-slate-200 transition-colors"
            >
              Continuar em Modo Demonstração
            </button>
            {clientId && (
              <button
                onClick={handleClear}
                className="inline-flex items-center gap-1 text-xs text-rose-400 hover:text-rose-300 transition-colors"
              >
                <Trash2 className="w-3.5 h-3.5" />
                Remover ID Salvo
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
