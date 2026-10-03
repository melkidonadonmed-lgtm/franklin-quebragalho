import React, { createContext, useContext, useState, useEffect, useMemo, useRef, ReactNode } from 'react';
import {
  DriveFile,
  DriveQuery,
  DriveStats,
  MimeCategory,
  SortField,
  UserProfile,
  DataSourceMode,
  ToastInfo
} from '../types/drive';
import { fetchFilesFromGoogleDrive, fetchGoogleUserProfile, categorizeMime } from '../services/driveService';
import { requestGoogleAccessToken, revokeGoogleAccessToken } from '../services/googleAuth';
import { useDebounce } from '../hooks/useDebounce';
import { useDriveSearch } from '../hooks/useDriveSearch';

interface DriveContextType {
  files: DriveFile[];
  filteredFiles: DriveFile[];
  stats: DriveStats;
  query: DriveQuery;
  isLoading: boolean;
  isAuthenticating: boolean;
  error: string | null;
  toast: ToastInfo | null;
  toastMessage: string | null; // Compatibilidade retroativa
  clientId: string;
  setClientId: (id: string) => void;
  isAuthenticated: boolean;
  userProfile: UserProfile | null;
  dataSourceMode: DataSourceMode;
  isConfigModalOpen: boolean;
  setIsConfigModalOpen: (open: boolean) => void;
  loginWithGoogle: (overrideClientId?: string) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  setSearchTerm: (term: string) => void;
  setCategory: (category: MimeCategory) => void;
  setSort: (field: SortField) => void;
  refreshFiles: () => Promise<void>;
  showToast: (msg: string, type?: 'success' | 'error' | 'info') => void;
}

const DriveContext = createContext<DriveContextType | undefined>(undefined);

export const DriveProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [files, setFiles] = useState<DriveFile[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isAuthenticating, setIsAuthenticating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<ToastInfo | null>(null);

  // Autenticação & Modo de Dados
  const envClientId = (import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined) || '';
  const [clientId, setClientIdState] = useState<string>(() => {
    let initial = '';
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('gdrive_client_id');
      if (stored) initial = stored;
    }
    if (!initial) initial = envClientId;
    return initial.trim().replace(/^["']|["']$/g, '').trim();
  });

  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [dataSourceMode, setDataSourceMode] = useState<DataSourceMode>('demo');
  const [isConfigModalOpen, setIsConfigModalOpen] = useState<boolean>(false);

  const [rawSearchTerm, setRawSearchTerm] = useState<string>('');
  const debouncedSearchTerm = useDebounce(rawSearchTerm, 200);

  const [query, setQuery] = useState<DriveQuery>({
    searchTerm: '',
    category: 'all',
    sortField: 'modifiedTime',
    sortOrder: 'desc'
  });

  // Atualiza query quando debounce mudar
  useEffect(() => {
    setQuery((prev) => ({ ...prev, searchTerm: debouncedSearchTerm }));
  }, [debouncedSearchTerm]);

  // Carrega arquivos iniciais (modo offline / mock por padrão)
  const loadInitialFiles = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchFilesFromGoogleDrive();
      setFiles(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar arquivos do Drive.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInitialFiles();
  }, []);

  const setClientId = (id: string) => {
    const cleanId = (id || '').trim().replace(/^["']|["']$/g, '').trim();
    setClientIdState(cleanId);
    if (typeof window !== 'undefined') {
      if (cleanId) {
        localStorage.setItem('gdrive_client_id', cleanId);
      } else {
        localStorage.removeItem('gdrive_client_id');
      }
    }
  };

  const toastTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (toastTimerRef.current) {
        clearTimeout(toastTimerRef.current);
      }
    };
  }, []);

  const showToast = (message: string, type: 'success' | 'error' | 'info' = 'success') => {
    if (toastTimerRef.current) {
      clearTimeout(toastTimerRef.current);
    }
    setToast({ message, type });
    toastTimerRef.current = setTimeout(() => {
      setToast(null);
      toastTimerRef.current = null;
    }, 3200);
  };

  const clearError = () => {
    setError(null);
  };

  // Login com Google Identity Services (suporta passar overrideClientId explicitamente para evitar stale closures)
  const loginWithGoogle = async (overrideClientId?: string) => {
    const activeId = (
      overrideClientId ||
      clientId ||
      (typeof window !== 'undefined' ? localStorage.getItem('gdrive_client_id') : '') ||
      envClientId ||
      ''
    ).trim().replace(/^["']|["']$/g, '');

    if (!activeId) {
      setIsConfigModalOpen(true);
      showToast('Por favor, configure o Google Client ID para autenticar.', 'info');
      return;
    }

    if (overrideClientId && overrideClientId.trim() !== clientId) {
      setClientId(overrideClientId.trim());
    }

    setIsAuthenticating(true);
    setIsLoading(true);
    setError(null);

    try {
      const token = await requestGoogleAccessToken(activeId);

      // Busca dados de perfil do usuário
      const profile = await fetchGoogleUserProfile(token);

      // Busca arquivos reais na Google Drive API v3
      const driveFiles = await fetchFilesFromGoogleDrive({ accessToken: token });

      // Transição atômica de estado para modo conectado:
      setAccessToken(token);
      setUserProfile(profile);
      setFiles(driveFiles);
      setIsAuthenticated(true);
      setDataSourceMode('google-drive');
      showToast(`Conectado como ${profile.name}! ${driveFiles.length} arquivos sincronizados.`, 'success');
    } catch (err: unknown) {
      // Limpeza de estado parcial em caso de falha durante a conexão
      setAccessToken(null);
      setUserProfile(null);
      setIsAuthenticated(false);
      setDataSourceMode('demo');
      const message = err instanceof Error ? err.message : 'Falha na autenticação Google.';
      setError(message);
      showToast(message, 'error');
    } finally {
      setIsAuthenticating(false);
      setIsLoading(false);
    }
  };

  // Logout e restauração de dados mockados
  const logout = async () => {
    setIsLoading(true);
    setError(null); // Limpa qualquer erro ativo para não travar a UI
    try {
      if (accessToken) {
        await revokeGoogleAccessToken(accessToken);
      }
    } catch (err) {
      console.warn('Aviso ao revogar token Google:', err);
    } finally {
      setAccessToken(null);
      setUserProfile(null);
      setIsAuthenticated(false);
      setDataSourceMode('demo');

      try {
        const mockData = await fetchFilesFromGoogleDrive();
        setFiles(mockData);
      } catch {
        // Fallback silencioso
      }
      setIsLoading(false);
      showToast('Desconectado da conta Google. Modo demonstração restaurado.', 'info');
    }
  };

  // Sincronizar arquivos manualmente
  const refreshFiles = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchFilesFromGoogleDrive({ accessToken: accessToken || undefined });
      setFiles(data);
      if (accessToken) {
        setIsAuthenticated(true);
        setDataSourceMode('google-drive');
      }
      showToast(
        isAuthenticated || Boolean(accessToken)
          ? `${data.length} arquivos sincronizados com o Google Drive!`
          : 'Catálogo de demonstração atualizado.',
        'success'
      );
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erro ao atualizar arquivos.';
      // Se for erro de autorização ou token expirado (401), desloga e reseta estado
      if (message.includes('401') || message.includes('expirada')) {
        setAccessToken(null);
        setUserProfile(null);
        setIsAuthenticated(false);
        setDataSourceMode('demo');
      }
      setError(message);
      showToast(message, 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredFiles = useDriveSearch(files, query);

  // Estatísticas computadas
  const stats = useMemo<DriveStats>(() => {
    let totalSizeBytes = 0;
    const categoryCounts: Record<MimeCategory, number> = {
      all: files.length,
      document: 0,
      spreadsheet: 0,
      pdf: 0,
      folder: 0,
      image: 0,
      code: 0
    };

    files.forEach((f) => {
      totalSizeBytes += f.sizeBytes || 0;
      const cat = categorizeMime(f.mimeType, f.name);
      if (categoryCounts[cat] !== undefined) {
        categoryCounts[cat]++;
      }
    });

    return {
      totalFiles: files.length,
      totalSizeBytes,
      categoryCounts
    };
  }, [files]);

  const setCategory = (cat: MimeCategory) => {
    setQuery((prev) => ({ ...prev, category: cat }));
  };

  const setSort = (field: SortField) => {
    setQuery((prev) => {
      if (prev.sortField === field) {
        return { ...prev, sortOrder: prev.sortOrder === 'asc' ? 'desc' : 'asc' };
      }
      return { ...prev, sortField: field, sortOrder: 'desc' };
    });
  };

  return (
    <DriveContext.Provider
      value={{
        files,
        filteredFiles,
        stats,
        query: { ...query, searchTerm: rawSearchTerm },
        isLoading,
        isAuthenticating,
        error,
        toast,
        toastMessage: toast ? toast.message : null,
        clientId,
        setClientId,
        isAuthenticated,
        userProfile,
        dataSourceMode,
        isConfigModalOpen,
        setIsConfigModalOpen,
        loginWithGoogle,
        logout,
        clearError,
        setSearchTerm: setRawSearchTerm,
        setCategory,
        setSort,
        refreshFiles,
        showToast
      }}
    >
      {children}
    </DriveContext.Provider>
  );
};

export const useDrive = (): DriveContextType => {
  const context = useContext(DriveContext);
  if (!context) {
    throw new Error('useDrive deve ser utilizado dentro de um DriveProvider');
  }
  return context;
};
