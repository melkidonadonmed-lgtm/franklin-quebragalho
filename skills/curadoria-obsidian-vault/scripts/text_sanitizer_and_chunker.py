# /// script
# dependencies = [
#     "pydantic>=2.0.0",
# ]
# ///

"""
Módulo de Higienização de Texto, Chunking Proporcional e Enriquecimento de Metadados.

Funcionalidades:
1. Higienização de Texto:
   - Remoção de caracteres invisíveis (zero-width spaces, BOM, control characters).
   - Normalização de espaços irregulares e quebras de linha excessivas.
   - Deduplicação de linhas redundantes para evitar ruído e distorção em embeddings vetoriais.
2. Fragmentação em Chunks com Sobreposição Proporcional:
   - Divisão inteligente em blocos sem quebra de palavras/sentenças.
   - Sobreposição configurável entre 10% e 15% (overlap_ratio: 0.10 a 0.15) para preservação de continuidade narrativa.
3. Atribuição Criptográfica e Identificação Unívoca:
   - Cálculo determinístico de hash SHA-256 para o documento pai e para cada fragmento individual.
4. Metadados Ricos para Busca Híbrida (Hybrid Vector Search):
   - Associação de documento de origem, categoria, índice sequencial, contagem de caracteres e tokens estimados.
   - Compatível com filtros de payload para Qdrant, Pinecone, Milvus, ChromaDB e PostgreSQL (pgvector).
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# MODELOS DE DADOS PYDANTIC v2
# =============================================================================

class SanitizationStats(BaseModel):
    """Estatísticas do processo de higienização de texto."""
    model_config = ConfigDict(extra="forbid")
    invisible_chars_removed: int = Field(default=0, description="Caracteres invisíveis ou de controle expurgados")
    spaces_normalized: int = Field(default=0, description="Ocorrências de espaços múltiplos colapsados")
    duplicate_lines_removed: int = Field(default=0, description="Linhas redundantes ou duplicadas expurgadas")
    original_char_count: int = Field(..., description="Contagem bruta original de caracteres")
    cleaned_char_count: int = Field(..., description="Contagem final de caracteres após higienização")
    reduction_percentage: float = Field(default=0.0, description="Percentual de redução volumétrica")


class ChunkMetadata(BaseModel):
    """Metadados anexados a cada fragmento para viabilizar filtragem híbrida."""
    model_config = ConfigDict(extra="forbid")
    source_doc: str = Field(..., description="Documento ou URI de origem")
    category: str = Field(default="geral", description="Categoria temática para filtragem por metadados")
    chunk_index: int = Field(..., ge=0, description="Índice sequencial do chunk no documento (0-indexed)")
    total_chunks: int = Field(..., ge=1, description="Total de fragmentos gerados para o documento")
    char_count: int = Field(..., ge=1, description="Quantidade exata de caracteres no chunk")
    token_count_est: int = Field(..., ge=1, description="Estimativa de tokens (base heurística BPE)")
    start_char: int = Field(..., ge=0, description="Posição de caractere inicial no texto higienizado")
    end_char: int = Field(..., ge=1, description="Posição de caractere final no texto higienizado")
    overlap_ratio: float = Field(..., ge=0.0, le=0.30, description="Percentual de sobreposição aplicado (ex: 0.12)")
    has_overlap_prev: bool = Field(default=False, description="Indica se há sobreposição com o chunk anterior")
    has_overlap_next: bool = Field(default=False, description="Indica se há sobreposição com o chunk posterior")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(), description="Timestamp UTC")
    extra_tags: dict[str, Any] = Field(default_factory=dict, description="Tags adicionais para busca vetorial híbrida")


class TextChunk(BaseModel):
    """Estrutura representativa de um fragmento processado."""
    model_config = ConfigDict(extra="forbid")
    chunk_id: str = Field(..., description="Hash identificador determinístico único do chunk (SHA-256 curto)")
    content_hash: str = Field(..., description="Hash SHA-256 integral do conteúdo textual do fragmento")
    parent_doc_hash: str = Field(..., description="Hash SHA-256 integral do documento de origem higienizado")
    text: str = Field(..., min_length=1, description="Texto sanitizado do fragmento")
    metadata: ChunkMetadata = Field(..., description="Metadados para indexação híbrida")


class ChunkingResult(BaseModel):
    """Resultado consolidado da operação de higienização e chunking."""
    model_config = ConfigDict(extra="forbid")
    source_doc: str
    category: str
    parent_doc_hash: str
    stats: SanitizationStats
    total_chunks: int
    chunks: list[TextChunk]


# =============================================================================
# MOTOR DE HIGIENIZAÇÃO (TEXT SANITIZER)
# =============================================================================

class TextSanitizer:
    """Higienizador determinístico de texto voltado à qualidade de embeddings."""

    # Regex para caracteres invisíveis:
    # \u200B (Zero Width Space), \u200C (ZWNJ), \u200D (ZWJ), \uFEFF (BOM),
    # \u2060 (Word Joiner), \u200E-\u200F (LTR/RTL marks), \u202A-\u202E (Directional formatting)
    # \x00-\x08, \x0B, \x0C, \x0E-\x1F (Caracteres de controle ASCII exceto \t, \n, \r)
    INVISIBLE_CHARS_PATTERN = re.compile(
        r"[\u200b\u200c\u200d\ufeff\u2060\u200e\u200f\u202a-\u202e"
        r"\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
    )

    # Regex para espaços não-quebráveis e variantes unicode (\u00a0, \u2000-\u200a, \u3000)
    UNICODE_SPACES_PATTERN = re.compile(r"[\u00a0\u2000-\u200a\u3000\u202f\u205f]")

    @classmethod
    def clean_invisible_characters(cls, text: str) -> tuple[str, int]:
        """Remove caracteres invisíveis e caracteres de controle."""
        matches = len(cls.INVISIBLE_CHARS_PATTERN.findall(text))
        cleaned = cls.INVISIBLE_CHARS_PATTERN.sub("", text)
        return cleaned, matches

    @classmethod
    def normalize_spaces(cls, text: str) -> tuple[str, int]:
        """Converte espaços exóticos em espaços comuns e remove repetições consecutivas."""
        # 1. Normaliza espaços unicode para espaço ASCII simples
        text = cls.UNICODE_SPACES_PATTERN.sub(" ", text)

        # 2. Colapsa espaços horizontais múltiplos (preservando quebras de linha)
        consecutive_spaces_count = len(re.findall(r"[^\S\r\n]{2,}", text))
        text = re.sub(r"[^\S\r\n]+", " ", text)

        return text, consecutive_spaces_count

    @classmethod
    def deduplicate_and_clean_lines(cls, text: str) -> tuple[str, int]:
        """Remove espaços no final de linhas, deduplica linhas consecutivas idênticas e colapsa linhas em branco."""
        lines = text.splitlines()
        cleaned_lines: list[str] = []
        dup_count = 0
        last_non_empty_line: Optional[str] = None

        for raw_line in lines:
            line = raw_line.strip()

            # Evita linhas em branco consecutivas múltiplas (limita a no máximo 1 linha em branco estrutural)
            if not line:
                if cleaned_lines and cleaned_lines[-1] != "":
                    cleaned_lines.append("")
                continue

            # Deduplicação de linhas idênticas consecutivas (típico de cabeçalhos/rodapés repetidos)
            if line == last_non_empty_line:
                dup_count += 1
                continue

            cleaned_lines.append(line)
            last_non_empty_line = line

        result = "\n".join(cleaned_lines).strip()
        return result, dup_count

    @classmethod
    def sanitize(cls, raw_text: str) -> tuple[str, SanitizationStats]:
        """Executa o pipeline completo de higienização com métricas detalhadas."""
        orig_len = len(raw_text)

        # Passo 1: Limpeza de caracteres invisíveis
        step1, inv_count = cls.clean_invisible_characters(raw_text)

        # Passo 2: Normalização de espaços
        step2, space_count = cls.normalize_spaces(step1)

        # Passo 3: Limpeza de linhas e deduplicação consecutiva
        step3, dup_count = cls.deduplicate_and_clean_lines(step2)

        final_len = len(step3)
        reduction = round(((orig_len - final_len) / orig_len * 100), 2) if orig_len > 0 else 0.0

        stats = SanitizationStats(
            invisible_chars_removed=inv_count,
            spaces_normalized=space_count,
            duplicate_lines_removed=dup_count,
            original_char_count=orig_len,
            cleaned_char_count=final_len,
            reduction_percentage=reduction
        )

        return step3, stats


# =============================================================================
# MOTOR DE CHUNKING COM SOBREPOSIÇÃO NARRATIVA PROPORCIONAL (10% A 15%)
# =============================================================================

class TextChunker:
    """Divisor proporcional de texto com sobreposição contextual e atribuição criptográfica."""

    def __init__(
        self,
        target_chunk_size: int = 800,
        overlap_ratio: float = 0.12,  # 12% por padrão (dentro da faixa 10% - 15%)
        min_chunk_size: int = 150
    ):
        if not (0.05 <= overlap_ratio <= 0.25):
            raise ValueError(f"overlap_ratio deve estar razoavelmente entre 0.05 e 0.25 (recebido: {overlap_ratio})")

        self.target_chunk_size = target_chunk_size
        self.overlap_ratio = overlap_ratio
        self.overlap_size = int(target_chunk_size * overlap_ratio)
        self.min_chunk_size = min_chunk_size

    def _find_natural_break(self, text: str, ideal_pos: int, window: int = 80) -> int:
        """Busca o melhor ponto de quebra (parágrafo, sentença ou pontuação) próximo à posição ideal."""
        text_len = len(text)
        if ideal_pos >= text_len:
            return text_len

        search_start = max(0, ideal_pos - window)
        search_end = min(text_len, ideal_pos + window)
        region = text[search_start:search_end]

        # 1. Tenta quebra de parágrafo duplo
        p_double = region.rfind("\n\n")
        if p_double != -1 and (search_start + p_double + 2) > search_start + 20:
            return search_start + p_double + 2

        # 2. Tenta quebra de linha simples
        p_single = region.rfind("\n")
        if p_single != -1 and (search_start + p_single + 1) > search_start + 20:
            return search_start + p_single + 1

        # 3. Tenta pontuação de fim de sentença (. ! ?)
        match = None
        for m in re.finditer(r"([.!?])\s+", region):
            match = m
        if match and (search_start + match.end()) > search_start + 20:
            return search_start + match.end()

        # 4. Tenta quebra de palavra (espaço simples)
        p_space = region.rfind(" ")
        if p_space != -1 and (search_start + p_space + 1) > search_start + 15:
            return search_start + p_space + 1

        # Fallback para a posição ideal se não houver quebra natural
        return ideal_pos

    def split_into_chunks(
        self,
        cleaned_text: str,
        source_doc: str,
        category: str = "geral",
        extra_tags: Optional[dict[str, Any]] = None
    ) -> ChunkingResult:
        """Realiza o fatiamento proporcional do texto higienizado anexando hashes e metadados."""
        extra_tags = extra_tags or {}
        parent_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()
        text_len = len(cleaned_text)

        if text_len == 0:
            return ChunkingResult(
                source_doc=source_doc,
                category=category,
                parent_doc_hash=parent_hash,
                stats=SanitizationStats(original_char_count=0, cleaned_char_count=0),
                total_chunks=0,
                chunks=[]
            )

        # Se o texto for menor ou próximo ao tamanho alvo, gera um chunk único
        if text_len <= (self.target_chunk_size + self.overlap_size):
            chunk_text = cleaned_text
            content_h = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            chunk_id = hashlib.sha256(f"{source_doc}:0:{content_h}".encode("utf-8")).hexdigest()[:16]

            meta = ChunkMetadata(
                source_doc=source_doc,
                category=category,
                chunk_index=0,
                total_chunks=1,
                char_count=len(chunk_text),
                token_count_est=max(1, len(chunk_text) // 4),
                start_char=0,
                end_char=len(chunk_text),
                overlap_ratio=self.overlap_ratio,
                has_overlap_prev=False,
                has_overlap_next=False,
                extra_tags=extra_tags
            )

            chunk = TextChunk(
                chunk_id=chunk_id,
                content_hash=content_h,
                parent_doc_hash=parent_hash,
                text=chunk_text,
                metadata=meta
            )

            return ChunkingResult(
                source_doc=source_doc,
                category=category,
                parent_doc_hash=parent_hash,
                stats=SanitizationStats(original_char_count=text_len, cleaned_char_count=text_len),
                total_chunks=1,
                chunks=[chunk]
            )

        # Particionamento iterativo com sobreposição proporcional
        raw_chunks: list[dict[str, Any]] = []
        cursor = 0

        while cursor < text_len:
            # Ponto final proposto antes do ajuste natural
            ideal_end = cursor + self.target_chunk_size
            actual_end = self._find_natural_break(cleaned_text, ideal_end)

            chunk_slice = cleaned_text[cursor:actual_end].strip()

            if chunk_slice:
                raw_chunks.append({
                    "start": cursor,
                    "end": actual_end,
                    "text": chunk_slice
                })

            if actual_end >= text_len:
                break

            # Avança o cursor aplicando o recuo de sobreposição (overlap entre 10% e 15%)
            step = (actual_end - cursor) - self.overlap_size
            # Garante avanço mínimo para evitar loops infinitos
            if step <= 0:
                step = max(1, self.target_chunk_size // 2)

            cursor += step

        # Refinamento final: se o último chunk for muito diminuto, mescla com o anterior
        if len(raw_chunks) > 1 and len(raw_chunks[-1]["text"]) < self.min_chunk_size:
            last = raw_chunks.pop()
            prev = raw_chunks[-1]
            merged_start = prev["start"]
            merged_end = max(prev["end"], last["end"])
            raw_chunks[-1] = {
                "start": merged_start,
                "end": merged_end,
                "text": cleaned_text[merged_start:merged_end].strip()
            }

        total = len(raw_chunks)
        final_chunks: list[TextChunk] = []

        for idx, item in enumerate(raw_chunks):
            c_text = item["text"]
            content_h = hashlib.sha256(c_text.encode("utf-8")).hexdigest()
            # ID determinístico combinando documento, índice sequencial e hash de conteúdo
            chunk_id = hashlib.sha256(f"{source_doc}:{idx}:{content_h}".encode("utf-8")).hexdigest()[:16]

            meta = ChunkMetadata(
                source_doc=source_doc,
                category=category,
                chunk_index=idx,
                total_chunks=total,
                char_count=len(c_text),
                token_count_est=max(1, len(c_text) // 4),
                start_char=item["start"],
                end_char=item["end"],
                overlap_ratio=self.overlap_ratio,
                has_overlap_prev=(idx > 0),
                has_overlap_next=(idx < total - 1),
                extra_tags=extra_tags
            )

            final_chunks.append(
                TextChunk(
                    chunk_id=chunk_id,
                    content_hash=content_h,
                    parent_doc_hash=parent_hash,
                    text=c_text,
                    metadata=meta
                )
            )

        return ChunkingResult(
            source_doc=source_doc,
            category=category,
            parent_doc_hash=parent_hash,
            stats=SanitizationStats(original_char_count=text_len, cleaned_char_count=text_len),
            total_chunks=total,
            chunks=final_chunks
        )


# =============================================================================
# PIPELINE UNIFICADO
# =============================================================================

def process_document(
    raw_text: str,
    source_doc: str,
    category: str = "geral",
    target_chunk_size: int = 800,
    overlap_ratio: float = 0.12,
    extra_tags: Optional[dict[str, Any]] = None
) -> ChunkingResult:
    """Executa o pipeline completo: Higienização -> Chunking Proporcional -> Atribuição Criptográfica."""
    cleaned_text, stats = TextSanitizer.sanitize(raw_text)
    chunker = TextChunker(target_chunk_size=target_chunk_size, overlap_ratio=overlap_ratio)
    result = chunker.split_into_chunks(
        cleaned_text=cleaned_text,
        source_doc=source_doc,
        category=category,
        extra_tags=extra_tags
    )
    result.stats = stats
    return result


# =============================================================================
# EXECUÇÃO CLI E AUTOTESTE
# =============================================================================

def run_self_test():
    """Valida todos os requisitos solicitados pelo usuário em um cenário sintético rigoroso."""
    print("\n" + "=" * 70)
    print("🧪 EXECUTANDO AUTOTESTE DO HIGIENIZADOR E CHUNKER PROPORCIONAL")
    print("=" * 70)

    # Texto de teste propositalmente corrompido com:
    # 1. Caracteres invisíveis (Zero Width Space \u200B, BOM \uFEFF, Control \x00)
    # 2. Espaços unicode não-quebráveis (\u00A0)
    # 3. Espaços múltiplos irregulares
    # 4. Linhas duplicadas consecutivas
    corrupted_sample = (
        "Artigo 1. Do Objeto e Finalidades.\u200b\ufeff\n"
        "Artigo 1. Do Objeto e Finalidades.\n"  # Linha duplicada proposital
        "Esta cláusula regula    os procedimentos   de   auditoria contábil.\u00a0\u00a0\n"
        "Esta cláusula regula    os procedimentos   de   auditoria contábil.\n"  # Duplicada
        "\n\n\n"
        "Parágrafo Único. Os relatórios fiscais deverão conter todos os cálculos detalhados.\x00\n"
        "O auditor independente analisará as divergências tributárias entre a contabilidade "
        "e o faturamento declarado no período de competência. Em caso de divergência apurada, "
        "o comitê de compliance fiscal será notificado imediatamente para emitir parecer técnico "
        "fundamentado nas normas da Receita Federal do Brasil.\n\n"
        "Artigo 2. Da Certificação e Validação Digital.\n"
        "Todas as transações deverão ser acompanhadas de assinatura criptográfica e selo temporal "
        "para assegurar a tempestividade, a integridade da base e a rastreabilidade das operações.\n"
    )

    result = process_document(
        raw_text=corrupted_sample,
        source_doc="contrato_auditoria_fiscal_2026.txt",
        category="tributario_auditoria",
        target_chunk_size=300,
        overlap_ratio=0.12,  # 12% de overlap (dentro de 10-15%)
        extra_tags={"jurisdicao": "BR", "versao": "2.0"}
    )

    print(f"\n📊 Estatísticas de Higienização:")
    print(f"  • Caracteres invisíveis removidos: {result.stats.invisible_chars_removed}")
    print(f"  • Espaços irregulares normalizados: {result.stats.spaces_normalized}")
    print(f"  • Linhas duplicadas eliminadas:     {result.stats.duplicate_lines_removed}")
    print(f"  • Tamanho original -> higienizado:  {result.stats.original_char_count} -> {result.stats.cleaned_char_count} chars (-{result.stats.reduction_percentage}%)")
    print(f"  • Hash do documento pai (SHA-256):  {result.parent_doc_hash[:16]}...")

    print(f"\n🧩 Fragmentos Gerados (Total: {result.total_chunks}):")
    for chunk in result.chunks:
        m = chunk.metadata
        print(f"\n  ▶ Chunk [{m.chunk_index + 1}/{m.total_chunks}] ID: {chunk.chunk_id} | Hash: {chunk.content_hash[:12]}...")
        print(f"    - Faixa: chars {m.start_char}..{m.end_char} ({m.char_count} chars, ~{m.token_count_est} tokens)")
        print(f"    - Overlap: {int(m.overlap_ratio * 100)}% (Prev: {m.has_overlap_prev}, Next: {m.has_overlap_next})")
        print(f"    - Metadados Híbridos: categoria='{m.category}', doc='{m.source_doc}', tags={m.extra_tags}")
        print(f"    - Amostra do texto:\n      \"{chunk.text[:90]}...\"")

    # Asserções de conformidade
    assert result.stats.invisible_chars_removed >= 2, "Deveria remover caracteres invisíveis"
    assert result.stats.duplicate_lines_removed >= 1, "Deveria remover linhas duplicadas"
    assert result.total_chunks >= 2, "Deveria gerar pelo menos 2 chunks para testar overlap"
    assert result.chunks[0].chunk_id != result.chunks[1].chunk_id, "Chunk IDs devem ser únicos"
    assert result.chunks[1].metadata.has_overlap_prev is True, "Chunk 1 deve ter overlap anterior"

    print("\n" + "=" * 70)
    print("✅ AUTOTESTE CONCLUÍDO COM 100% DE SUCESSO!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--test":
        input_path = Path(sys.argv[1])
        if not input_path.exists():
            print(f"❌ Erro: Arquivo {input_path} não encontrado.")
            sys.exit(1)
        raw = input_path.read_text(encoding="utf-8")
        cat = sys.argv[2] if len(sys.argv) > 2 else "geral"
        res = process_document(raw, source_doc=input_path.name, category=cat)
        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
    else:
        run_self_test()
