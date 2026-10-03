import React from 'react';
import { SearchX } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';

export const EmptyState: React.FC = () => {
  const { files, query, setSearchTerm, setCategory, refreshFiles, logout } = useDrive();

  const handleReset = () => {
    setSearchTerm('');
    setCategory('all');
  };

  const isCatalogEmpty = files.length === 0;

  return (
    <div className="py-16 px-4 text-center">
      <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-slate-400">
        <SearchX className="w-7 h-7" />
      </div>
      <h3 className="text-base font-semibold text-slate-200 mb-1">
        {isCatalogEmpty ? 'Nenhum arquivo no catálogo' : 'Nenhum arquivo encontrado'}
      </h3>
      <p className="text-sm text-slate-400 max-w-sm mx-auto mb-5">
        {isCatalogEmpty
          ? 'Nenhum arquivo ativo foi localizado na sua conta Google Drive.'
          : `Não encontramos nenhum item correspondente a ${
              query.searchTerm ? `"${query.searchTerm}"` : 'este filtro'
            }.`}
      </p>
      {isCatalogEmpty ? (
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => refreshFiles()}
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 transition-all shadow-md shadow-sky-500/10"
          >
            Sincronizar Novamente
          </button>
          <button
            onClick={() => logout()}
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
          >
            Carregar Demonstração
          </button>
        </div>
      ) : (
        <button
          onClick={handleReset}
          className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 transition-all shadow-md shadow-sky-500/10"
        >
          Limpar Filtros e Buscar Novamente
        </button>
      )}
    </div>
  );
};
