# Publication E: Is the Philippines approaching its steady state? — project brief

The study asks whether the Philippine economy is approaching its Solow steady state, and why it seems to approach without arriving. It separates three meanings: the country's own (conditional) steady state, the world frontier, and a steady growth rate. It then measures how much of the persistent distance is due to the steady state moving, to recurring shocks, and to a low steady state (stalled productivity). Units: the Philippines, 1960 to the latest year, against ASEAN peers, Korea, China and the United States. Output and target journal: **to be decided (Q3)**. Reference design: **to be decided (Q1)**; the recommended design is Mankiw, Romer & Weil (1992) with Cho & Graham (1996). See `docs/01_exploring_the_question.md`.

**Current phase: 1 (Research).** The exploration note has been written. The brief is in draft until the user answers Q1–Q3.

## Conventions

- `data/raw/` holds untouched downloads only. Every file gets an entry in
  `data/raw/source_log.md` (URL, date pulled, base year, coverage, checksum).
- `data/processed/` and `output/` are written by scripts, never by hand.
- `replication/<paper>_targets.csv` holds the reference paper's coefficients.
- No new-data estimate is reported until the replication gate passes. The
  Phase 1 exploration (`scripts/00_explore_steady_state.py`) is labelled
  *exploratory* and is a feasibility check only.
- Every specification choice goes in the decisions log below, with the evidence,
  labelled pre-registered / supplementary / exploratory.
- Documents are rendered from templates; never edit rendered .md/.docx by hand.
  (The Phase 1 exploration note is hand-written and quotes exploratory numbers
  with their source file; later documents must pull numbers from output tables.)
- User style: as simple as possible, define every term on first use (words →
  formula → example), paragraphs over bullets/tables.

## Notation

| Symbol | Meaning |
| --- | --- |
| t | year |
| c | country |
| K, Y, L | capital stock, real GDP, employment |
| s | real investment share of GDP (gross fixed capital formation / GDP, national prices) |
| n | employment growth |
| g | labour-augmenting technology growth |
| δ | depreciation rate |
| A, h | productivity (TFP) level, human capital per worker |
| α | capital share (1 − labour share) |
| (K/Y)\* | steady-state capital-output ratio, s / (n + g + δ) |
| gap | ln(K/Y) − ln(K/Y)\* |
| λ | speed of convergence (share of the gap closed per year) |

## Reference specification

*Pending Q1.* If Option A is chosen:

- Equation (MRW 1992, Tables I–II): ln(Y/L)_c = a + b₁ ln s_c + b₂ ln(n_c + g + δ) [+ b₃ ln(school)_c] + ε_c, OLS across countries, with g + δ = 0.05. Restricted version imposes b₁ = −b₂. Convergence regression (MRW Table IV–VI): growth 1960–85 on ln y_1960 and the same regressors.
- Cho & Graham (1996): use the fitted steady state to compute each country's distance, ln y_c − ln y\*_c, and classify countries as above or below.
- Samples: MRW non-oil (98), intermediate (75) and OECD (22). The targets must be typed from the PDF into `replication/mrw1992_targets.csv`. Do not type them from memory.

## Decisions log

| # | Date | Decision | Evidence / reason | Status |
| --- | --- | --- | --- | --- |
| D1 | 2026-10-15 | Exploration uses Penn World Table 11.0 (1950–2023) for all countries. | Only public source with consistent capital stocks, depreciation, human capital and TFP for all peers. | exploratory |
| D2 | 2026-10-15 | National-prices K/Y = (rnna / rgdpna) × (pl_n / pl_gdpo) in 2021. | rnna and rgdpna use different PPPs. The accumulation identity ΔK = sY − δK only balances after rescaling: the implied factor is 1.61 for PHL, against 1/0.605 = 1.65; for the USA it is 1.01 against 1.00. | exploratory |
| D3 | 2026-10-15 | (K/Y)\* uses 10-year trailing means of s, n, δ. V1: g = 0.02 (MRW convention). V2: n + g replaced by trend real GDP growth. | V1 is the theoretically correct form but needs an assumed g; V2 avoids choosing g but treats transitional growth as permanent. PHL TFP growth 2010–19 (≈1%/yr, labour share ≈0.43) implies g ≈ 2.4%, close to V1. The USA sits +26% above under V1 in 2019, so gap *levels* are not reliable; use changes. | exploratory |
| D4 | 2026-10-15 | Speed-of-convergence regression uses 1980–2019 (excludes COVID years), with HAC standard errors (3 lags). | A single 2020 outlier would dominate a 40-observation regression. | exploratory |

## Exploratory findings (2026-10-15; `output/exploration/`)

- PHL national-prices K/Y stayed at about 1.9–2.15 over 1985–2019, so it looks like a steady state.
- ln(K/Y)\* (V1) rose by 0.30 over 2010–19 (0.26 from s, 0.06 from n, −0.02 from δ) while ln(K/Y) rose by 0.07. The gap went from about 0 to −0.21 (V1); under V2 it stays about 0.
- TFP (rtfpna) is lower in 2023 than in 1980. Output per worker grew 1.1%/yr over 1980–2023.
- Output per worker relative to the US: 18.6% (1960), 19.5% (1980), 12.1% (2000), 18.1% (2019), 16.4% (2023).
- λ ≈ 0.10 (SE 0.05), half-life ≈ 7 years (1980–2019). Noisy; not for citation.

## Draft research questions and hypotheses

- **Objective 1 (descriptive). RQ1:** the path of the distance to its own steady state and to the frontier, 1960–latest, against peers.
- **Objective 2 (estimation). RQ2:** λ and its stability. **RQ3:** decomposition of gap changes into target movement versus the economy's own movement. **RQ4:** stochastic convergence to the US, allowing for structural breaks.
- **Objective 3 (policy). RQ5:** steady-state and transition-time effects of higher s, h or g.
- **Hypotheses:** H1 asymptotic approach; H2 moving target; H3 shocks faster than healing; H4 low steady state (A, g); H5 trap / multiple equilibria.

## Documents

- `docs/01_exploring_the_question.md` — Phase 1 exploration note (hand-written).

## Pipeline

`python scripts/00_explore_steady_state.py` rebuilds `output/exploration/` from `data/raw/pwt/`. A `run_all.sh` will be added in Phase 2.

## Open questions

- [ ] **Q1.** Reference design: A (MRW + Cho–Graham), B (Bernard–Durlauf time series), C (Kremer–Willis–You framing), or a combination? Recommended: A + B, with C for framing.
- [ ] **Q2.** Main meaning of "steady state": own steady state (recommended), frontier, or steady growth?
- [ ] **Q3.** Output format, audience and template (journal article, thesis chapter, policy brief).
- [ ] **Q4.** Does a concept note or earlier draft for Publication E exist?
- [ ] **Q5.** Data extension to 2024–25: confirm whether PSA publishes a capital stock series. If not, use the study's own perpetual-inventory extension from PSA gross fixed capital formation.
- [ ] **Q6.** Verify the co-authors of Felipe, Abdon & Kumar (2012), and the editors of Clarete, Esguerra & Hill (2018) and Balisacan & Hill (2003). Crossref records are incomplete.
- [ ] **Q7.** King & Rebelo (1993, AER) journal version is not on Crossref (only NBER WP w3185). Verify before citing.
