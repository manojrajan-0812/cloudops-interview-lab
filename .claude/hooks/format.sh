#!/usr/bin/env bash
set -euo pipefail

FILE=$(python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))")

[[ -z "$FILE" ]] && exit 0
[[ "$FILE" == *.py ]] || exit 0

python3 -m ruff format --quiet "$FILE" 2>/dev/null || exit 0
