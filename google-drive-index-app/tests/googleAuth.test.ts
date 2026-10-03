import test from 'node:test';
import assert from 'node:assert';
import {
  isGisLoaded,
  requestGoogleAccessToken,
  revokeGoogleAccessToken
} from '../src/services/googleAuth';

test('requestGoogleAccessToken throws error when Client ID is empty', async () => {
  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('');
    },
    (err: Error) => {
      assert.strictEqual(err.message, 'Google Client ID não configurado.');
      return true;
    }
  );

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('   ');
    },
    (err: Error) => {
      assert.strictEqual(err.message, 'Google Client ID não configurado.');
      return true;
    }
  );
});

test('requestGoogleAccessToken initializes GIS token client and receives token', async () => {
  let initializedConfig: Record<string, unknown> = {};
  let requestedWithPrompt: Record<string, unknown> = {};

  // Mock global window and Google Identity Services
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: (res: { access_token?: string; error?: string }) => void;
            error_callback?: (err: { message?: string }) => void;
          }) => {
            initializedConfig = config;
            return {
              requestAccessToken: (override?: { prompt?: string }) => {
                requestedWithPrompt = override || {};
                // Simula retorno bem-sucedido do token de acesso
                config.callback({ access_token: 'mock-gis-access-token-12345' });
              }
            };
          },
          revoke: (_token: string, callback?: () => void) => {
            if (callback) callback();
          }
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  assert.strictEqual(isGisLoaded(), true);

  const token = await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
  assert.strictEqual(token, 'mock-gis-access-token-12345');
  assert.strictEqual(initializedConfig.client_id, 'my-client-id.apps.googleusercontent.com');
  assert.strictEqual(initializedConfig.scope, 'https://www.googleapis.com/auth/drive.readonly');
  assert.strictEqual(requestedWithPrompt.prompt, 'consent');
});

test('requestGoogleAccessToken handles user denial or error in OAuth popup', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: (res: { access_token?: string; error?: string; error_description?: string }) => void;
          }) => {
            return {
              requestAccessToken: () => {
                config.callback({
                  error: 'access_denied',
                  error_description: 'O usuário não concedeu permissão de leitura.'
                });
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('O usuário não concedeu permissão de leitura'));
      return true;
    }
  );
});

test('requestGoogleAccessToken handles error_callback when popup is closed', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: () => void;
            error_callback?: (err: { message?: string }) => void;
          }) => {
            return {
              requestAccessToken: () => {
                if (config.error_callback) {
                  config.error_callback({ message: 'popup_closed_by_user' });
                }
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('popup_closed_by_user'));
      return true;
    }
  );
});

test('revokeGoogleAccessToken invokes GIS revoke method', async () => {
  let revokedToken = '';
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          revoke: (token: string, callback?: () => void) => {
            revokedToken = token;
            if (callback) callback();
          }
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await revokeGoogleAccessToken('token-to-revoke');
  assert.strictEqual(revokedToken, 'token-to-revoke');
});

test('requestGoogleAccessToken formats popup_closed into user-friendly message', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: () => void;
            error_callback?: (err: { type: string; message?: string }) => void;
          }) => {
            return {
              requestAccessToken: () => {
                if (config.error_callback) {
                  // Simula evento nativo do GIS onde message não vem preenchida
                  config.error_callback({ type: 'popup_closed' });
                }
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('O popup de autenticação foi fechado'));
      return true;
    }
  );
});

test('requestGoogleAccessToken formats popup_failed_to_open into user-friendly message', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: {
            client_id: string;
            scope: string;
            callback: () => void;
            error_callback?: (err: { type: string; message?: string }) => void;
          }) => {
            return {
              requestAccessToken: () => {
                if (config.error_callback) {
                  config.error_callback({ type: 'popup_failed_to_open' });
                }
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('bloqueou a abertura da janela popup'));
      return true;
    }
  );
});

test('revokeGoogleAccessToken resolves without hanging when callback is never called', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          revoke: (_token: string, _callback?: () => void) => {
            // Intencionalmente NÃO chama o callback para simular falha de rede/API
          }
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  const start = Date.now();
  await revokeGoogleAccessToken('unresponsive-token', 150);
  const duration = Date.now() - start;
  // Deve ter resolvido após o timeout configurado de 150ms sem travar
  assert.ok(duration >= 140 && duration < 800, `Duração esperada em torno de 150ms, foi ${duration}ms`);
});

test('requestGoogleAccessToken sanitizes surrounding double and single quotes from client ID', async () => {
  let passedClientId = '';
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: { client_id: string; callback: (res: { access_token?: string }) => void }) => {
            passedClientId = config.client_id;
            return {
              requestAccessToken: () => {
                config.callback({ access_token: 'valid-token' });
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await requestGoogleAccessToken('  "client-id-with-double-quotes.apps.googleusercontent.com"  ');
  assert.strictEqual(passedClientId, 'client-id-with-double-quotes.apps.googleusercontent.com');

  await requestGoogleAccessToken("  'client-id-with-single-quotes.apps.googleusercontent.com'  ");
  assert.strictEqual(passedClientId, 'client-id-with-single-quotes.apps.googleusercontent.com');
});

test('requestGoogleAccessToken rejects empty quotes as empty client ID', async () => {
  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('""');
    },
    (err: Error) => {
      assert.strictEqual(err.message, 'Google Client ID não configurado.');
      return true;
    }
  );

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken("''");
    },
    (err: Error) => {
      assert.strictEqual(err.message, 'Google Client ID não configurado.');
      return true;
    }
  );
});

test('requestGoogleAccessToken formats access_denied without error_description into helpful message', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: { callback: (res: { error: string }) => void }) => {
            return {
              requestAccessToken: () => {
                config.callback({ error: 'access_denied' });
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('O usuário não concedeu permissão de leitura'));
      return true;
    }
  );
});

test('requestGoogleAccessToken rejects when response has neither token nor error', async () => {
  const mockWindow = {
    google: {
      accounts: {
        oauth2: {
          initTokenClient: (config: { callback: (res: Record<string, unknown>) => void }) => {
            return {
              requestAccessToken: () => {
                config.callback({});
              }
            };
          },
          revoke: () => {}
        }
      }
    }
  };

  (globalThis as unknown as { window: unknown }).window = mockWindow;

  await assert.rejects(
    async () => {
      await requestGoogleAccessToken('my-client-id.apps.googleusercontent.com');
    },
    (err: Error) => {
      assert.ok(err.message.includes('Nenhum token de acesso foi retornado'));
      return true;
    }
  );
});

