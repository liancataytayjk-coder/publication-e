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

**Result (2026-10-15, `output/tables/replication_gate.csv`): PASS — all 17 criteria.** MRW: Table I non-oil ln s 1.424 (target 1.42), ln(n+g+δ) −1.990 (−1.97), N = 98; Table II 0.697 / −1.745 / 0.654 (0.69 / −1.73 / 0.66); Table V ln y60 −0.288 / −0.366 / −0.398 and λ 0.0136 / 0.0182 / 0.0203 (all three samples on target); Table VI α 0.484, β 0.228 (0.48, 0.23). Barro: 80 countries, 783 observations (exactly as published); col 1 0.0016 (s.e. 0.0011; target 0.0019), R² 0.090 (0.095); col 2 −0.0295 (0.0064; target −0.0326), R² 0.379 (0.381); difference −0.031. `rgdpl` gives the same to three decimals. *Indicative* col 3 with public substitutes: −0.0167 (0.0025) against Barro's −0.0171 (0.0022), 691 observations; life expectancy, fertility, inflation and schooling-by-sex signs match, V-Dem rule of law and democracy are weaker than ICRG and Freedom House were for Barro.

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
| D9 | 2026-10-15 | Fixed-effects bias correction: **indirect inference** (match the FE slope and the within s.d. of ln y in simulated panels of the same size), not the split-panel jackknife. | Simulation tests (`tests/test_estimators.py`): with 10 five-year periods and true λ = 0.02, FE gives λ ≈ 0.042; the jackknife over-corrects (b too close to zero); indirect inference gives λ ≈ 0.024. Logged before any new-data estimate. | pre-registered |
| D10 | 2026-10-15 | Method B sample: PWT 11.0 countries with GDP data starting by the 1965–70 period (Barro's criterion) and population ≥ 0.5 million in 1990. Main periods 1965–70 … 2015–20, 2020–23 (1960–65 lacks lagged instruments). | Mirrors Barro's sample rule; drops micro-states and post-1990 countries. | pre-registered |
| D11 | 2026-10-15 | Method A sample per window: population ≥ 1 million at window start and mean oil rents < 20% of GDP (WDI); complete data. y = real GDP per working-age person (level from rgdpo, growth from rgdpna, PWT's recommended split); s_k = mean csh_i; n = growth of population 15–64 (WDI); SCHOOL = secondary gross enrolment × (population 15–19 / population 15–64), as MRW built it. Windows 1960–85, 1965–90, …, 1995–2020, 1998–2023. | Closest modern analogue to MRW's non-oil sample and variables. | pre-registered |
| D12 | 2026-10-15 | Method B variables: y = rgdpe per capita (levels and growth; Barro used PWT 7 chain `rgdpch`); X = 1/life expectancy, ln fertility, V-Dem rule of law, csh_i, csh_g, openness (national current prices), V-Dem democracy and its square, inflation (period mean, capped at 100%/yr), Barro–Lee years by sex at period start, terms-of-trade growth × openness. Period averages instrumented by previous-period averages; schooling and terms of trade treated as exogenous, as Barro did. | Barro's specification with public data. The inflation cap keeps a few hyperinflation periods from dominating. | pre-registered |
| D13 | 2026-10-15 | **Post-run correction:** the terms-of-trade term (growth of export relative to import prices × openness) is treated as a *shock* in the Philippine distance and decomposition, not as a steady-state determinant. The regression itself is unchanged. The pre-registered version is kept as robustness row B0. | Barro (2015, section III) treats contemporaneous terms-of-trade growth as a temporary growth influence. Putting it in the steady state made d jump with each terms-of-trade swing (2020 d: +0.23 with it, −0.22 without). Found on reading the first run. | correction after first run (supplementary) |
| D14 | 2026-10-15 | **Reconciliation of the two methods (supplementary):** R1 Method B with MRW determinants only; R2 Method A cross-section with Barro's determinants added; R3 Method A with current (last 5 years) instead of 25-year-average working-age population growth. Plus a decomposition of each method's Philippine steady state into determinant contributions relative to the sample mean. | Added after the pre-registered agreement rule failed on the sign of d. Labelled supplementary. | supplementary |

## Estimation plan (pre-specified 2026-10-15, before any new-data estimate)

**Common settings.** PWT 11.0; g\* = 0.02 (steady-state growth per person, MRW's convention); g + δ = 0.05; λ from the exact formula λ = −ln(1 + bτ)/τ; half-life ln 2/λ. Uncertainty from a country-cluster bootstrap (499 draws; for each draw re-estimate and recompute the Philippine quantities), reported as 90% percentile intervals.

**RQ1 (Objective 1, descriptive).** The Philippine path relative to peers: growth by decade, output per worker relative to the US, capital-output ratio against its implied steady state (`scripts/00`, exploratory, D2–D4), and the dating of large negative growth shocks. Descriptive; no hypothesis test.

**RQ2 (Objective 2): how far is the Philippines from its own steady state, and is the distance shrinking?**
- *Method A.* For each 25-year window, MRW Table V regression (unrestricted conditional convergence) on the D11 sample. The Philippines' distance at the window start is d₀ = (Δ̂ − g\*T)/b, using fitted growth Δ̂ (Cho–Graham logic); at the window end d_T = d₀ + (Δ_actual − g\*T). Headline: d in 2023 from the 1998–2023 window.
- *Method B (main = Barro's preferred column 3 analogue).* 2SLS with time effects and X, no fixed effects, D10 sample, periods 1965–2023. The Philippines' distance at each period start t is d_t = (ĝ_t − g\*)/b, with ĝ_t = ã_t + b ln y_t + X_t′γ̂, where ã_t is the fitted linear trend of the estimated time effects (so world business-cycle shocks do not move the steady state). Headline: d at the start of 2020–23 and its path since 1965.
- *Agreement rule (the user's "do the two methods converge?").* The methods agree if, at the latest common date (2020): (i) the sign of d is the same; (ii) the 90% intervals overlap; and (iii) the λ of each method lies inside the other's 90% interval. The correlation of the two Philippine d paths over 1985–2020 is reported descriptively.

**RQ3 (Objective 2): how fast does the Philippines close the gap?** λ and half-life from Method A (each window; headline latest) and Method B main. Also Method B with country fixed effects, raw and corrected by indirect inference (D9), as the bound on how fast convergence could be if the Philippines' own fixed characteristics are allowed for.

**RQ4 (Objective 2): why "approaching but not quite"?** For the Philippines, from Method B main, the exact period-by-period identity
Δd_t = τb·d_t [closing, H1] + τ(a_t − ã_t) [world shock, H3] + τe_t [Philippine shock, H3] − m_t [steady state moving, H2],
where m_t = Δln y\*_t − g\*τ, split into contributions −γ_kΔX_k/b of each determinant plus the trend term. Decision rules: H1 is supported if d is negative and its trend over 1965–2020 is towards zero; H2 if the cumulative m_t is positive and at least half the size of the cumulative closing term; H3 if the shock terms are negative in at least two of the three crisis periods named in advance (1980–85 debt crisis, 1995–2000 Asian crisis, 2015–20 and 2020–23 COVID-19); H4 (low own steady state) if the Philippines' mean residual ē_PH in Method B main is negative with a 90% bootstrap interval below zero. The "own-productivity" distance d^own = (ĝ + ē_PH − g\*)/b is reported next to d.

**RQ5 (Objective 3, policy).** Steady-state gains if each Philippine determinant moved to the median of four ASEAN peers (Indonesia, Malaysia, Thailand, Viet Nam) in the latest period: Δln y\* = −γ_kΔX_k/b (Method B) and, for investment and schooling, from Method A's coefficients (Δln y\* = −(γ_k/b_A)Δln X_k). With the half-life, the time needed to close half of the new gap.

**Robustness (pre-registered menu).** Method B: (B1) g\* = 0.015, 0.025, the g\* that puts the US at its steady state on average, and the g\* implied by the time-effect trend; (B2) raw time effects a_t; (B3) growth from rgdpna; (B4) 10-year periods; (B5) data ending 2019 (last period 2015–19); (B6) OLS instead of 2SLS; (B7) without the V-Dem variables; (B8) excluding oil-rich countries (mean oil rents > 20% of GDP); (B9) country fixed effects, raw and indirect-inference corrected; (B10) Barro's period window 1965–2005 on PWT 11. Method A: (A1) restricted Table VI form; (A2) ln(hc) instead of ln SCHOOL; (A3) per capita instead of per working-age person; (A4) g\* = 0.015 and 0.025. In the text, name every check under which a headline conclusion changes.

**Labels.** Everything above is *pre-registered*. Anything added after the first new-data run is labelled *supplementary* (specified before running but after seeing main results) or *exploratory*.

## Results (2026-10-15; `output/tables/`)

- **Speed (RQ3).** Method B main: b = −0.0198 (s.e. 0.0052), λ = 2.1% a year (90% bootstrap 1.2–3.3%), half-life 33 years; 98 countries, 1,143 observations. Fixed effects raw λ = 4.0%, corrected by indirect inference 1.7% (half-life 40 years), exactly Barro's point that FE overstate convergence. Method A, latest window 1998–2023: λ = 1.2% (0.9–1.5%), half-life 56 years; 1.0–1.7% in every window. Both inside the 1–2.5% "iron law" range.
- **Distance (RQ2).** Method B main: Philippines below its steady state by 0.20–0.39 log points in every period start 1985–2020 (2020: −0.22, 90% band −0.77 to +1.01); bands include zero after 1965. Method A: above its MRW steady state from the 2000 window end onwards (2020: +0.45 [0.12, 0.89]; 2023: +0.41 [0.03, 0.82]).
- **Agreement rule (pre-registered):** (i) same sign in 2020: **fails** (A +0.45, B −0.22); (ii) 90% intervals overlap: passes; (iii) λ each inside the other's interval: **fails** (A's 1.4% is inside B's band, B's 2.1% is not inside A's). Correlation of the paths 1985–2020: −0.60. The disagreement is not a g\* artefact (both distances move almost one-for-one with g\*) and not a normalisation artefact (relative to the median country A puts PHL at the 74th percentile, B at the 28th).
- **Reconciliation (supplementary, D14).** Swapping determinant sets does not flip the signs (R1 B with MRW variables −0.70; R2 A with Barro variables +0.12). What drives A's positive sign is population growth: A's steady state uses 1995–2020 average working-age population growth (2.45%/yr), which lowers PHL's steady state by 0.55 log points relative to the mean; B uses current fertility (now below the sample mean), which raises it. With current population growth (R3), A's distance falls to +0.14 (2020) and +0.05 (2023), inside B's band. Reading: the two methods catch the Philippine steady state at different points of the demographic transition; once current demography is used, both place the Philippines **close to its steady state** (within roughly ±0.25 log points), with the steady state rising.
- **Why "not quite" (RQ4, Method B decomposition).** 1985–2020: convergence closed +0.20 log points, but the steady state rose 0.245 log points faster than the 2% path (fertility decline and longer lives relative to the world; lower inflation), and shocks netted +0.05; the distance was unchanged (−0.23 → −0.22). 1965–85: the steady state fell (−0.46 against the 2% path; inflation, rule of law, government consumption) while crises hit. Pre-registered rules: H1 not supported (no trend towards zero: −0.04 per decade); H2 not supported over 1965–2020 (cumulative movement −0.215) — *exploratory:* it holds for 1985–2020 (+0.245 vs closing +0.20); H3 supported (shock terms negative in 1980–85, 1995–2000, 2015–20); H4 not supported (PHL mean residual +0.0013 [−0.011, 0.014]: the Philippines grows as its determinants predict).
- **Robustness.** Method B d in 2020 is negative in 13 of 14 B checks (positive only for g\* = 0.025 and for the pre-registered terms-of-trade treatment B0); Method A d in 2023 positive in all A checks (0.06 to 0.75). λ for B ranges 1.2% (10-year periods) to 2.9% (data ending 2019; Barro's window).
- **Policy (RQ5).** Moving to the ASEAN-4 median: life expectancy +0.27, fertility +0.15, openness +0.11, investment +0.06 (B) / +0.63 (A) log points on the steady state; half of any gain arrives in 33 (B) to 56 (A) years.
- **Descriptive (RQ1).** GDP per person relative to the US: 10.5% (1960), 11.3% (1980), 9.5% (2000), 13.7% (2019), 12.9% (2023) (rgdpe). Large negative years: 1984, 1985, 1991, 1998, 2020.

## Documents

- `docs/01_exploring_the_question.md` — Phase 1 exploration note (hand-written).

## Pipeline

`./run_all.sh` (Phase 7). For now: `python scripts/00_explore_steady_state.py`.

## Open questions

- [ ] **Q5.** Data extension to 2024–25 (PWT ends 2023): out of scope for the first version; note as a limitation.
- [ ] **Q6.** Verify the co-authors and editors of Felipe, Abdon & Kumar (2012), Clarete, Esguerra & Hill (2018) and Balisacan & Hill (2003) before citing.
- [ ] **Q8.** Target journal and its format (word limit, reference style). Until named, the manuscript uses a generic economics-journal format with APA-like author–date references.
- [ ] **Q9.** Barro (2015) published EJ tables: check the targets against the published version if the user has access.

**Status:** Phases 1–5 done; Phase 6 (manuscript) in progress.
