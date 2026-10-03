import React, { useRef, useEffect } from 'react';
import { Search, X } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';

export const SearchInput: React.FC = () => {
  const { query, setSearchTerm, isConfigModalOpen } = useDrive();
  const inputRef = useRef<HTMLInputElement>(null);

  // Atalho de teclado global Ctrl+K / Cmd+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        if (isConfigModalOpen) return;
        e.preventDefault();
        inputRef.current?.focus();
        inputRef.current?.select();
      }
      if (e.key === 'Escape' && document.activeElement === inputRef.current) {
        setSearchTerm('');
        inputRef.current?.blur();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [setSearchTerm, isConfigModalOpen]);

  return (
    <div className="relative flex items-center w-full">
      <Search className="absolute left-3.5 w-5 h-5 text-slate-400 pointer-events-none" />
      <input
        ref={inputRef}
        type="text"
        value={query.searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Buscar por arquivo, ID, pasta ou autor (Ctrl + K)..."
        aria-label="Buscar arquivos no Google Drive"
        className="w-full pl-11 pr-24 py-2.5 bg-slate-900/90 text-slate-100 placeholder-slate-400 text-sm md:text-base rounded-xl border border-slate-700/80 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 transition-all shadow-inner"
      />
      <div className="absolute right-3 flex items-center gap-1.5">
        {query.searchTerm && (
          <button
            onClick={() => setSearchTerm('')}
            aria-label="Limpar busca"
            className="p-1 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-md transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        <kbd className="hidden sm:inline-flex items-center px-1.5 py-0.5 text-[11px] font-mono font-medium text-slate-400 bg-slate-800/80 border border-slate-700 rounded shadow-sm">
          ⌘K
        </kbd>
      </div>
    </div>
  );
};
