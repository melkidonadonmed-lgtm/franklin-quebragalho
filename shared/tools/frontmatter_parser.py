"""
frontmatter_parser.py
Parser determinístico de frontmatter YAML para SKILL.md e notas Markdown,
com suporte a bloco metadata aninhado e fallback sem dependências externas.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


def _try_yaml_safe_load(raw_yaml: str) -> Optional[Dict[str, Any]]:
    """Tenta carregar o frontmatter via PyYAML higienizando caracteres de controle."""
    try:
        import yaml
    except ImportError as exc:
        _ = exc
        return None
    try:
        parsed = yaml.safe_load(raw_yaml)
    except (yaml.YAMLError, ValueError, TypeError, KeyError) as exc:
        _ = exc
        return None
    if not isinstance(parsed, dict):
        return None
    nested = parsed.get("metadata")
    if isinstance(nested, dict):
        for k, v in nested.items():
            parsed.setdefault(k, v)
    return parsed


def _flush_multiline(
    current_key: Optional[str],
    multiline_val: List[str],
    in_metadata: bool,
    meta: Dict[str, Any],
    metadata_dict: Dict[str, Any],
) -> None:
    """Consolida linhas acumuladas de um escalar YAML multilinha."""
    if not current_key or not multiline_val:
        return
    target = metadata_dict if in_metadata else meta
    target[current_key] = " ".join(multiline_val)


def _parse_fallback_lines(raw_yaml: str) -> Dict[str, Any]:
    """Parser leve sem dependências externas para blocos frontmatter simples."""
    meta: Dict[str, Any] = {}
    metadata_dict: Dict[str, Any] = {}
    current_key: Optional[str] = None
    multiline_val: List[str] = []
    in_metadata = False

    for line in raw_yaml.splitlines():
        if re.match(r"^\s+", line) and current_key:
            multiline_val.append(line.strip())
            continue
        _flush_multiline(current_key, multiline_val, in_metadata, meta, metadata_dict)
        multiline_val, current_key = [], None

        if re.match(r"^metadata:\s*$", line):
            in_metadata = True
            continue

        nested_match = re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line) if in_metadata else None
        if nested_match:
            k, v = nested_match.group(1), nested_match.group(2).strip().strip("'\"")
            if v in (">-", ">", "|", "|-"):
                current_key = k
            else:
                metadata_dict[k] = v
            continue

        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            in_metadata = False
            key, val = kv_match.group(1), kv_match.group(2).strip()
            if val in (">-", ">", "|", "|-"):
                current_key = key
            else:
                meta[key] = val.strip("'\"")

    _flush_multiline(current_key, multiline_val, in_metadata, meta, metadata_dict)
    if metadata_dict:
        meta["metadata"] = metadata_dict
        for k, v in metadata_dict.items():
            meta.setdefault(k, v)
    return meta


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extrai frontmatter YAML (com suporte a metadata aninhado) e corpo do documento Markdown."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    raw_yaml = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", match.group(1))
    body = match.group(2)
    yaml_meta = _try_yaml_safe_load(raw_yaml)
    if yaml_meta is not None:
        return yaml_meta, body
    return _parse_fallback_lines(raw_yaml), body
