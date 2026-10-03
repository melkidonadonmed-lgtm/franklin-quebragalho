import React from 'react';
import { Files, HardDrive, FileText, CheckCircle2 } from 'lucide-react';
import { useDrive } from '../../context/DriveContext';
import { formatFileSize } from '../../services/driveService';

export const StatsOverview: React.FC = () => {
  const { stats, filteredFiles, dataSourceMode } = useDrive();

  return (
    <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {/* Card 1: Total de Arquivos */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Catalogado</span>
          <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
            <Files className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-100">{stats.totalFiles}</div>
        <p className="text-xs text-slate-500 mt-1">Arquivos indexados no sistema</p>
      </div>

      {/* Card 2: Espaço Ocupado */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Espaço em Disco</span>
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <HardDrive className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-100">{formatFileSize(stats.totalSizeBytes)}</div>
        <p className="text-xs text-slate-500 mt-1">Volume consolidado dos metadados</p>
      </div>

      {/* Card 3: Documentos e PDFs */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Docs & PDFs</span>
          <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
            <FileText className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-100">
          {(stats.categoryCounts.document || 0) + (stats.categoryCounts.pdf || 0)}
        </div>
        <p className="text-xs text-slate-500 mt-1">
          {dataSourceMode === 'google-drive' ? 'Documentos e PDFs na nuvem' : 'Receitas, laudos e protocolos'}
        </p>
      </div>

      {/* Card 4: Resultados da Busca Atual */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Filtro Ativo</span>
          <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
            <CheckCircle2 className="w-4 h-4" />
          </div>
        </div>
        <div className="text-2xl font-bold text-sky-400">{filteredFiles.length}</div>
        <p className="text-xs text-slate-500 mt-1">Arquivos visíveis na tabela</p>
      </div>
    </section>
  );
};
