# Publication E — Approaching but Not Quite: Is the Philippines Converging to Its Own Steady State?

An empirical growth study, written up as a journal article. It replicates two reference designs — Mankiw, Romer & Weil (1992) and Barro (2015) — and applies them to Penn World Table 11.0 (1960–2023) to measure how far the Philippines is from its own steady state, how fast the gap closes, and why it never seems to close.

## Documents

| File | What it is |
| --- | --- |
| `paper/manuscript.docx` / `paper/manuscript.md` | The journal manuscript (rendered; do not edit by hand) |
| `paper/manuscript_template.md` | The manuscript source; numbers come from `output/tables/paper_numbers.json` |
| `paper/SUBMISSION_CHECKLIST.md` | What remains before submission |
| `paper/references.bib` | Verified bibliography |
| `CLAUDE.md` | Project brief: notation, reference specifications, replication gate, decisions log, pre-registered plan, results, open questions |
| `docs/01_exploring_the_question.md` | Phase 1 exploration note |
| `docs/session_handoff.Rmd` | How to resume the project in a new session |

## Rebuild

```
pip install -r requirements.txt
./run_all.sh              # from data/raw/ (committed)
./run_all.sh --download   # re-download every raw file first
```

The pipeline: `01_download` → `02_clean` → `03_build_panel` → tests → `04_replicate` (gate) → `00_explore` and `09_descriptive` (Objective 1) → `05_estimate` (Objectives 2–3) → `06_figures` → `08_paper`.

## Layout

`data/raw/` untouched downloads (logged in `data/raw/source_log.md`); `data/processed/` built by scripts (gitignored); `steadystate/estimators.py` estimators; `tests/` simulation tests; `replication/` published targets; `output/tables`, `output/figures` written by scripts.
