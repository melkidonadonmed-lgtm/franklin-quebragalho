import '../types/google';

const GIS_SCRIPT_URL = 'https://accounts.google.com/gsi/client';

/**
 * Verifica se a API do Google Identity Services já está carregada no objeto global window.
 */
export function isGisLoaded(): boolean {
  return typeof window !== 'undefined' && Boolean(window.google?.accounts?.oauth2);
}

let gisPromise: Promise<void> | null = null;

/**
 * Garante que o script oficial do Google Identity Services seja carregado no navegador de forma idempotente.
 */
export function loadGisScript(): Promise<void> {
  if (isGisLoaded()) {
    return Promise.resolve();
  }

  if (gisPromise) {
    return gisPromise;
  }

  gisPromise = new Promise<void>((resolve, reject) => {
    if (typeof window === 'undefined') {
      reject(new Error('Google Identity Services só pode ser carregado no ambiente de navegador.'));
      return;
    }

    const existingScript = document.querySelector<HTMLScriptElement>(`script[src="${GIS_SCRIPT_URL}"]`);
    if (existingScript) {
      if (isGisLoaded()) {
        resolve();
        return;
      }
      let attempts = 0;
      const interval = setInterval(() => {
        attempts++;
        if (isGisLoaded()) {
          clearInterval(interval);
          resolve();
        } else if (attempts >= 40) {
          clearInterval(interval);
          reject(new Error('Tempo limite excedido ao inicializar o Google Identity Services. Verifique sua conexão com a internet ou bloqueadores de scripts.'));
        }
      }, 100);
      return;
    }

    const script = document.createElement('script');
    script.src = GIS_SCRIPT_URL;
    script.async = true;
    script.defer = true;
    script.onload = () => {
      let attempts = 0;
      const interval = setInterval(() => {
        attempts++;
        if (isGisLoaded()) {
          clearInterval(interval);
          resolve();
        } else if (attempts >= 30) {
          clearInterval(interval);
          reject(new Error('Google Identity Services carregado, mas objeto oauth2 não encontrado.'));
        }
      }, 100);
    };
    script.onerror = () => {
      reject(new Error('Falha ao carregar o script do Google Identity Services. Verifique sua conexão com a internet.'));
    };

    document.head.appendChild(script);
  }).finally(() => {
    if (!isGisLoaded()) {
      gisPromise = null;
    }
  });

  return gisPromise;
}

/**
 * Dispara o popup de consentimento OAuth 2.0 via Google Identity Services
 * solicitando acesso de leitura ao Google Drive (drive.readonly).
 */
export async function requestGoogleAccessToken(clientId: string): Promise<string> {
  const trimmedId = (clientId || '').trim().replace(/^["']|["']$/g, '').trim();
  if (!trimmedId) {
    throw new Error('Google Client ID não configurado.');
  }

  await loadGisScript();

  if (!window.google?.accounts?.oauth2) {
    throw new Error('Google Identity Services não está disponível.');
  }

  return new Promise<string>((resolve, reject) => {
    try {
      const tokenClient = window.google!.accounts.oauth2.initTokenClient({
        client_id: trimmedId,
        scope: 'https://www.googleapis.com/auth/drive.readonly',
        callback: (response) => {
          if (response.error) {
            let desc = response.error_description || response.error;
            if (response.error === 'access_denied' && !response.error_description) {
              desc = 'O usuário não concedeu permissão de leitura aos arquivos do Drive.';
            }
            reject(new Error(`Autorização Google recusada: ${desc}`));
          } else if (response.access_token) {
            resolve(response.access_token);
          } else {
            reject(new Error('Nenhum token de acesso foi retornado pela autenticação Google.'));
          }
        },
        error_callback: (error) => {
          let detail = error.message || error.type;
          if (error.type === 'popup_closed' && !error.message) {
            detail = 'O popup de autenticação foi fechado antes de concluir o login.';
          } else if (error.type === 'popup_failed_to_open' && !error.message) {
            detail = 'O navegador bloqueou a abertura da janela popup. Permita popups para este site.';
          } else if (!detail) {
            detail = 'Popup de login fechado ou bloqueado.';
          }
          reject(new Error(`Falha no popup de login Google: ${detail}`));
        }
      });

      tokenClient.requestAccessToken({ prompt: 'consent' });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Falha inesperada ao inicializar login Google.';
      reject(new Error(message));
    }
  });
}

/**
 * Revoga o token de acesso no Google Identity Services ao desconectar,
 * garantindo resolução via timeout mesmo se a API do Google não invocar o callback.
 */
export async function revokeGoogleAccessToken(accessToken: string, timeoutMs: number = 2000): Promise<void> {
  if (!accessToken) return;
  return new Promise<void>((resolve) => {
    const timer = setTimeout(() => {
      resolve();
    }, timeoutMs);

    if (typeof window !== 'undefined' && window.google?.accounts?.oauth2?.revoke) {
      try {
        window.google.accounts.oauth2.revoke(accessToken, () => {
          clearTimeout(timer);
          resolve();
        });
        return;
      } catch {
        clearTimeout(timer);
        resolve();
      }
    }
    clearTimeout(timer);
    resolve();
  });
}
