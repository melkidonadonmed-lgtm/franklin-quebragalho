"""
frontmatter_parser.py
Parser determinístico de frontmatter YAML para SKILL.md e notas Markdown,
com suporte a bloco metadata aninhado e fallback sem dependências externas.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extrai frontmatter YAML (com suporte a metadata aninhado) e corpo do documento Markdown."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    raw_yaml, body = match.group(1), match.group(2)
    meta: Dict[str, Any] = {}

    try:
        import yaml

        parsed = yaml.safe_load(raw_yaml)
        if isinstance(parsed, dict):
            meta = parsed
            if "metadata" in meta and isinstance(meta["metadata"], dict):
                for k, v in meta["metadata"].items():
                    if k not in meta:
                        meta[k] = v
            return meta, body
    except ImportError:
        pass

    current_key: str | None = None
    multiline_val: List[str] = []
    in_metadata = False
    metadata_dict: Dict[str, Any] = {}

    for line in raw_yaml.splitlines():
        if re.match(r"^\s+", line) and current_key:
            multiline_val.append(line.strip())
            continue

        if current_key and multiline_val:
            val_joined = " ".join(multiline_val)
            if in_metadata:
                metadata_dict[current_key] = val_joined
            else:
                meta[current_key] = val_joined
            multiline_val = []
            current_key = None

        if re.match(r"^metadata:\s*$", line):
            in_metadata = True
            continue

        if in_metadata and re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line):
            m = re.match(r"^\s+([a-zA-Z0-9_\-]+):\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip().strip("'\"")
                if v in (">-", ">", "|", "|-"):
                    current_key = k
                    multiline_val = []
                else:
                    metadata_dict[k] = v
            continue

        kv_match = re.match(r"^([a-zA-Z0-9_\-]+):\s*(.*)$", line)
        if kv_match:
            in_metadata = False
            key, val = kv_match.group(1), kv_match.group(2).strip()
            if val in (">-", ">", "|", "|-"):
                current_key = key
                multiline_val = []
            else:
                meta[key] = val.strip("'\"")
                current_key = None

    if current_key and multiline_val:
        val_joined = " ".join(multiline_val)
        if in_metadata:
            metadata_dict[current_key] = val_joined
        else:
            meta[current_key] = val_joined

    if metadata_dict:
        meta["metadata"] = metadata_dict
        for k, v in metadata_dict.items():
            if k not in meta:
                meta[k] = v

    return meta, body
