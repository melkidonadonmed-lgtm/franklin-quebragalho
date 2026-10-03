export interface GoogleTokenResponse {
  access_token: string;
  expires_in?: number;
  scope?: string;
  token_type?: string;
  error?: string;
  error_description?: string;
  error_uri?: string;
}

export interface GoogleAuthError {
  type: string;
  message?: string;
}

export interface TokenClientConfig {
  client_id: string;
  scope: string;
  callback?: (response: GoogleTokenResponse) => void;
  error_callback?: (error: GoogleAuthError) => void;
  prompt?: string;
}

export interface TokenClient {
  requestAccessToken: (overrideConfig?: { prompt?: string }) => void;
}

export interface GoogleAccountsOAuth2 {
  initTokenClient: (config: TokenClientConfig) => TokenClient;
  revoke: (accessToken: string, callback?: () => void) => void;
}

export interface GoogleAccounts {
  oauth2: GoogleAccountsOAuth2;
}

declare global {
  interface Window {
    google?: {
      accounts: GoogleAccounts;
    };
  }
}
