# Padrões de Diagramação Mermaid e Árvores Comentadas (`organizador-fluxo-arvore-arquivos` v1.2.0)

Referência técnica de Tier 3 para construção de fluxogramas Mermaid à prova de falhas de parser e árvores de diretórios ASCII comentadas.

---

## 1. Regras de Sintaxe Mermaid Segura (Módulo `M5`)

1. **Tipos de Diagrama Permitidos**: Utilize prioritariamente `flowchart TD` (Top-Down) ou `flowchart LR` (Left-Right).
2. **Aspas Duplas Obrigatórias em Rótulos com Caracteres Especiais**: Qualquer nó cujo texto contenha parênteses `()`, colchetes `[]`, barras `/` ou dois-pontos `:` deve ter o rótulo entre aspas duplas:
   - Correto: `A["Entrada do Usuário (Formulário Web)"] --> B["Validação de Dados"]`
   - Proibido: `A[Entrada do Usuário (Formulário Web)]` (quebra o parser Mermaid).
3. **Zero Tags HTML Brutas**: Não utilize `<br>`, `<b>` ou `<div>` dentro dos nós Mermaid.

---

## 2. Convenção de Árvore de Diretórios Comentada

```text
nome-do-projeto/
├── src/                        # Código-fonte principal da aplicação
│   ├── core/                   # Regras de negócio puras e cálculos determinísticos
│   ├── ui/                     # Componentes visuais desacoplados
│   └── main.py                 # Ponto de entrada (Entrypoint) da aplicação
├── tests/                      # Suíte de testes automatizados falsificáveis
├── .env.example                # Modelo de variáveis de ambiente (sem segredos reais)
└── README.md                   # Guia rápido de instalação e execução
```

---

## 3. Pipeline de Exportação Direta (`.md` / `.pdf`)
- **Arquivo Único Markdown (`.md`)**: Gravação com codificação UTF-8 e Lei da Linha em Branco antes/depois de blocos ```mermaid e ```text.
- **Conversão para PDF (`.pdf`)**: Delegação à skill `conversor-html-pdf` via Microsoft Edge headless (`msedge.exe --headless --print-to-pdf`), garantindo `break-inside: avoid` nos diagramas e árvores.
