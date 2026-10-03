import React from 'react';
import { useDrive } from '../../context/DriveContext';
import { SortHeader } from '../molecules/SortHeader';
import { FileRow } from '../molecules/FileRow';
import { EmptyState } from './EmptyState';

export const FileTable: React.FC = () => {
  const { filteredFiles, isLoading, isAuthenticating, error, refreshFiles, logout, loginWithGoogle } = useDrive();

  if (isLoading) {
    return (
      <div className="py-20 text-center">
        <div className="w-10 h-10 border-4 border-sky-500/20 border-t-sky-500 rounded-full animate-spin mx-auto mb-4" />
        <p className="text-sm text-slate-400">Indexando arquivos do Google Drive...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center bg-rose-500/10 border border-rose-500/30 rounded-2xl text-rose-300 space-y-4">
        <div>
          <p className="font-semibold text-base mb-1">Falha na Conexão com Google Drive</p>
          <p className="text-xs text-rose-400/90 max-w-lg mx-auto">{error}</p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button
            onClick={() => loginWithGoogle()}
            disabled={isAuthenticating}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 transition-all shadow-md shadow-sky-500/20 disabled:opacity-50"
          >
            Reconectar Google
          </button>
          <button
            onClick={() => refreshFiles()}
            disabled={isAuthenticating}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-rose-500 hover:bg-rose-400 text-slate-950 transition-all shadow-md shadow-rose-500/20 disabled:opacity-50"
          >
            Tentar Novamente
          </button>
          <button
            onClick={() => logout()}
            className="px-4 py-2 text-xs font-medium rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-all"
          >
            Restaurar Modo Demonstração
          </button>
        </div>
      </div>
    );
  }

  return (
    <section className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden shadow-lg backdrop-blur-sm">
      {/* Barra de Acessibilidade e Status */}
      <div className="px-4 py-3 border-b border-slate-800 bg-slate-900/80 flex items-center justify-between text-xs text-slate-400">
        <div aria-live="polite" aria-atomic="true">
          Mostrando <strong className="text-slate-200">{filteredFiles.length}</strong> arquivos encontrados
        </div>
        <div className="text-[11px] text-slate-500">
          Clique nas colunas para ordenar
        </div>
      </div>

      {filteredFiles.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse" role="table">
            <thead>
              <tr className="bg-slate-950/60 border-b border-slate-800">
                <SortHeader field="name" label="Nome do Arquivo" />
                <th className="py-3.5 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Google Drive ID
                </th>
                <th className="py-3.5 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Tipo MIME
                </th>
                <SortHeader field="sizeBytes" label="Tamanho" />
                <SortHeader field="modifiedTime" label="Modificado em" />
                <th className="py-3.5 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Proprietário
                </th>
                <th className="py-3.5 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider text-right">
                  Ação
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {filteredFiles.map((file) => (
                <FileRow key={file.id} file={file} />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
};
