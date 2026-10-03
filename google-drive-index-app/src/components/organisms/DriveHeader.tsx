import React from 'react';
import { Cloud, RefreshCw, Settings, LogOut } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';

export const DriveHeader: React.FC = () => {
  const {
    isLoading,
    isAuthenticating,
    refreshFiles,
    isAuthenticated,
    userProfile,
    loginWithGoogle,
    logout,
    setIsConfigModalOpen,
    dataSourceMode,
    clientId,
    error
  } = useDrive();

  const [avatarFailed, setAvatarFailed] = React.useState<boolean>(false);

  // Reseta estado de falha de avatar quando userProfile mudar
  React.useEffect(() => {
    setAvatarFailed(false);
  }, [userProfile?.avatarUrl]);

  return (
    <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Marca & Identidade */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-sky-500/20 shrink-0">
            <Cloud className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base sm:text-lg font-bold text-slate-100">
                Google Drive Explorer
              </h1>
              {dataSourceMode === 'google-drive' ? (
                error ? (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
                    Erro de Conexão
                  </span>
                ) : (
                  <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    API v3 Online
                  </span>
                )
              ) : (
                <button
                  onClick={() => setIsConfigModalOpen(true)}
                  className="hidden sm:inline-flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 border border-amber-500/30 transition-colors"
                  title="Operando com dados simulados do internato médico. Clique para configurar credenciais."
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
                  Modo Demonstração
                </button>
              )}
            </div>
            <p className="text-xs text-slate-400 hidden xs:block">
              Catálogo interativo com IDs de arquivo e busca instantânea
            </p>
          </div>
        </div>

        {/* Ações do Topo */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Botão de Configuração de Client ID */}
          <button
            onClick={() => setIsConfigModalOpen(true)}
            className="relative p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 hover:text-slate-100 border border-slate-700/60 transition-all"
            title="Configurar Google Client ID"
            aria-label="Abrir configurações de autenticação"
          >
            <Settings className="w-4 h-4" />
            {!clientId && (
              <span
                className="absolute top-1 right-1 w-2 h-2 rounded-full bg-amber-400"
                title="Client ID não configurado"
              />
            )}
          </button>

          {/* Botão de Sincronização */}
          <button
            onClick={() => refreshFiles()}
            disabled={isLoading || isAuthenticating}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs sm:text-sm font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all disabled:opacity-50"
            title="Sincronizar arquivos agora"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-sky-400' : ''}`} />
            <span className="hidden md:inline">Sincronizar</span>
          </button>

          {/* Área de Autenticação */}
          {isAuthenticated ? (
            <div className="flex items-center gap-2 pl-1 border-l border-slate-800">
              {/* Perfil do Usuário */}
              <div
                className="flex items-center gap-2 px-2 py-1 rounded-lg bg-slate-800/60 border border-slate-700/60 max-w-[160px] sm:max-w-[200px]"
                title={`Conectado como ${userProfile?.name || 'Conta Google'} (${userProfile?.email || 'Google Drive'})`}
              >
                {userProfile?.avatarUrl && !avatarFailed ? (
                  <img
                    src={userProfile.avatarUrl}
                    alt={userProfile.name || 'Avatar'}
                    referrerPolicy="no-referrer"
                    className="w-6 h-6 rounded-full border border-slate-700 object-cover shrink-0"
                    onError={() => setAvatarFailed(true)}
                  />
                ) : (
                  <div className="w-6 h-6 rounded-full bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-[11px] border border-sky-500/30 shrink-0">
                    {(userProfile?.name || 'U').trim().charAt(0).toUpperCase() || 'U'}
                  </div>
                )}
                <span className="text-xs font-medium text-slate-200 truncate hidden sm:inline">
                  {userProfile?.name || 'Conta Google'}
                </span>
              </div>

              {/* Botão Desconectar */}
              <button
                onClick={() => logout()}
                disabled={isLoading}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/20 transition-all"
                title="Desconectar do Google"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Desconectar</span>
              </button>
            </div>
          ) : (
            <button
              onClick={() => loginWithGoogle()}
              disabled={isAuthenticating || isLoading}
              className="inline-flex items-center gap-2 px-3 sm:px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-lg bg-sky-500 hover:bg-sky-400 text-slate-950 transition-all shadow-md shadow-sky-500/20 disabled:opacity-50 active:scale-95"
            >
              {isAuthenticating ? (
                <>
                  <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  <span>Conectando...</span>
                </>
              ) : (
                <>
                  {/* Ícone Google oficial colorido */}
                  <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24">
                    <path
                      fill="#4285F4"
                      d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3.03h3.88c2.27-2.09 3.665-5.17 3.665-9.12z"
                    />
                    <path
                      fill="#34A853"
                      d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.03c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.13C3.28 21.43 7.35 24 12 24z"
                    />
                    <path
                      fill="#FBBC05"
                      d="M5.28 14.29c-.25-.72-.38-1.49-.38-2.29s.13-1.57.38-2.29V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.13z"
                    />
                    <path
                      fill="#EA4335"
                      d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.35 0 3.28 2.57 1.25 6.58l4.03 3.13c.95-2.83 3.6-4.96 6.72-4.96z"
                    />
                  </svg>
                  <span className="hidden xs:inline">Conectar Google</span>
                  <span className="xs:hidden">Conectar</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
