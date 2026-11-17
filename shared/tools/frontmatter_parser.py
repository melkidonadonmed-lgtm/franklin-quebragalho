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
        return {}
    if not isinstance(parsed, dict):
        return {}
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


def _flush_list(
    list_key: Optional[str],
    list_items: List[str],
    in_metadata: bool,
    meta: Dict[str, Any],
    metadata_dict: Dict[str, Any],
) -> None:
    """Flushes accumulated YAML list items into the target metadata dict."""
    if not list_key or not list_items:
        return
    target = metadata_dict if in_metadata else meta
    target[list_key] = list(list_items)


def _apply_kv_assignment(
    key: str,
    val: str,
    target: Dict[str, Any],
) -> Tuple[Optional[str], bool]:
    """Aplica atribuicao escalar ou inicia acumulo multilinha."""
    if val in (">-", ">", "|", "|-"):
        return key, False
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        target[key] = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()] if inner else []
        return None, False
    cleaned = val.strip("'\"")
    target[key] = cleaned
    return None, bool(cleaned)


def _merge_nested_metadata(meta: Dict[str, Any], metadata_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Mescla o bloco metadata no dicionario raiz sem sobrescrever chaves existentes."""
    if metadata_dict:
        meta["metadata"] = metadata_dict
        for k, v in metadata_dict.items():
            meta.setdefault(k, v)
    return meta


def _parse_fallback_lines(raw_yaml: str) -> Dict[str, Any]:
    """Parser leve sem dependências externas para blocos frontmatter simples."""
    meta: Dict[str, Any] = {}
    metadata_dict: Dict[str, Any] = {}
    current_key: Optional[str] = None
    multiline_val: List[str] = []
    list_key: Optional[str] = None
    list_items: List[str] = []
    in_metadata = False
    last_was_scalar_root = False
    last_assigned_key: Optional[str] = None

    for line in raw_yaml.splitlines():
        if not line.strip():
            continue
        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match and (list_key or last_assigned_key):
            if not list_key:
                list_key = last_assigned_key
                current_key = None
                multiline_val = []
            item_val = list_match.group(1).strip().strip("'\"")
            list_items.append(item_val)
            continue
        if re.match(r"^\s+", line) and current_key:
            multiline_val.append(line.strip())
            continue
        _flush_multiline(current_key, multiline_val, in_metadata, meta, metadata_dict)
        _flush_list(list_key, list_items, in_metadata, meta, metadata_dict)
        multiline_val, current_key = [], None
        list_items, list_key = [], None

        if re.match(r"^metadata:\s*$", line):
            in_metadata, last_was_scalar_root, last_assigned_key = True, False, None
            continue

        nested_match = re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line) if in_metadata else None
        if nested_match:
            n_key, n_val = nested_match.group(1), nested_match.group(2).strip()
            current_key, _ = _apply_kv_assignment(n_key, n_val, metadata_dict)
            last_assigned_key = n_key if not n_val else None
            continue

        if last_was_scalar_root and re.match(r"^\s+[a-zA-Z0-9_\-]+:\s*", line):
            return {}

        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            in_metadata = False
            k_name, k_val = kv_match.group(1), kv_match.group(2).strip()
            current_key, last_was_scalar_root = _apply_kv_assignment(k_name, k_val, meta)
            last_assigned_key = k_name if not k_val else None

    _flush_multiline(current_key, multiline_val, in_metadata, meta, metadata_dict)
    _flush_list(list_key, list_items, in_metadata, meta, metadata_dict)
    return _merge_nested_metadata(meta, metadata_dict)


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
