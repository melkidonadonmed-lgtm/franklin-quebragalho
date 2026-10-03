import React from 'react';
import { ExternalLink, Star } from 'lucide-react';
import { DriveFile } from '../../types/drive';
import { MimeBadge } from '../atoms/MimeBadge';
import { CopyButton } from '../atoms/CopyButton';
import { formatFileSize, formatDate } from '../../services/driveService';

interface FileRowProps {
  file: DriveFile;
}

export const FileRow: React.FC<FileRowProps> = ({ file }) => {
  return (
    <tr className="border-b border-slate-800/80 hover:bg-slate-850/60 transition-colors group">
      {/* Nome e Categoria de Pasta */}
      <td className="py-3 px-4">
        <div className="flex items-start gap-2.5">
          {file.isStarred && <Star className="w-4 h-4 text-amber-400 fill-amber-400 mt-0.5 shrink-0" />}
          <div>
            {file.webViewLink ? (
              <a
                href={file.webViewLink}
                target="_blank"
                rel="noopener noreferrer"
                title={`Abrir ${file.name} no Google Drive`}
                className="font-medium text-slate-200 hover:text-sky-300 transition-colors break-words"
              >
                {file.name}
              </a>
            ) : (
              <div className="font-medium text-slate-200 group-hover:text-sky-300 transition-colors break-words">
                {file.name}
              </div>
            )}
            {file.folderCategory && (
              <span className="inline-block mt-0.5 text-xs text-slate-500 font-mono">
                {file.folderCategory}
              </span>
            )}
          </div>
        </div>
      </td>

      {/* ID do Google Drive */}
      <td className="py-3 px-4">
        <CopyButton textToCopy={file.id} />
      </td>

      {/* Tipo / Badge MIME */}
      <td className="py-3 px-4">
        <MimeBadge mimeType={file.mimeType} fileName={file.name} />
      </td>

      {/* Tamanho */}
      <td className="py-3 px-4 text-sm text-slate-300 font-mono whitespace-nowrap">
        {file.sizeBytes !== undefined ? formatFileSize(file.sizeBytes) : '—'}
      </td>

      {/* Data de Modificação */}
      <td className="py-3 px-4 text-sm text-slate-400 whitespace-nowrap">
        {formatDate(file.modifiedTime)}
      </td>

      {/* Proprietário */}
      <td className="py-3 px-4 text-sm text-slate-400 whitespace-nowrap">
        {Array.isArray(file.owners) && file.owners.length > 0
          ? file.owners.filter(Boolean).join(', ') || 'Meu Drive'
          : 'Meu Drive'}
      </td>

      {/* Ações */}
      <td className="py-3 px-4 text-right whitespace-nowrap">
        {file.webViewLink && (
          <a
            href={file.webViewLink}
            target="_blank"
            rel="noopener noreferrer"
            title="Abrir no Google Drive"
            aria-label={`Abrir ${file.name} no Google Drive`}
            className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold rounded-lg bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 hover:text-sky-300 border border-sky-500/20 transition-all"
          >
            Abrir
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}
      </td>
    </tr>
  );
};
