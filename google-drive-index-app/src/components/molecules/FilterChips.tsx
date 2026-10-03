import React from 'react';
import { MimeCategory } from '../../types/drive';
import { useDrive } from '../../context/DriveContext';

interface FilterOption {
  id: MimeCategory;
  label: string;
}

const FILTER_OPTIONS: FilterOption[] = [
  { id: 'all', label: 'Todos os Arquivos' },
  { id: 'document', label: 'Documentos' },
  { id: 'spreadsheet', label: 'Planilhas' },
  { id: 'pdf', label: 'PDFs' },
  { id: 'code', label: 'Códigos & Markdown' },
  { id: 'image', label: 'Imagens' },
  { id: 'folder', label: 'Pastas' }
];

export const FilterChips: React.FC = () => {
  const { query, setCategory, stats } = useDrive();

  return (
    <div className="flex flex-wrap items-center gap-2 pt-2">
      <span className="text-xs font-medium text-slate-400 mr-1">Filtrar por:</span>
      {FILTER_OPTIONS.map((opt) => {
        const isActive = query.category === opt.id;
        const count = stats.categoryCounts[opt.id] ?? 0;

        return (
          <button
            key={opt.id}
            onClick={() => setCategory(opt.id)}
            className={`inline-flex items-center gap-1.5 px-3 py-1 text-xs rounded-full font-medium transition-all ${
              isActive
                ? 'bg-sky-500 text-slate-950 font-semibold shadow-md shadow-sky-500/20'
                : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-700/60'
            }`}
          >
            <span>{opt.label}</span>
            <span
              className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                isActive ? 'bg-sky-950 text-sky-200' : 'bg-slate-800 text-slate-400'
              }`}
            >
              {count}
            </span>
          </button>
        );
      })}
    </div>
  );
};
