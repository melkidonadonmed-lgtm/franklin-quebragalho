# Guia de Estilo Markdown Canônico (Obsidian & Antigravity)

Diretrizes de diagramação e sintaxe para redação técnica:

1. **Frontmatter Canônico:**
   - Sempre em minúsculas nas chaves (`title`, `date`, `tags`, `author`, `status`).
   - Datas estritamente no padrão ISO `YYYY-MM-DD`.

2. **Cercas de Código:**
   - Sempre declarar o identificador de linguagem na abertura (ex.: `powershell`, `javascript`, `python`, `json`, `yaml`, `mermaid`, `text`).
   - Nunca deixar cerca de código sem linguagem declarada se contiver sintaxe estruturada.

3. **Links e Imagens:**
   - Para links locais de arquivos no sistema operacional: sempre utilizar o esquema `file:///` com barras normais (`/`).
   - Para links internos no Obsidian: usar notação de Wikilink com rótulo semântico `[[NomeDaNota|Texto Exibido]]`.

4. **Hierarquia de Títulos:**
   - Título 1 (`#`) reservado para o título do documento.
   - Títulos de seções principais em Título 2 (`##`).
   - Subseções em Título 3 (`###`).
