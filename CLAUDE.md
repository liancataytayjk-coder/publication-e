# Publication E: Is the Philippines approaching its steady state? — project brief

Journal article. The study asks whether the Philippine economy is approaching **its own** (conditional) Solow steady state, and why it seems to approach without arriving. It answers with two reference designs that should agree: the classic cross-country augmented Solow model of Mankiw, Romer & Weil (1992, "MRW"), and the more recent panel conditional-convergence design of Barro (2015, "Convergence and Modernisation", *Economic Journal*). Barro's design pays explicit attention to the bias from country fixed effects (the Hurwicz–Nickell bias). Each design gives (i) the Philippines' distance from its steady state and (ii) the speed at which that distance closes. The gap is then decomposed into the steady state moving, shocks, and closing. Units: 1960–2023, Penn World Table 11.0, about 100 countries, with the Philippines as the focus and ASEAN peers for comparison.

**User decisions (2026-10-15):** Q2 own steady state; Q1 two foundational papers, one classic (MRW 1992) and one recent and rigorous (Barro 2015), hoping the two methods converge on one answer; Q3 journal article; Q4 no concept note — build everything from scratch with the empirical-econ-study workflow.

**Current phase:** see the "Status" line at the end of this file.

## Conventions

- `data/raw/` holds untouched downloads only (`scripts/01_download.py`). Every file has a row in `data/raw/source_log.md`.
- `data/processed/` and `output/` are written by scripts, never by hand.
- `replication/<paper>_targets.csv` holds the reference papers' coefficients, typed from the PDFs (MRW: QJE PDF from D. Romer's site; Barro: NBER WP 18295, revised Sept 2012, the working-paper version of Barro 2015).
- No new-data estimate is reported until the replication gate passes.
- Every specification choice goes in the decisions log, labelled pre-registered / supplementary / exploratory.
- Documents are rendered from templates (`paper/*_template.md`); never edit rendered .md/.docx by hand. The Phase 1 note `docs/01_exploring_the_question.md` is the only hand-written document.
- User style: as simple as possible, define every term on first use (words → formula → example), paragraphs over bullets/tables.

## Notation

| Symbol | Meaning |
| --- | --- |
| i, t | country, year (or start year of a period) |
| y | real GDP per working-age person (Method A) or per capita (Method B) |
| s_k | investment share of GDP (physical capital) |
| s_h | investment in human capital (MRW: SCHOOL, % of working-age population in secondary school) |
| n | growth of working-age population (A) / of population (B) |
| g, δ | technology growth, depreciation; g + δ = 0.05 (MRW) |
| α, β | output elasticities of physical and human capital |
| X | steady-state determinants (Barro: life expectancy, fertility, rule of law, investment, schooling, government consumption, openness, terms of trade, democracy, inflation) |
| b | coefficient on ln y in a growth regression (annual rate) |
| λ | speed of convergence: share of the remaining gap closed per year; b = −(1 − e^{−λτ})/τ |
| y\* | steady-state path of y |
| d | distance from steady state, d = ln y − ln y\* (negative = below) |
| g\* | steady-state growth of y per person, 0.02 by convention |

## Reference specifications

**Method A — MRW (1992).** Cross-section OLS, one observation per country, window 1960–1985.
- Levels (Tables I–II): ln(Y/L)_85 = a + b₁ ln s_k + b₂ ln(n + g + δ) [+ b₃ ln SCHOOL] + ε, with g + δ = 0.05. Restricted versions impose b₁ = −b₂ (I) and b₁ + b₂ + b₃ = 0 (II). α, β implied.
- Convergence (Tables V–VI): ln y_85 − ln y_60 = c + b ln y_60 + γ₁ ln s_k + γ₂ ln(n+g+δ) + γ₃ ln SCHOOL + ε; λ = −ln(1 + b)/25.
- Samples: non-oil (98), intermediate (75), OECD (22), from MRW's indicators N, I, O.
- Steady state used by this study (Cho & Graham 1996 logic): ln y\*_{i,0} = ln y_{i,0} + (Δ̂_i − g\*T)/(−b), so d_{i,0} = (Δ̂_i − g\*T)/b, where Δ̂ is fitted growth.

**Method B — Barro (2015).** Panel of 5-year periods 1960–65, …, 2005–09; 80 countries (WP Table 2); dependent variable is the annual growth rate of real per capita GDP (PWT 7.0, 2005 international dollars) over each period; regressors are ln y at the period start plus time effects, with ln y one year earlier as the instrument.
- Col 1: time effects only. Col 2: plus country fixed effects. Col 3: plus X variables (period averages, instrumented by lagged values), no fixed effects. Col 4: col 3 plus fixed effects.
- Errors correlated within countries (we use 2SLS with country-clustered standard errors).
- Barro's argument: with ~10 periods, fixed effects overstate convergence (Hurwicz–Nickell bias), so col 3 (X variables, no FE) is his preferred estimate, about 1.7% per year.

## Replication gate (pre-registered 2026-10-15, before any estimate)

Method A uses MRW's own dataset (`data/raw/mrw1992/MRW1992.txt`), so tolerances only allow for rounding in the published tables.

- **G1 (MRW Table I, non-oil):** ln s_k coefficient within ±0.02 of 1.42; ln(n+g+δ) within ±0.03 of −1.97; N = 98.
- **G2 (MRW Table II, non-oil):** ln s_k within ±0.02 of 0.69; ln(n+g+δ) within ±0.03 of −1.73; ln SCHOOL within ±0.02 of 0.66.
- **G3 (MRW Table V, all three samples):** ln y_60 coefficient within ±0.005 of target (−0.289, −0.366, −0.398); implied λ within ±0.0005 of target (0.0137, 0.0182, 0.0203).
- **G4 (MRW Table VI, non-oil):** implied α within ±0.02 of 0.48 and implied β within ±0.02 of 0.23.

Method B is rebuilt from PWT 7.0 (`rgdpch`, the chain series, as the main choice; `rgdpl` is reported alongside but does not decide the gate). Barro used a SUR-type estimator and a dataset we cannot see, so the tolerances are wider.

- **G5 (Barro Table 1, col 1, no FE):** coefficient on ln y_lag in [−0.0010, 0.0050] (target 0.0019), and not significantly negative at 5%.
- **G6 (Barro Table 1, col 2, FE):** coefficient in [−0.0400, −0.0250] (target −0.0326), significant at 1%.
- **G7 (ordering):** col 2 coefficient below col 1 by at least 0.020 (target gap 0.0345).
- *Indicative only (not part of the gate):* col 3 with public substitutes for ICRG law and order (V-Dem rule of law) and Freedom House (V-Dem electoral democracy); expected in [−0.025, −0.010].

The gate passes only if G1–G7 all pass. If it fails, stop, re-read the specification, fix the code, and log what changed. Ranges are not loosened after seeing results.

**Result:** *not yet run.*

## Decisions log

| # | Date | Decision | Evidence / reason | Status |
| --- | --- | --- | --- | --- |
| D1 | 2026-10-15 | PWT 11.0 (1950–2023) is the main dataset for new estimates. | Only public source with consistent PPP output, capital, investment shares and human capital for ~180 countries. | pre-registered |
| D2 | 2026-10-15 | National-prices K/Y = (rnna / rgdpna) × (pl_n / pl_gdpo)₂₀₂₁ for the descriptive capital-output analysis. | Accumulation identity balances only after rescaling (implied factor 1.61 PHL vs 1/0.605 = 1.65; USA 1.01 vs 1.00). | exploratory |
| D3 | 2026-10-15 | Descriptive (K/Y)\* from 10-year trailing means; V1 g = 0.02, V2 trend GDP growth. | See `docs/01_exploring_the_question.md`. Gap levels are sensitive to g; use changes. | exploratory |
| D4 | 2026-10-15 | Descriptive speed regression on K/Y gap uses 1980–2019, HAC(3). | Avoid COVID outlier. | exploratory |
| D5 | 2026-10-15 | Reference designs: MRW (1992) as the classic, Barro (2015) as the recent rigorous design. Cho & Graham (1996) logic for the MRW-implied distance. | User's choice of "one classic, one recent and rigorous". Barro directly addresses own-steady-state convergence and the FE bias. Both have public data for a replication gate. | pre-registered |
| D6 | 2026-10-15 | Barro targets are from NBER WP 18295 (2012), the working-paper version of Barro (2015). The published EJ tables were not accessible. | NBER PDF is public; EJ is paywalled. Flag in the checklist. | pre-registered |
| D7 | 2026-10-15 | Barro col 1–2 replication: PWT 7.0 `rgdpch`, China = "CHN" (version 1), periods 1960–65 … 2005–09 (last period 4 years), growth annualised by the period length, instrument ln y_{t−1}, 2SLS, clustered by country. | Closest public analogue to Barro's description. | pre-registered |
| D8 | 2026-10-15 | Public substitutes for Barro's X variables: V-Dem rule of law (for ICRG law and order), V-Dem electoral democracy (for Freedom House political rights), WDI CPI inflation (GDP deflator where CPI missing), Barro–Lee v3 years of schooling ages 25–64 by sex (population-weighted from 10-year age groups; v3 has no 25+ aggregate), PWT terms of trade pl_x/pl_m. | ICRG is proprietary; Freedom House is not machine-downloadable here. V-Dem is the standard public alternative. | pre-registered |

## Estimation plan

*To be written before the first new-data estimate (Phase 4).*

## Results

*None yet.*

## Documents

- `docs/01_exploring_the_question.md` — Phase 1 exploration note (hand-written).

## Pipeline

`./run_all.sh` (Phase 7). For now: `python scripts/00_explore_steady_state.py`.

## Open questions

- [ ] **Q5.** Data extension to 2024–25 (PWT ends 2023): out of scope for the first version; note as a limitation.
- [ ] **Q6.** Verify the co-authors and editors of Felipe, Abdon & Kumar (2012), Clarete, Esguerra & Hill (2018) and Balisacan & Hill (2003) before citing.
- [ ] **Q8.** Target journal and its format (word limit, reference style). Until named, the manuscript uses a generic economics-journal format with APA-like author–date references.
- [ ] **Q9.** Barro (2015) published EJ tables: check the targets against the published version if the user has access.

**Status:** Phase 1 done; Phase 2 (data) in progress.
