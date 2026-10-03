import React from 'react';
import { CheckCircle2, AlertCircle, Info } from 'lucide-react';
import { DriveProvider, useDrive } from './context/DriveContext';
import { DriveHeader } from './components/organisms/DriveHeader';
import { StatsOverview } from './components/organisms/StatsOverview';
import { SearchInput } from './components/atoms/SearchInput';
import { FilterChips } from './components/molecules/FilterChips';
import { FileTable } from './components/organisms/FileTable';
import { ConfigModal } from './components/organisms/ConfigModal';

const DriveAppContent: React.FC = () => {
  const { toast } = useDrive();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-sky-500 selection:text-white">
      {/* Cabeçalho de Navegação e Autenticação */}
      <DriveHeader />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Painel de Métricas e Resumo */}
        <StatsOverview />

        {/* Barra de Controles e Busca Global */}
        <section className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 sm:p-5 mb-6 shadow-md backdrop-blur-sm space-y-3">
          <SearchInput />
          <FilterChips />
        </section>

        {/* Tabela de Arquivos */}
        <FileTable />
      </main>

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>Google Drive Explorer • Desenvolvido com React 18, Vite e Tailwind CSS</p>
      </footer>

      {/* Modal de Configuração do Client ID */}
      <ConfigModal />

      {/* Toast Notification Flutuante com Suporte a Tipos (Sucesso, Erro, Info) */}
      {toast && (
        <aside
          role="status"
          aria-live="polite"
          className={`fixed bottom-6 right-6 z-50 px-4 py-3 font-medium text-xs sm:text-sm rounded-xl shadow-2xl flex items-center gap-2.5 transition-all duration-200 ${
            toast.type === 'error'
              ? 'bg-rose-500 text-white shadow-rose-500/30 border border-rose-400'
              : toast.type === 'info'
              ? 'bg-slate-850 text-sky-300 shadow-slate-950/70 border border-slate-700'
              : 'bg-sky-500 text-slate-950 shadow-sky-500/30 border border-sky-400 font-semibold'
          }`}
        >
          {toast.type === 'error' && <AlertCircle className="w-4 h-4 shrink-0 text-white" />}
          {toast.type === 'info' && <Info className="w-4 h-4 shrink-0 text-sky-400" />}
          {toast.type === 'success' && <CheckCircle2 className="w-4 h-4 shrink-0 text-slate-950" />}
          <span>{toast.message}</span>
        </aside>
      )}
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <DriveProvider>
      <DriveAppContent />
    </DriveProvider>
  );
};

export default App;
