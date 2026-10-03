import React from 'react';
import { ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import { SortField } from '../../types/drive';
import { useDrive } from '../../context/DriveContext';

interface SortHeaderProps {
  field?: SortField;
  label: string;
  className?: string;
  align?: 'left' | 'right';
}

export const SortHeader: React.FC<SortHeaderProps> = ({ field, label, className = '', align = 'left' }) => {
  const { query, setSort } = useDrive();
  const alignClass = align === 'right' ? 'text-right' : 'text-left';

  if (!field) {
    return (
      <th className={`py-3.5 px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider ${alignClass} ${className}`}>
        {label}
      </th>
    );
  }

  const isCurrentSort = query.sortField === field;
  const ariaSortValue = isCurrentSort ? (query.sortOrder === 'asc' ? 'ascending' : 'descending') : 'none';

  return (
    <th
      aria-sort={ariaSortValue}
      className={`py-3.5 px-4 text-xs font-semibold uppercase tracking-wider ${alignClass} ${className}`}
    >
      <button
        type="button"
        onClick={() => setSort(field)}
        aria-label={`Ordenar por ${label} (${isCurrentSort ? (query.sortOrder === 'asc' ? 'ordem crescente' : 'ordem decrescente') : 'não ordenado'})`}
        className="inline-flex items-center gap-1.5 text-slate-400 hover:text-slate-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900 rounded group transition-colors"
      >
        <span>{label}</span>
        {isCurrentSort ? (
          query.sortOrder === 'asc' ? (
            <ArrowUp className="w-3.5 h-3.5 text-sky-400" />
          ) : (
            <ArrowDown className="w-3.5 h-3.5 text-sky-400" />
          )
        ) : (
          <ArrowUpDown className="w-3.5 h-3.5 text-slate-600 group-hover:text-slate-400" />
        )}
      </button>
    </th>
  );
};
