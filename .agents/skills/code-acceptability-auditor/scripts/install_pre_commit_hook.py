#!/usr/bin/env python3
"""
install_pre_commit_hook.py
Instala um Git Hook pre-commit determinístico que executa o Code Acceptability Auditor
nos arquivos Python staged antes de autorizar o commit.
"""

import argparse
import os
import stat
from pathlib import Path

PRE_COMMIT_TEMPLATE = """#!/usr/bin/env sh
# Gerado automaticamente por code-acceptability-auditor
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\\.py$' || true)
if [ -z "$STAGED_PY" ]; then
    exit 0
fi

echo "[code-acceptability-auditor] Auditando arquivos Python staged..."
for FILE in $STAGED_PY; do
    if [ -f "$FILE" ]; then
        python "{auditor_script}" --file "$FILE"
        if [ $? -ne 0 ]; then
            echo "[BLOCKED] Commit abortado: $FILE reprovado nos critérios de aceite."
            exit 1
        fi
    fi
done
echo "[PASS] Todos os arquivos Python staged cumpriram os critérios de aceite."
exit 0
"""


def install_hook(repo_root: Path) -> Path:
    git_hooks_dir = repo_root / ".git" / "hooks"
    git_hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = git_hooks_dir / "pre-commit"
    auditor_script = (Path(__file__).resolve().parent / "code_acceptability_auditor.py").as_posix()

    content = PRE_COMMIT_TEMPLATE.format(auditor_script=auditor_script)
    hook_path.write_text(content, encoding="utf-8", newline="\n")
    try:
        current_mode = os.stat(hook_path).st_mode
        os.chmod(hook_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        pass
    return hook_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala o Git Hook pre-commit do Code Acceptability Auditor.")
    parser.add_argument("--repo-root", type=str, default=".", help="Raiz do repositório Git")
    args = parser.parse_args()

    hook_file = install_hook(Path(args.repo_root).resolve())
    print(f"[PASS] Git pre-commit hook instalado em: {hook_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
