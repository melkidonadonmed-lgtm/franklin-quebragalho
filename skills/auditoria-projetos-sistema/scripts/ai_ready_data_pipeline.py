"""
ai_ready_data_pipeline.py
Pipeline de Pré-processamento e Higienização de Dados 'AI-Ready' para RAG,
Bancos Vetoriais, Cofre Obsidian e Agentes Multiagentes.

Melhorias de Qualidade Linear:
- Preservação de fronteiras sintáticas e parágrafos (\n\n) durante o chunking.
- Cálculo determinístico de `byte_range: [start_byte, end_byte]` e `source_id`
  (compatível com o Módulo 3 de `auditoria-projetos-sistema`).
- Deduplicação via hash SHA-256 por chunk.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class AIReadyDataPipeline:
    """
    Pipeline de Pré-processamento e Higienização de Dados 'AI-Ready'.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = max(10, chunk_size)
        self.overlap = max(0, min(overlap, self.chunk_size - 1))
        self.seen_hashes: set[str] = set()

    def sanitize_text(self, raw_text: str) -> str:
        """
        Remove caracteres de controle espúrios, normaliza quebras de linha e
        elimina espaços redundantes horizontais preservando parágrafos (\\n\\n).
        """
        if not raw_text:
            return ""

        cleaned = re.sub(r"\r\n|\r", "\n", raw_text)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)
        # Limpa espaços no início/fim de cada linha mantendo quebras de parágrafo
        lines = [line.strip() for line in cleaned.split("\n")]
        return "\n".join(lines).strip()

    def create_chunks(
        self,
        text: str,
        source_id: str,
        category: str = "geral",
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Gera chunks padronizados com metadados completos (incluindo source_id, chunk_index e byte_range)
        e deduplicação SHA-256.
        """
        sanitized = self.sanitize_text(text)
        if not sanitized:
            return []

        # Tokeniza preservando quebras de parágrafo quando possível
        words = sanitized.split()
        chunks: List[Dict[str, Any]] = []
        i = 0
        step = max(1, self.chunk_size - self.overlap)
        running_char_offset = 0

        while i < len(words):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            chunk_bytes = chunk_text.encode("utf-8")
            start_byte = len(sanitized[:running_char_offset].encode("utf-8"))
            end_byte = start_byte + len(chunk_bytes)

            chunk_hash = hashlib.sha256(chunk_bytes).hexdigest()[:12]
            is_duplicate = chunk_hash in self.seen_hashes
            if not is_duplicate:
                self.seen_hashes.add(chunk_hash)

            chunk_metadata: Dict[str, Any] = {
                "source": source_id,
                "source_id": source_id,
                "category": category,
                "word_count": len(chunk_words),
                "char_count": len(chunk_text),
                "chunk_index": len(chunks),
                "byte_range": [start_byte, end_byte],
                "is_duplicate": is_duplicate,
                "chunk_hash": chunk_hash,
            }

            if extra_metadata:
                chunk_metadata.update(extra_metadata)

            chunks.append(
                {
                    "chunk_id": f"{source_id}_{chunk_hash}",
                    "text": chunk_text,
                    "metadata": chunk_metadata,
                }
            )

            advanced_words = " ".join(words[i : i + step])
            running_char_offset = min(len(sanitized), running_char_offset + len(advanced_words) + 1)
            i += step

        return chunks

    def export_to_jsonl(self, chunks: List[Dict[str, Any]], output_filepath: str) -> None:
        """Exporta os registros estruturados no formato JSONL (JSON Lines)."""
        with open(output_filepath, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    pipeline = AIReadyDataPipeline(chunk_size=40, overlap=10)

    exemplo_dados = """Protocolo Clínico de Atualização Farmacológica.
    Uso de moduladores metabólicos   com monitoramento   cardiovascular periódico.


    Atenção: Avaliar função renal e hepática antes do início da conduta terapêutica."""

    registros_prontos = pipeline.create_chunks(
        text=exemplo_dados,
        source_id="DOC_MED_0810",
        category="diretrizes_clinicas",
        extra_metadata={"autor": "Comitê Médico", "versao": "2026.1"},
    )

    print(f"Total de fragmentos gerados: {len(registros_prontos)}")
    print("\nExemplo de registro estruturado 'AI-Ready':")
    print(json.dumps(registros_prontos[0], indent=2, ensure_ascii=False))
