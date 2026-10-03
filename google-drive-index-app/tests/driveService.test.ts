import test from 'node:test';
import assert from 'node:assert';
import {
  categorizeMime,
  formatFileSize,
  formatDate,
  MOCK_DRIVE_FILES,
  fetchFilesFromGoogleDrive,
  fetchGoogleUserProfile
} from '../src/services/driveService';

test('categorizeMime correctly classifies MIME types and extensions', () => {
  assert.strictEqual(categorizeMime('application/vnd.google-apps.folder'), 'folder');
  assert.strictEqual(categorizeMime('application/pdf', 'relatorio.pdf'), 'pdf');
  assert.strictEqual(categorizeMime('application/vnd.google-apps.spreadsheet'), 'spreadsheet');
  assert.strictEqual(categorizeMime('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'tabela.xlsx'), 'spreadsheet');
  assert.strictEqual(categorizeMime('application/vnd.google-apps.document'), 'document');
  assert.strictEqual(categorizeMime('application/msword', 'doc.docx'), 'document');
  assert.strictEqual(categorizeMime('image/png', 'foto.png'), 'image');
  assert.strictEqual(categorizeMime('image/jpeg', 'foto.jpg'), 'image');
  assert.strictEqual(categorizeMime('text/markdown', 'README.md'), 'code');
  assert.strictEqual(categorizeMime('application/json', 'package.json'), 'code');
  assert.strictEqual(categorizeMime('application/octet-stream', 'arquivo.bin'), 'document');
  assert.strictEqual(categorizeMime(undefined), 'document');
  assert.strictEqual(categorizeMime(''), 'document');
});

test('formatFileSize formats byte quantities into human-readable strings', () => {
  assert.strictEqual(formatFileSize(undefined), '0 B');
  assert.strictEqual(formatFileSize(0), '0 B');
  assert.strictEqual(formatFileSize(512), '512 B');
  assert.strictEqual(formatFileSize(1024), '1.0 KB');
  assert.strictEqual(formatFileSize(1536), '1.5 KB');
  assert.strictEqual(formatFileSize(1024 * 1024), '1.0 MB');
  assert.strictEqual(formatFileSize(2.5 * 1024 * 1024), '2.5 MB');
  assert.strictEqual(formatFileSize(1024 * 1024 * 1024), '1.00 GB');
});

test('formatDate formats ISO dates or returns fallback', () => {
  const formatted = formatDate('2026-09-27T08:15:00Z');
  assert.ok(formatted.length > 5, 'Data deve ser formatada com sucesso');
  // Formato inválido deve retornar a string original sem quebrar
  const fallback = formatDate('data-invalida');
  assert.strictEqual(fallback, 'data-invalida');
  assert.strictEqual(formatDate(''), '—');
  assert.strictEqual(formatDate(undefined), '—');
});

test('MOCK_DRIVE_FILES has valid schema and mock medical files', () => {
  assert.strictEqual(MOCK_DRIVE_FILES.length, 10);
  for (const file of MOCK_DRIVE_FILES) {
    assert.ok(file.id && typeof file.id === 'string');
    assert.ok(file.name && typeof file.name === 'string');
    assert.ok(file.mimeType && typeof file.mimeType === 'string');
    assert.ok(Array.isArray(file.owners));
    assert.ok(file.modifiedTime);
  }
});

test('fetchFilesFromGoogleDrive returns mock files when no credentials provided', async () => {
  const files = await fetchFilesFromGoogleDrive();
  assert.strictEqual(files.length, 10);
  assert.strictEqual(files[0].id, MOCK_DRIVE_FILES[0].id);
});

test('fetchFilesFromGoogleDrive connects to Google Drive API v3 with Bearer token', async () => {
  const originalFetch = globalThis.fetch;
  let interceptedUrl = '';
  let interceptedHeaders: Record<string, string> = {};

  try {
    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      interceptedUrl = input.toString();
      interceptedHeaders = (init?.headers as Record<string, string>) || {};
      return {
        ok: true,
        status: 200,
        statusText: 'OK',
        json: async () => ({
          files: [
            {
              id: 'real-drive-file-123',
              name: 'Prontuario_Paciente_01.pdf',
              mimeType: 'application/pdf',
              size: '409600',
              modifiedTime: '2026-09-27T12:00:00Z',
              owners: [{ displayName: 'Dr. Melki' }],
              webViewLink: 'https://drive.google.com/file/d/real-drive-file-123',
              starred: true
            },
            {
              id: 'folder-456',
              name: 'Internato Medico 2026',
              mimeType: 'application/vnd.google-apps.folder',
              modifiedTime: '2026-09-20T10:00:00Z',
              owners: []
            }
          ]
        })
      } as Response;
    }) as typeof fetch;

    const files = await fetchFilesFromGoogleDrive({ accessToken: 'test-oauth-bearer-token' });

    assert.ok(interceptedUrl.startsWith('https://www.googleapis.com/drive/v3/files'));
    assert.strictEqual(interceptedHeaders['Authorization'], 'Bearer test-oauth-bearer-token');
    assert.strictEqual(files.length, 2);

    // Primeiro arquivo (PDF)
    assert.strictEqual(files[0].id, 'real-drive-file-123');
    assert.strictEqual(files[0].name, 'Prontuario_Paciente_01.pdf');
    assert.strictEqual(files[0].sizeBytes, 409600);
    assert.strictEqual(files[0].owners[0], 'Dr. Melki');
    assert.strictEqual(files[0].folderCategory, 'Google Drive');
    assert.strictEqual(files[0].isStarred, true);

    // Segundo arquivo (Pasta)
    assert.strictEqual(files[1].id, 'folder-456');
    assert.strictEqual(files[1].folderCategory, 'Pasta');
    assert.strictEqual(files[1].owners[0], 'Meu Drive');
    assert.strictEqual(files[1].sizeBytes, undefined);
    assert.strictEqual(files[1].webViewLink, 'https://drive.google.com/file/d/folder-456/view');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchFilesFromGoogleDrive connects to Google Drive API v3 with apiKey', async () => {
  const originalFetch = globalThis.fetch;
  let interceptedUrl = '';

  try {
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      interceptedUrl = input.toString();
      return {
        ok: true,
        status: 200,
        json: async () => ({ files: [] })
      } as Response;
    }) as typeof fetch;

    const files = await fetchFilesFromGoogleDrive({ apiKey: 'my-custom-api-key' });
    assert.strictEqual(files.length, 0);
    assert.ok(interceptedUrl.includes('key=my-custom-api-key'));
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchFilesFromGoogleDrive handles API errors and throws formatted error message', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = (async () => {
      return {
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: async () => ({
          error: {
            message: 'Token de acesso expirado ou inválido.'
          }
        })
      } as Response;
    }) as typeof fetch;

    await assert.rejects(
      async () => {
        await fetchFilesFromGoogleDrive({ accessToken: 'expired-token' });
      },
      (err: Error) => {
        assert.ok(err.message.includes('Token de acesso expirado ou inválido'));
        return true;
      }
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchGoogleUserProfile extracts user profile from Drive about endpoint', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      if (input.toString().includes('about')) {
        return {
          ok: true,
          json: async () => ({
            user: {
              displayName: 'Dr. Melki Donadon',
              emailAddress: 'melki@exemplo.com',
              photoLink: 'https://lh3.googleusercontent.com/avatar.jpg'
            }
          })
        } as Response;
      }
      return { ok: false } as Response;
    }) as typeof fetch;

    const profile = await fetchGoogleUserProfile('valid-token');
    assert.strictEqual(profile.name, 'Dr. Melki Donadon');
    assert.strictEqual(profile.email, 'melki@exemplo.com');
    assert.strictEqual(profile.avatarUrl, 'https://lh3.googleusercontent.com/avatar.jpg');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchGoogleUserProfile falls back to userinfo endpoint when about endpoint fails', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      const url = input.toString();
      if (url.includes('about')) {
        return { ok: false, status: 403 } as Response;
      }
      if (url.includes('userinfo')) {
        return {
          ok: true,
          json: async () => ({
            name: 'Dr. Melki Via UserInfo',
            email: 'melki.userinfo@exemplo.com',
            picture: 'https://lh3.googleusercontent.com/userinfo-pic.jpg'
          })
        } as Response;
      }
      return { ok: false } as Response;
    }) as typeof fetch;

    const profile = await fetchGoogleUserProfile('valid-token');
    assert.strictEqual(profile.name, 'Dr. Melki Via UserInfo');
    assert.strictEqual(profile.email, 'melki.userinfo@exemplo.com');
    assert.strictEqual(profile.avatarUrl, 'https://lh3.googleusercontent.com/userinfo-pic.jpg');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchGoogleUserProfile falls back gracefully when API returns error', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = (async () => {
      return { ok: false, status: 500 } as Response;
    }) as typeof fetch;

    const profile = await fetchGoogleUserProfile('invalid-token');
    assert.strictEqual(profile.name, 'Usuário Google');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchFilesFromGoogleDrive correctly paginates with nextPageToken across multiple pages', async () => {
  const originalFetch = globalThis.fetch;
  const requests: string[] = [];

  try {
    globalThis.fetch = (async (input: RequestInfo | URL) => {
      const url = input.toString();
      requests.push(url);

      if (!url.includes('pageToken')) {
        // Primeira página
        return {
          ok: true,
          status: 200,
          json: async () => ({
            nextPageToken: 'token-page-2',
            files: [
              { id: 'file-p1-1', name: 'Arquivo 1 Pag 1.pdf', mimeType: 'application/pdf', size: '1000' },
              { id: 'file-p1-2', name: 'Arquivo 2 Pag 1.pdf', mimeType: 'application/pdf', size: '2000' }
            ]
          })
        } as Response;
      } else {
        // Segunda página (sem nextPageToken adicional)
        return {
          ok: true,
          status: 200,
          json: async () => ({
            files: [
              { id: 'file-p2-1', name: 'Arquivo 1 Pag 2.docx', mimeType: 'application/vnd.google-apps.document', size: '3000' }
            ]
          })
        } as Response;
      }
    }) as typeof fetch;

    const files = await fetchFilesFromGoogleDrive({ accessToken: 'valid-token' });
    assert.strictEqual(files.length, 3);
    assert.strictEqual(files[0].id, 'file-p1-1');
    assert.strictEqual(files[1].id, 'file-p1-2');
    assert.strictEqual(files[2].id, 'file-p2-1');
    assert.strictEqual(requests.length, 2);
    assert.ok(requests[1].includes('pageToken=token-page-2'));
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('fetchFilesFromGoogleDrive respects maxResults limit during multi-page pagination', async () => {
  const originalFetch = globalThis.fetch;
  let pageCount = 0;

  try {
    globalThis.fetch = (async () => {
      pageCount++;
      return {
        ok: true,
        status: 200,
        json: async () => ({
          nextPageToken: `token-page-${pageCount + 1}`,
          files: [
            { id: `file-${pageCount}-1`, name: `Arquivo ${pageCount}.pdf`, mimeType: 'application/pdf', size: '1000' },
            { id: `file-${pageCount}-2`, name: `Arquivo ${pageCount}b.pdf`, mimeType: 'application/pdf', size: '1000' }
          ]
        })
      } as Response;
    }) as typeof fetch;

    // Configura maxResults = 2 para interromper a busca após atingir o limite
    const files = await fetchFilesFromGoogleDrive({ accessToken: 'valid-token', maxResults: 2 });
    assert.strictEqual(files.length, 2);
    assert.strictEqual(pageCount, 1); // Não buscou a segunda página pois o limite foi atingido
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test('categorizeMime properly classifies office presentation, modern image, and code extensions', () => {
  assert.strictEqual(categorizeMime('application/vnd.google-apps.presentation', 'slides.gslides'), 'document');
  assert.strictEqual(categorizeMime('application/vnd.ms-powerpoint', 'apresentacao.ppt'), 'document');
  assert.strictEqual(categorizeMime('application/vnd.openxmlformats-officedocument.presentationml.presentation', 'aula.pptx'), 'document');
  assert.strictEqual(categorizeMime('application/octet-stream', 'tabela.xls'), 'spreadsheet');
  assert.strictEqual(categorizeMime('application/octet-stream', 'dados.gsheet'), 'spreadsheet');
  assert.strictEqual(categorizeMime('image/webp', 'foto.webp'), 'image');
  assert.strictEqual(categorizeMime('image/svg+xml', 'logo.svg'), 'image');
  assert.strictEqual(categorizeMime('text/x-python', 'script.py'), 'code');
  assert.strictEqual(categorizeMime('text/html', 'index.html'), 'code');
  assert.strictEqual(categorizeMime('text/css', 'styles.css'), 'code');
});

test('formatFileSize handles NaN defensively', () => {
  assert.strictEqual(formatFileSize(NaN), '0 B');
});

test('categorizeMime correctly classifies text/plain as document and source files as code', () => {
  assert.strictEqual(categorizeMime('text/plain', 'anotacoes.txt'), 'document');
  assert.strictEqual(categorizeMime('text/plain'), 'document');
  assert.strictEqual(categorizeMime('application/json', 'config.json'), 'code');
  assert.strictEqual(categorizeMime('application/sql', 'schema.sql'), 'code');
  assert.strictEqual(categorizeMime('application/x-sh', 'script.sh'), 'code');
});

test('fetchFilesFromGoogleDrive safely handles malformed owners and non-numeric size', async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = (async () => {
      return {
        ok: true,
        status: 200,
        json: async () => ({
          files: [
            {
              id: 'file-malformed-1',
              name: 'Arquivo Incomum',
              mimeType: 'application/pdf',
              size: 'not-a-number',
              owners: [null, { displayName: '' }, { displayName: 'Dr. Teste' }]
            }
          ]
        })
      } as Response;
    }) as typeof fetch;

    const files = await fetchFilesFromGoogleDrive({ accessToken: 'test-token' });
    assert.strictEqual(files.length, 1);
    assert.strictEqual(files[0].sizeBytes, undefined); // Deve ignorar NaN e ficar undefined
    assert.strictEqual(files[0].owners[0], 'Desconhecido');
    assert.strictEqual(files[0].owners[1], 'Desconhecido');
    assert.strictEqual(files[0].owners[2], 'Dr. Teste');
  } finally {
    globalThis.fetch = originalFetch;
  }
});

