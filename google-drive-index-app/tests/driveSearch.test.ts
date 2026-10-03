import test from 'node:test';
import assert from 'node:assert';
import { MOCK_DRIVE_FILES } from '../src/services/driveService';
import { DriveFile, DriveQuery, MimeCategory } from '../types/drive';
import { categorizeMime } from '../src/services/driveService';

import { searchAndSortFiles } from '../src/hooks/useDriveSearch';

test('searchAndSortFiles filters correctly by MIME category', () => {
  const allFiles = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '',
    category: 'all',
    sortField: 'modifiedTime',
    sortOrder: 'desc'
  });
  assert.strictEqual(allFiles.length, 10);

  const pdfFiles = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '',
    category: 'pdf',
    sortField: 'modifiedTime',
    sortOrder: 'desc'
  });
  assert.strictEqual(pdfFiles.length, 4);
  assert.ok(pdfFiles.every((f) => f.mimeType === 'application/pdf'));

  const spreadsheetFiles = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '',
    category: 'spreadsheet',
    sortField: 'modifiedTime',
    sortOrder: 'desc'
  });
  assert.strictEqual(spreadsheetFiles.length, 1);
  assert.strictEqual(spreadsheetFiles[0].name, 'Tabela_Doses_Pediatricas_Gotas_Xarope.gsheet');
});

test('searchAndSortFiles filters correctly by search term', () => {
  // Busca por nome
  const resultsAmoxi = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: 'amoxicilina',
    category: 'all',
    sortField: 'name',
    sortOrder: 'asc'
  });
  assert.strictEqual(resultsAmoxi.length, 1);
  assert.ok(resultsAmoxi[0].name.includes('Amoxicilina'));

  // Busca por ID do Google Drive
  const resultsById = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '1aB2cD3e',
    category: 'all',
    sortField: 'name',
    sortOrder: 'asc'
  });
  assert.strictEqual(resultsById.length, 1);
  assert.strictEqual(resultsById[0].id, '1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV');

  // Busca por Pasta
  const resultsPediatria = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: 'Pediatria',
    category: 'all',
    sortField: 'name',
    sortOrder: 'asc'
  });
  assert.strictEqual(resultsPediatria.length, 3);
});

test('searchAndSortFiles sorts files properly', () => {
  // Ordenação por nome asc
  const sortedNameAsc = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '',
    category: 'all',
    sortField: 'name',
    sortOrder: 'asc'
  });
  for (let i = 0; i < sortedNameAsc.length - 1; i++) {
    assert.ok(sortedNameAsc[i].name.localeCompare(sortedNameAsc[i + 1].name) <= 0);
  }

  // Ordenação por tamanho desc
  const sortedSizeDesc = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '',
    category: 'all',
    sortField: 'sizeBytes',
    sortOrder: 'desc'
  });
  for (let i = 0; i < sortedSizeDesc.length - 1; i++) {
    const sizeCurrent = sortedSizeDesc[i].sizeBytes || 0;
    const sizeNext = sortedSizeDesc[i + 1].sizeBytes || 0;
    assert.ok(sizeCurrent >= sizeNext);
  }
});

test('searchAndSortFiles handles special regex characters and whitespace safely', () => {
  // Teste 1: Termo com whitespace ao redor é normalizado e encontra o arquivo
  const resultWhitespace = searchAndSortFiles(MOCK_DRIVE_FILES, {
    searchTerm: '   IAM   ',
    category: 'all',
    sortField: 'name',
    sortOrder: 'asc'
  });
  assert.strictEqual(resultWhitespace.length, 1);
  assert.ok(resultWhitespace[0].name.includes('IAM'));

  // Teste 2: Caracteres especiais de regex (ex: [ { ( * + ? ^ $ | ) não quebram a aplicação
  assert.doesNotThrow(() => {
    const resultSpecial = searchAndSortFiles(MOCK_DRIVE_FILES, {
      searchTerm: '[*+?^$|(){}',
      category: 'all',
      sortField: 'name',
      sortOrder: 'asc'
    });
    assert.strictEqual(resultSpecial.length, 0);
  });
});

test('searchAndSortFiles safely handles files with partial metadata or invalid dates', () => {
  const imperfectFiles: DriveFile[] = [
    {
      id: 'file-1',
      name: 'Arquivo Alpha',
      mimeType: 'application/vnd.google-apps.document',
      modifiedTime: 'data-invalida',
      owners: []
    },
    {
      id: 'file-2',
      name: 'Arquivo Beta',
      mimeType: 'application/pdf',
      sizeBytes: 500,
      modifiedTime: '2026-09-20T10:00:00Z',
      owners: ['Dono 1']
    }
  ];

  // Ordenação por modifiedTime não deve quebrar nem retornar NaN
  const sortedTime = searchAndSortFiles(imperfectFiles, {
    searchTerm: '',
    category: 'all',
    sortField: 'modifiedTime',
    sortOrder: 'desc'
  });
  assert.strictEqual(sortedTime.length, 2);
  assert.strictEqual(sortedTime[0].id, 'file-2'); // Data válida vem primeiro em desc

  // Ordenação por tamanho com sizeBytes undefined
  const sortedSize = searchAndSortFiles(imperfectFiles, {
    searchTerm: '',
    category: 'all',
    sortField: 'sizeBytes',
    sortOrder: 'asc'
  });
  assert.strictEqual(sortedSize.length, 2);
  assert.strictEqual(sortedSize[0].id, 'file-1'); // undefined avaliado como 0 vem primeiro em asc
});
