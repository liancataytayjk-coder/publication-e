# Publication E — Is the Philippines approaching its steady state?

Phase 1 (research) of an empirical growth study on whether the Philippine economy is converging to its Solow steady state, and why it seems to approach without arriving.

- `CLAUDE.md` — project brief, notation, decisions log, open questions.
- `docs/01_exploring_the_question.md` — exploration note: what "steady state" means, first look at the data, competing hypotheses, draft research questions, candidate reference designs, data feasibility.
- `scripts/00_explore_steady_state.py` — exploratory diagnostics (writes `output/exploration/`).
- `data/raw/` — untouched downloads, logged in `data/raw/source_log.md`.

Rebuild the exploration:

```
pip install -r requirements.txt
python scripts/00_explore_steady_state.py
```
