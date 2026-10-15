#!/usr/bin/env bash
# One-command rebuild of every number, table, figure and document from data/raw/.
# Usage: ./run_all.sh            (uses the raw files in data/raw/)
#        ./run_all.sh --download (re-downloads the raw files first)
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-python3}
if [[ "${1:-}" == "--download" ]]; then $PY scripts/01_download.py --force; fi
$PY scripts/02_clean.py
$PY scripts/03_build_panel.py
$PY -m pytest -q tests
$PY scripts/04_replicate.py
$PY scripts/00_explore_steady_state.py
$PY scripts/09_descriptive.py
$PY scripts/05_estimate.py
$PY scripts/06_figures.py
$PY scripts/08_paper.py
echo "Rebuild complete: output/tables, output/figures, paper/manuscript.{md,docx}"
