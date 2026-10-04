import React, { useRef, useEffect } from 'react';
import { Search } from 'lucide-react';

export interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSearch?: (value: string) => void;
  placeholder?: string;
  shortcutHint?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  onSearch,
  placeholder = 'Pesquisar arquivos, fluxos ou configurações...',
  shortcutHint = 'Ctrl+K',
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  // Captura global do atalho de pesquisa (Ctrl+K ou Cmd+K)
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
        inputRef.current?.select();
      }
    };

    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && onSearch) {
      onSearch(value);
    }
  };

  return (
    <div className="relative flex items-center w-full max-w-md">
      <div className="absolute left-3.5 flex items-center pointer-events-none text-[var(--text-muted)] shrink-0">
        <Search className="w-4 h-4" />
      </div>

      <input
        ref={inputRef}
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className="
          w-full h-10 pl-10 pr-20
          bg-[var(--surface-sunken)]
          text-[var(--text-primary)]
          placeholder:text-[var(--text-muted)]
          text-xs tracking-wide
          rounded-xl
          border border-[var(--border-subtle)]
          shadow-[var(--shadow-tactile-inset)]
          transition-all duration-150 ease-out
          focus-visible:outline-none
          focus-visible:border-[var(--accent-action)]
          focus-visible:ring-2
          focus-visible:ring-[var(--accent-focus)]
        "
      />

      <div className="absolute right-2.5 flex items-center pointer-events-none">
        <kbd
          className="
            px-2 py-0.5
            text-[10px] font-mono font-medium
            text-[var(--text-muted)]
            bg-[rgba(255,255,255,0.06)]
            border border-[var(--border-subtle)]
            rounded-md
            shadow-sm
          "
        >
          {shortcutHint}
        </kbd>
      </div>
    </div>
  );
};
