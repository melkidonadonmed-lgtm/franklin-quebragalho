import React from 'react';
import { FileText, FileSpreadsheet, File, Folder, Image, Code2 } from 'lucide-react';
import { categorizeMime } from '../../services/driveService';

interface MimeBadgeProps {
  mimeType: string;
  fileName: string;
}

export const MimeBadge: React.FC<MimeBadgeProps> = ({ mimeType, fileName }) => {
  const category = categorizeMime(mimeType, fileName);

  switch (category) {
    case 'pdf':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-300 border border-rose-500/30">
          <FileText className="w-3.5 h-3.5 text-rose-400" />
          PDF
        </span>
      );
    case 'spreadsheet':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
          <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-400" />
          Planilha
        </span>
      );
    case 'document':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-500/10 text-sky-300 border border-sky-500/30">
          <FileText className="w-3.5 h-3.5 text-sky-400" />
          Doc
        </span>
      );
    case 'folder':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/30">
          <Folder className="w-3.5 h-3.5 text-amber-400" />
          Pasta
        </span>
      );
    case 'image':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-300 border border-purple-500/30">
          <Image className="w-3.5 h-3.5 text-purple-400" />
          Imagem
        </span>
      );
    case 'code':
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
          <Code2 className="w-3.5 h-3.5 text-indigo-400" />
          Código
        </span>
      );
    default:
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-500/10 text-slate-300 border border-slate-500/30">
          <File className="w-3.5 h-3.5 text-slate-400" />
          Arquivo
        </span>
      );
  }
};
