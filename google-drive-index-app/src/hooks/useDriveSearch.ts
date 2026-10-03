import { useMemo } from 'react';
import { DriveFile, DriveQuery } from '../types/drive';
import { categorizeMime } from '../services/driveService';

export function searchAndSortFiles(files: DriveFile[], query: DriveQuery): DriveFile[] {
  const term = query.searchTerm.toLowerCase().trim();

  return files
    .filter((file) => {
      // Filtro por Categoria MIME
      if (query.category !== 'all') {
        const cat = categorizeMime(file.mimeType, file.name);
        if (cat !== query.category) return false;
      }

      // Filtro por Termo de Busca (Nome, ID, Categoria ou Dono)
      if (term) {
        const matchName = (file.name || '').toLowerCase().includes(term);
        const matchId = (file.id || '').toLowerCase().includes(term);
        const matchCategory = (file.folderCategory || '').toLowerCase().includes(term);
        const matchOwner = Array.isArray(file.owners) && file.owners.some((o) => (o || '').toLowerCase().includes(term));
        return matchName || matchId || matchCategory || matchOwner;
      }

      return true;
    })
    .sort((a, b) => {
      const orderMod = query.sortOrder === 'asc' ? 1 : -1;

      if (query.sortField === 'name') {
        return (a.name || '').localeCompare(b.name || '') * orderMod;
      }

      if (query.sortField === 'sizeBytes') {
        const sizeA = a.sizeBytes || 0;
        const sizeB = b.sizeBytes || 0;
        return (sizeA - sizeB) * orderMod;
      }

      if (query.sortField === 'modifiedTime') {
        const parsedA = a.modifiedTime ? new Date(a.modifiedTime).getTime() : 0;
        const parsedB = b.modifiedTime ? new Date(b.modifiedTime).getTime() : 0;
        const timeA = Number.isNaN(parsedA) ? 0 : parsedA;
        const timeB = Number.isNaN(parsedB) ? 0 : parsedB;
        return (timeA - timeB) * orderMod;
      }

      return 0;
    });
}

export function useDriveSearch(files: DriveFile[], query: DriveQuery): DriveFile[] {
  return useMemo(() => searchAndSortFiles(files, query), [files, query]);
}
