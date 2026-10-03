import { DriveFile, MimeCategory, UserProfile } from '../types/drive';

export const MOCK_DRIVE_FILES: DriveFile[] = [
  {
    id: '1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV',
    name: '01_Receita_Especial_Amoxicilina_Clavulanato.gdoc',
    mimeType: 'application/vnd.google-apps.document',
    sizeBytes: 195,
    modifiedTime: '2026-09-27T08:15:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://docs.google.com/document/d/1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV',
    folderCategory: '01_Modelos_Rapidos/02_Receitas_Especiais',
    isStarred: true
  },
  {
    id: '2bC3dE4fG5hI6jK7lM8nO9pQ0rS1tU2vW',
    name: 'Atestado_Medico_Comparecimento_UBS.gdoc',
    mimeType: 'application/vnd.google-apps.document',
    sizeBytes: 195,
    modifiedTime: '2026-09-26T14:30:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://docs.google.com/document/d/2bC3dE4fG5hI6jK7lM8nO9pQ0rS1tU2vW',
    folderCategory: '01_Modelos_Rapidos/03_Atestados',
    isStarred: true
  },
  {
    id: '3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX',
    name: 'Protocolo_Reposicao_Ferro_Pediatria_2026.pdf',
    mimeType: 'application/pdf',
    sizeBytes: 2450000,
    modifiedTime: '2026-09-25T11:20:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX',
    folderCategory: '02_Protocolos_e_Medicamentos/01_Pediatria',
    isStarred: true
  },
  {
    id: '4dE5fG6hI7jK8lM9nO0pQ1rS2tU3vW4xY',
    name: 'Passometro_Neonatal_Sala_de_Parto.pdf',
    mimeType: 'application/pdf',
    sizeBytes: 812000,
    modifiedTime: '2026-09-24T09:10:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/4dE5fG6hI7jK8lM9nO0pQ1rS2tU3vW4xY',
    folderCategory: '02_Protocolos_e_Medicamentos/01_Pediatria',
    isStarred: false
  },
  {
    id: '5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ',
    name: 'Abordagem_Dor_Toracica_Emergencia_IAM.pdf',
    mimeType: 'application/pdf',
    sizeBytes: 1540000,
    modifiedTime: '2026-09-22T17:45:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ',
    folderCategory: '02_Protocolos_e_Medicamentos/03_Cardiologia_e_Emergencia',
    isStarred: false
  },
  {
    id: '6fG7hI8jK9lM0nO1pQ2rS3tU4vW5xY6zA',
    name: 'Tabela_Doses_Pediatricas_Gotas_Xarope.gsheet',
    mimeType: 'application/vnd.google-apps.spreadsheet',
    sizeBytes: 195,
    modifiedTime: '2026-09-21T18:00:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://docs.google.com/spreadsheets/d/6fG7hI8jK9lM0nO1pQ2rS3tU4vW5xY6zA',
    folderCategory: '02_Protocolos_e_Medicamentos/01_Pediatria',
    isStarred: true
  },
  {
    id: '7gH8iJ9kL0mN1oP2qR3sT4uV5wX6yZ7aB',
    name: 'Logo_Oficial_UBS_Osvaldo_Piana_Alta_Resolucao.png',
    mimeType: 'image/png',
    sizeBytes: 1240000,
    modifiedTime: '2026-09-20T10:15:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/7gH8iJ9kL0mN1oP2qR3sT4uV5wX6yZ7aB',
    folderCategory: '01_Modelos_Rapidos/06_Logos',
    isStarred: false
  },
  {
    id: '8hI9jK0lM1nO2pQ3rS4tU5vW6xY7zA8bC',
    name: 'scoreboard-app-build-neurocirurgia-pwa.zip',
    mimeType: 'application/zip',
    sizeBytes: 328575,
    modifiedTime: '2026-09-22T21:00:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/8hI9jK0lM1nO2pQ3rS4tU5vW6xY7zA8bC',
    folderCategory: '04_Projetos_e_Desenvolvimento/01_App_Scoreboard',
    isStarred: false
  },
  {
    id: '9iJ0kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD',
    name: 'App_Calculadoras_Medicas_Modelagem_Dados.pdf',
    mimeType: 'application/pdf',
    sizeBytes: 181625,
    modifiedTime: '2026-09-22T19:30:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/9iJ0kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD',
    folderCategory: '04_Projetos_e_Desenvolvimento/01_App_Scoreboard',
    isStarred: false
  },
  {
    id: '0jK1lL2mN3oP4qR5sT6uV7wX8yZ9aB0cE',
    name: 'arquiteto_de_conteudo_e_solucoes.md',
    mimeType: 'text/markdown',
    sizeBytes: 5585,
    modifiedTime: '2026-09-15T22:20:00Z',
    owners: ['Melki Donadon'],
    webViewLink: 'https://drive.google.com/file/d/0jK1lL2mN3oP4qR5sT6uV7wX8yZ9aB0cE',
    folderCategory: '05_IA_Agentes_e_Prompts/01_Antigravity_e_Skills',
    isStarred: true
  }
];

export function categorizeMime(mime?: string, name?: string): MimeCategory {
  const m = (mime || '').toLowerCase();
  const n = (name || '').toLowerCase();

  if (m.includes('folder')) return 'folder';
  if (m.includes('pdf') || n.endsWith('.pdf')) return 'pdf';
  if (
    m.includes('spreadsheet') ||
    m.includes('sheet') ||
    n.endsWith('.xlsx') ||
    n.endsWith('.xls') ||
    n.endsWith('.csv') ||
    n.endsWith('.gsheet')
  ) return 'spreadsheet';
  if (
    m.includes('document') ||
    m.includes('word') ||
    m.includes('presentation') ||
    m.includes('slide') ||
    m === 'text/plain' ||
    n.endsWith('.docx') ||
    n.endsWith('.doc') ||
    n.endsWith('.gdoc') ||
    n.endsWith('.ppt') ||
    n.endsWith('.pptx') ||
    n.endsWith('.gslides') ||
    n.endsWith('.txt') ||
    n.endsWith('.rtf')
  ) return 'document';
  if (
    m.includes('image') ||
    n.endsWith('.jpg') ||
    n.endsWith('.png') ||
    n.endsWith('.jpeg') ||
    n.endsWith('.webp') ||
    n.endsWith('.gif') ||
    n.endsWith('.svg')
  ) return 'image';
  if (
    m.includes('json') ||
    m.includes('javascript') ||
    m.includes('typescript') ||
    m.includes('markdown') ||
    m.includes('html') ||
    m.includes('xml') ||
    m.includes('css') ||
    m.includes('python') ||
    n.endsWith('.ts') ||
    n.endsWith('.tsx') ||
    n.endsWith('.js') ||
    n.endsWith('.jsx') ||
    n.endsWith('.md') ||
    n.endsWith('.py') ||
    n.endsWith('.html') ||
    n.endsWith('.css') ||
    n.endsWith('.yaml') ||
    n.endsWith('.yml') ||
    n.endsWith('.json') ||
    n.endsWith('.sql') ||
    n.endsWith('.sh')
  ) return 'code';
  return 'document';
}

export function formatFileSize(bytes?: number): string {
  if (bytes === undefined || bytes === null || Number.isNaN(bytes) || bytes === 0) return '0 B';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

export function formatDate(isoString?: string): string {
  if (!isoString || typeof isoString !== 'string' || !isoString.trim()) {
    return '—';
  }
  try {
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) {
      return isoString;
    }
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  } catch {
    return isoString;
  }
}

export interface DriveApiConfig {
  apiKey?: string;
  accessToken?: string;
  pageSize?: number;
  maxResults?: number;
}

interface RawDriveFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  modifiedTime?: string;
  owners?: Array<{ displayName?: string }>;
  webViewLink?: string;
  starred?: boolean;
}

/**
 * Busca o perfil do usuário conectado via Google Drive API v3 (about.get)
 * com fallback para o endpoint userinfo.
 */
export async function fetchGoogleUserProfile(accessToken: string): Promise<UserProfile> {
  // 1. Tenta obter o perfil através do endpoint about da Drive API v3 (coberto pelo escopo drive.readonly)
  try {
    const response = await fetch('https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress,photoLink)', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      if (data?.user) {
        return {
          name: data.user.displayName || data.user.emailAddress || 'Usuário Google',
          email: data.user.emailAddress,
          avatarUrl: data.user.photoLink
        };
      }
    }
  } catch (err) {
    console.warn('Não foi possível obter dados do perfil via Drive About API:', err);
  }

  // 2. Fallback para userinfo API caso o token possua escopo de perfil
  try {
    const res = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    if (res.ok) {
      const data = await res.json();
      return {
        name: data.name || data.email || 'Usuário Google',
        email: data.email,
        avatarUrl: data.picture
      };
    }
  } catch {
    // Ignora e retorna fallback amigável
  }

  return {
    name: 'Usuário Google'
  };
}

/**
 * Consulta arquivos do Google Drive API v3 utilizando Bearer Token ou Chave de API.
 * Em ausência de credenciais, retorna dados mockados de demonstração.
 */
export async function fetchFilesFromGoogleDrive(config?: DriveApiConfig): Promise<DriveFile[]> {
  if (!config?.accessToken && !config?.apiKey) {
    // Retorna mock instantâneo realista quando em modo offline/demonstração
    return new Promise((resolve) => {
      setTimeout(() => resolve([...MOCK_DRIVE_FILES]), 200);
    });
  }

  const allRawFiles: RawDriveFile[] = [];
  let pageToken: string | undefined = undefined;
  const maxResults = config?.maxResults || 500;
  const pageSize = Math.min(config?.pageSize || 100, 1000);

  const headers: HeadersInit = {};
  if (config.accessToken) {
    headers['Authorization'] = `Bearer ${config.accessToken}`;
  }

  do {
    const endpoint = new URL('https://www.googleapis.com/drive/v3/files');
    endpoint.searchParams.append('pageSize', String(pageSize));
    endpoint.searchParams.append('fields', 'nextPageToken, files(id, name, mimeType, size, modifiedTime, owners(displayName), webViewLink, starred)');
    endpoint.searchParams.append('q', 'trashed = false');
    if (pageToken) {
      endpoint.searchParams.append('pageToken', pageToken);
    }
    if (config.apiKey) {
      endpoint.searchParams.append('key', config.apiKey);
    }

    const response = await fetch(endpoint.toString(), { headers });
    if (!response.ok) {
      let errorMessage = `Falha na requisição à Google Drive API v3 (${response.status} ${response.statusText})`;
      try {
        const errBody = await response.json();
        if (errBody?.error?.message) {
          errorMessage = errBody.error.message;
        }
      } catch {
        // Ignora erro no parse de JSON
      }
      if (response.status === 401) {
        errorMessage = `Sessão expirada ou não autorizada (${response.status}): ${errorMessage}`;
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    const pageFiles: RawDriveFile[] = Array.isArray(data.files) ? data.files : [];
    allRawFiles.push(...pageFiles);

    if (data.nextPageToken && allRawFiles.length < maxResults) {
      pageToken = data.nextPageToken;
    } else {
      pageToken = undefined;
    }
  } while (pageToken);

  return allRawFiles.map((f) => {
    const parsedSize = f.size ? parseInt(f.size, 10) : undefined;
    return {
      id: f.id,
      name: f.name || 'Arquivo sem nome',
      mimeType: f.mimeType || 'application/octet-stream',
      sizeBytes: (parsedSize !== undefined && !Number.isNaN(parsedSize)) ? parsedSize : undefined,
      modifiedTime: f.modifiedTime || new Date().toISOString(),
      owners: (Array.isArray(f.owners) && f.owners.length > 0)
        ? f.owners.map((o) => o?.displayName || 'Desconhecido')
        : ['Meu Drive'],
      webViewLink: f.webViewLink || (f.id ? `https://drive.google.com/file/d/${f.id}/view` : undefined),
      folderCategory: f.mimeType === 'application/vnd.google-apps.folder' ? 'Pasta' : 'Google Drive',
      isStarred: Boolean(f.starred)
    };
  });
}

