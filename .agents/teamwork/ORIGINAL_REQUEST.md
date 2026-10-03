# Original User Request

## 2026-09-27T08:45:27Z

This is a single self-contained fix; keep it small and focused. Implement Google OAuth 2.0 (Google Identity Services) authentication and real-time Google Drive API v3 data synchronization in the existing React 18 / Vite / Tailwind CSS application, with seamless fallback to offline mock data when no credentials are provided.

Working directory: c:\Users\melki\dev\franklin-quebragalho\google-drive-index-app
Integrity mode: demo

## Requirements

### R1. Autenticação Google OAuth 2.0 via Google Identity Services
Implementar fluxo de autorização client-side moderno utilizando a API oficial do Google (google.accounts.oauth2.initTokenClient) ou biblioteca @react-oauth/google com o escopo de leitura https://www.googleapis.com/auth/drive.readonly. O botão no cabeçalho deve exibir estado de "Conectar Google", alternando para "Desconectar" e exibindo a foto/nome do usuário quando logado.

### R2. Sincronização em Tempo Real com a Google Drive API v3
Conectar a camada de serviço driveService.ts à API v3 do Google Drive (https://www.googleapis.com/drive/v3/files) utilizando o Bearer Token obtido no OAuth. Mapear arquivos reais com ID, nome, MIME type, tamanho em bytes e data de modificação.

### R3. Fallback Gracioso e Configuração Amigável de Client ID
O aplicativo deve funcionar perfeitamente de forma imediata:
- Se houver VITE_GOOGLE_CLIENT_ID no .env ou se o usuário inserir o Client ID em um modal de configuração simples, o OAuth é ativado.
- Se não houver credenciais configuradas, o sistema informa amigavelmente e opera com os dados mockados dos arquivos clínicos do internato sem emitir erros no console.

### R4. Preservação dos Recursos de UI e Acessibilidade Existentes
Manter estritamente os componentes de busca instantânea (debounce de 200ms com atalho Ctrl+K), filtros rápidos de categorias MIME, ordenação clicável e o botão de cópia de ID com feedback tátil.

## Acceptance Criteria

### Compilação e Integridade Técnica
- [ ] O projeto compila com sucesso (npm run build) sem erros de tipagem no TypeScript (strict mode ativado).
- [ ] Nenhuma dependência depreciada ou APIs legadas (como gapi.auth2 antiga) devem ser usadas; utilizar apenas Google Identity Services.

### Fluxo de Autenticação & Dados
- [ ] O usuário consegue abrir o popup de consentimento OAuth do Google ao clicar em "Conectar com Google".
- [ ] Após a autorização, a tabela exibe os arquivos reais da conta Google Drive retornados pela API v3.
- [ ] Na ausência de Client ID, o botão de configuração permite inserir um ID temporário ou continuar no modo de demonstração.

### Usabilidade e Feedback
- [ ] Indicador de carregamento (spinner) ativo durante a requisição de autenticação e busca no Drive.
- [ ] Toast notification informa com clareza o sucesso da conexão ou eventuais erros de autenticação.
