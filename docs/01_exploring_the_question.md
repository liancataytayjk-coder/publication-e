# Is the Philippines approaching its steady state? Exploring the research question

*Publication E. Phase 1 exploration note. Prepared 15 October 2026.*

*Status: exploratory. All numbers below come from `scripts/00_explore_steady_state.py`, run on Penn World Table 11.0. They are feasibility checks, not pre-registered estimates, and they will change once the specification is fixed.*

## 1. The short answer

The answer depends on which steady state we mean. The data point to a clear working answer, which the study would then test formally.

Measured by its own capital accumulation, the Philippines has looked like an economy sitting at a steady state for about thirty-five years. Its capital-output ratio stayed between roughly 1.9 and 2.15 from 1985 to 2019. It is still not quite there, for three reasons. First, the target keeps moving. Second, large shocks push the economy off its path faster than it can close the distance. Third, the steady state it is moving towards is a low one, because productivity has barely grown since 1980.

Measured against the world frontier, the Philippines is not converging at all. Output per worker was about 19% of the US level in 1960 and about 16% in 2023, after falling to 12% around 2000.

The research question can therefore be sharpened. *Is the Philippines approaching a steady state?* is mostly answered "yes, but asymptotically and towards a moving target". The more interesting question is **why the distance never closes**, and how much of that is the target moving, how much is shocks, and how much is a low target.

## 2. What "steady state" means, and why the phrase is ambiguous

**The steady state.** In the Solow–Swan growth model (Solow, 1956; Swan, 1956), the steady state is the point where capital per *effective* worker stops changing. It is "per effective worker" because each worker's productivity also grows with technology. At the steady state, the investment that adds capital exactly offsets what is lost to depreciation, to a growing workforce and to technology making each worker more productive. One consequence is that the capital-output ratio is constant there:

$$\left(\frac{K}{Y}\right)^{*} = \frac{s}{n + g + \delta} \tag{1}$$

Here s is the share of GDP that is invested, n the growth rate of employment, g the growth rate of labour-augmenting technology and δ the rate of depreciation. *Example:* if the Philippines invests s = 22% of GDP, employment grows n = 2% a year, technology g = 2% and capital wears out at δ = 4.5%, then (K/Y)\* = 0.22 / 0.085 ≈ 2.6. In the long run the economy holds about 2.6 pesos of capital for every peso of annual output.

**Distance from the steady state.** With a Cobb–Douglas production function Y = K^α (AhL)^(1−α), output per worker y can be written as

$$y = A \cdot h \cdot \left(\frac{K}{Y}\right)^{\alpha/(1-\alpha)} \tag{2}$$

Here A is technology (productivity), h is human capital per worker and α is the capital share. Holding A and h fixed, the percentage distance of output per worker from its steady-state path is

$$\text{gap}^{y}_t \approx \frac{\alpha}{1-\alpha}\left[\ln\left(\frac{K}{Y}\right)_t - \ln\left(\frac{K}{Y}\right)^{*}_t\right] \tag{3}$$

*Example:* with α = 1/3, a capital-output ratio 20% below its steady state means output per worker is about 10% below its steady-state path.

**Why the economy is always "approaching but not quite".** Near the steady state, the model says the economy closes a fixed share λ of the remaining distance every year (Barro & Sala-i-Martin, 1992; Mankiw, Romer & Weil, 1992):

$$\ln y_t - \ln y^{*}_t = e^{-\lambda t}\,(\ln y_0 - \ln y^{*}_0) \tag{4}$$

λ is called the speed of convergence. Because the remaining gap shrinks by a fixed fraction rather than a fixed amount, it never reaches exactly zero. *Example:* the classic estimate is λ ≈ 2% a year. At that speed half of any gap closes in ln 2 / 0.02 ≈ 35 years, three-quarters in 70 years, and the last quarter takes another 70. So part of the "not quite" is simply how convergence works, even in a textbook economy with no shocks.

**Three meanings people have in mind.** The question in the title can mean three different things, and the study must say which one it tests.

1. *Its own steady state* (conditional convergence). Is the Philippines approaching the steady state set by its own investment rate, population growth, schooling and productivity? This is the steady state in equation (1).
2. *The frontier* (unconditional or absolute convergence). Is the Philippines catching up with rich countries? This happens only if its steady state is close to theirs.
3. *Steady growth* (a balanced growth path). Has growth settled at a constant rate, for example the "6% economy" of the 2010s? In the model, steady-state growth of output per worker equals g, the rate of technology growth.

The exploration below looks at all three, because the gap between meanings 1 and 2 is exactly where the puzzle sits.

## 3. What a first look at the data shows

These are exploratory checks on Penn World Table 11.0 (Feenstra, Inklaar & Timmer, 2015), covering 1950–2023. Files are in `output/exploration/`.

**Measurement note.** Penn World Table (PWT) reports capital (`rnna`) and GDP (`rgdpna`) in 2021 US dollars. However, it converts them with *different* purchasing-power parities, one for investment goods and one for GDP. Their ratio is therefore not the national-prices capital-output ratio needed in equation (1). For the Philippines the correction factor (the 2021 price level of capital relative to GDP) is about 0.61. Skipping it would overstate K/Y by about two-thirds. We checked this against the capital accumulation identity, which only balances once the correction is applied (decision D2 in `CLAUDE.md`).

**Finding 1: the capital-output ratio looks like a steady state.** In national prices, K/Y rose from about 1.3 in the early 1970s to 2.1 in 1985, during the debt-financed investment boom of the Marcos years and the collapse of output in 1984–85. It has then stayed between about 1.9 and 2.15 every year from 1985 to 2019 (`phl_snapshot.csv`, Figure 1). A constant capital-output ratio is one of the "stylised facts" of an economy on its balanced growth path (Jones, 2016). This is why the Philippines *looks* like it has arrived.

**Finding 2: but the target moved.** Through the 2010s the investment share rose from about 18% to 27% of GDP. The 10-year average rose from 0.17 in 2010 to 0.22 in 2019. The steady-state ratio in equation (1), with g set at 2%, rose by about 30 log points over 2010–2019, while the actual ratio rose by only 7 (`phl_star_decomposition.csv`). Of the 30-point rise in the target, about 26 points came from higher investment and 6 from slower employment growth. Depreciation changed little. The distance between actual and steady-state K/Y therefore went from about zero in 2010 to about −21% in 2019. Equation (3) translates that into output per worker roughly 10% below its steady-state path. In plain words, the Philippines was approaching a steady state, and the steady state then moved away from it. COVID-19 in 2020 then knocked output down and pushed the ratio up for the wrong reason. In 2023 the gap was still about −11%.

**Finding 3: the result is sensitive to what we assume about long-run growth.** If we replace "n + 2%" in the denominator of (1) with the economy's own 10-year average GDP growth, which was about 6% in the 2010s, the 2019 gap is close to zero (variant V2 in Figure 2). The two variants disagree because they answer different questions. V1 assumes that the 6% growth of the 2010s was partly temporary catching up. V2 assumes that 6% is the new normal. Whether the Philippines is "at" its steady state therefore hinges on whether the 2010s growth rate is permanent. This is exactly the "approaching but not quite" ambiguity in measurable form. The measured productivity data lean towards V1: total factor productivity (TFP), the part of output growth not explained by more capital or more labour, grew only about 1% a year over 2010–2019. With a labour share of about 0.43, that implies labour-augmenting technology growth of roughly 1.02 / 0.43 ≈ 2.4% a year. This is close to the 2% assumed in V1 and well below the roughly 4% that V2 implicitly assumes (6.2% GDP growth minus 1.9% employment growth). A sanity check also argues for caution with levels. Under V1 the United States itself sits 26% *above* its steady state in 2019, which suggests that a single g = 2% does not fit every country. The study should rely on *changes* in the gap more than on its level.

**Finding 4: the steady state the Philippines is approaching is low, because productivity stalled.** Measured TFP in 2023 was *lower* than in 1980. It fell by about 1.6% a year over 1980–2000, recovered by about 1% a year over 2000–2019, and fell again after 2019 (`rtfpna` in `steady_state_gap.csv`). Output per worker grew only about 1.1% a year over 1980–2023. In the Solow model, long-run growth comes only from g. An economy with g near zero for four decades can sit close to its own steady state and still make no progress against the frontier.

**Finding 5: no convergence to the frontier.** Output per worker relative to the United States was 18.6% in 1960, 19.5% in 1980, 12.1% in 2000, 18.1% in 2019 and 16.4% in 2023 (`relative_income.csv`, Figure 3). Over the same period Thailand went from about 6% to 24% and Korea from 12% to 67%. Over sixty years the Philippines has gone round in a circle rather than up a slope.

**Finding 6: the speed of convergence is fast enough, so speed alone is not the problem.** A simple regression of the yearly change in ln(K/Y) on last year's gap gives λ ≈ 0.10 for 1980–2019, with a standard error of 0.05. Standard errors measure how uncertain the estimate is. This implies a half-life of about 7 years (`speed_of_convergence.csv`). The estimate is noisy and uses a crude gap measure, so it should not be cited. Still, it suggests that the Philippines *would* reach its steady state within a decade or two if the steady state stood still and nothing hit the economy. The repeated "not quite" therefore points to the target moving and to shocks, more than to slow adjustment.

## 4. Candidate explanations as competing hypotheses

A test between named hypotheses is more informative than a test against zero. The exploration suggests five explanations, which the study can weigh against each other.

**H1, asymptotic approach.** The economy is on an ordinary transition path. The "not quite" is just the exponential shape of equation (4). This predicts a gap that shrinks steadily between shocks, at a roughly constant λ.

**H2, moving target.** The steady state itself keeps shifting. Over 2010–2019 the investment boom and the demographic transition (falling employment growth) both raised (K/Y)\*. The economy chases a target that runs ahead of it. This predicts that changes in the gap are driven mainly by changes in s, n and δ, not by changes in actual K/Y. The 2010–2019 decomposition fits this pattern.

**H3, shocks arrive faster than the economy heals.** The debt crisis of 1983–85, the Asian financial crisis of 1997–98 and the COVID-19 contraction of 2020 each pushed the economy off its path. If large shocks come about once a decade and the half-life is about 7 years, the economy is never given the time to arrive. Easterly, Kremer, Pritchett and Summers (1993) show that country growth rates are much less persistent than country characteristics, which fits this view. This predicts that the gap closes between shocks and jumps at shock dates.

**H4, a low steady state.** The Philippines is close to its *own* steady state, but that steady state is low, because productivity growth g and the productivity level A are low. In this view, not catching up with the frontier is about where the target is, not about distance from it. This links to development accounting, which finds that most cross-country income differences reflect productivity rather than capital (Hall & Jones, 1999; Caselli, 2005). It predicts a small conditional gap alongside a large and stable frontier gap.

**H5, a trap with more than one equilibrium.** The economy may be stuck in a "low-capital-stock equilibrium" (Bocchi, 2008) or a middle-income trap (Felipe, Abdon & Kumar, 2012). In such a trap, forces such as weak infrastructure, low investment and premature deindustrialisation (Rodrik, 2016) keep it from moving to a higher steady state. H5 differs from H4 because it predicts that the economy does not respond to small improvements in the fundamentals. A large push is needed.

These hypotheses are not mutually exclusive. The study's contribution would be to say *how much* of the observed distance each one accounts for in each decade.

## 5. Draft research questions mapped to three objectives

**Objective 1, descriptive: document the distance.** *RQ1.* How has the Philippines' distance from its own steady state evolved from 1960 to the latest year, how does it compare with ASEAN peers and with Korea and China, and how does it relate to the distance from the frontier? This is answered with the gap series in equations (1)–(3), the relative-income series and a dating of the main shocks.

**Objective 2, estimation: explain the distance.** *RQ2.* What is the Philippines' speed of convergence λ to its own steady state, and is it stable across sub-periods and similar to that of its peers? *RQ3.* How much of the change in the gap in each decade comes from movement of the steady state (s, n, δ, A, h) and how much from the economy's own movement? This decomposition tests H2 against H1 and H3. *RQ4.* Is the Philippines converging to the frontier? This is tested by checking whether the log of its income relative to the US settles towards a stable level, allowing for structural breaks (Bernard & Durlauf, 1995). It separates H4 and H5 from H1–H3.

**Objective 3, policy: what would move the target.** *RQ5.* Given the estimated λ and the steady-state equation, how much would a sustained rise in the investment share, in schooling or in productivity growth raise the Philippines' steady state, and how long would the transition take? Each answer should be tied to a specific estimate. Natural benchmarks are the targets in the Philippine Development Plan and the infrastructure programme of the 2010s.

## 6. Candidate reference papers and a recommended design

The workflow replicates a published design before applying it to new data. Three designs fit, and they can be combined.

**Option A (recommended core): Mankiw, Romer and Weil (1992) together with Cho and Graham (1996).** MRW is the standard estimate of the steady-state equation across countries. Its data are public and widely replicated, so the replication gate is well defined: reproduce their Table I and Table II coefficients. Cho and Graham (1996) take the MRW steady-state estimates and ask, for each country, whether it sits above or below its steady state. That is our research question almost word for word. The design is to replicate both on the original 1960–1985 data, re-estimate on PWT 11.0, and read off the Philippines' predicted steady state and its distance from it, decade by decade. This answers RQ1–RQ3 and RQ5.

**Option B (time series): Bernard and Durlauf (1995).** This design tests whether the log income gap with the frontier settles towards a stable level, using time-series methods with breaks. It answers RQ4 and gives H4 against H1–H3 a formal test.

**Option C (context): Kremer, Willis and You (2022), with Patel, Sandefur and Subramanian (2021) and Johnson and Papageorgiou (2020).** These papers show that since the 1990s poorer countries have started to converge on average. They also show that the determinants of steady states, such as policies and institutions, have themselves been converging. This gives the Philippine case a global benchmark: is the Philippines part of the "new era of convergence" or an exception to it?

My recommendation is Option A as the main design, with Option B as Objective 2's second test and Option C for framing the literature review. The choice is yours. It is open question Q1 in `CLAUDE.md`.

## 7. Data feasibility

Everything needed for a first version is public. Penn World Table 11.0 (downloaded, 1950–2023) has capital stocks, depreciation, investment, employment, a human-capital index and TFP for all peers. The Philippine Statistics Authority (PSA) national accounts can extend GDP, investment and employment to 2025. PSA does not, as far as we know yet, publish an official capital stock that matches PWT's. So the latest two years would need the study's own perpetual-inventory extension, which adds each year's investment and subtracts depreciation. That extension would be the study's construction, not an official statistic, and the paper must say so. The original MRW (1992) dataset is public, so the replication gate is feasible. Schooling data (Barro–Lee) and UN population projections would support the human-capital and demographic channels. Nothing in the design requires data that do not exist.

The main measurement risks are three. The first is the price-level correction in Section 3. The second is the choice of g, which drives the level of the gap. The third is that PWT's TFP and capital series are themselves model-based constructions. Each will become a numbered decision with a robustness check.

## 8. What I need from you to move to the next step

- **Your intended meaning of "steady state"**: your own steady state (conditional convergence), the frontier, or steady growth. My recommendation is to make the first the main question and the second the contrast.
- **A choice of reference design**: Option A, B, C or a combination. Also tell me if your adviser has a reference paper in mind.
- **The output format and audience**: journal article, thesis chapter or policy brief, and any formatting template.
- **Any concept note or earlier draft for Publication E**, so the brief matches what you have already written.

## References

All entries were checked on Crossref on 15 October 2026. Two are flagged.

- Barro, R. J., & Sala-i-Martin, X. (1992). Convergence. *Journal of Political Economy, 100*(2), 223–251. https://doi.org/10.1086/261816
- Bernard, A. B., & Durlauf, S. N. (1995). Convergence in international output. *Journal of Applied Econometrics, 10*(2), 97–108. https://doi.org/10.1002/jae.3950100202
- Bocchi, A. M. (2008). *Rising growth, declining investment: The puzzle of the Philippines breaking the "low-capital-stock" equilibrium* (Policy Research Working Paper 4472). World Bank. https://doi.org/10.1596/1813-9450-4472
- Caselli, F. (2005). Accounting for cross-country income differences. In P. Aghion & S. Durlauf (Eds.), *Handbook of Economic Growth* (Vol. 1A, pp. 679–741). Elsevier. https://doi.org/10.1016/S1574-0684(05)01009-9
- Cho, D., & Graham, S. (1996). The other side of conditional convergence. *Economics Letters, 50*(2), 285–290. https://doi.org/10.1016/0165-1765(95)00745-8
- Easterly, W., Kremer, M., Pritchett, L., & Summers, L. H. (1993). Good policy or good luck? Country growth performance and temporary shocks. *Journal of Monetary Economics, 32*(3), 459–483. https://doi.org/10.1016/0304-3932(93)90026-C
- Feenstra, R. C., Inklaar, R., & Timmer, M. P. (2015). The next generation of the Penn World Table. *American Economic Review, 105*(10), 3150–3182. https://doi.org/10.1257/aer.20130954
- Felipe, J., Abdon, A., & Kumar, U. (2012). *Tracking the middle-income trap: What is it, who is in it, and why?* (Working Paper). Levy Economics Institute. https://doi.org/10.2139/ssrn.2069645 *(Flag: Crossref lists the SSRN record under Felipe only; check the co-authors and working-paper number against the PDF.)*
- Hall, R. E., & Jones, C. I. (1999). Why do some countries produce so much more output per worker than others? *Quarterly Journal of Economics, 114*(1), 83–116. https://doi.org/10.1162/003355399555954
- Johnson, P., & Papageorgiou, C. (2020). What remains of cross-country convergence? *Journal of Economic Literature, 58*(1), 129–175. https://doi.org/10.1257/jel.20181207
- Jones, C. I. (2016). The facts of economic growth. In J. B. Taylor & H. Uhlig (Eds.), *Handbook of Macroeconomics* (Vol. 2A, pp. 3–69). Elsevier. https://doi.org/10.1016/bs.hesmac.2016.03.002
- Kremer, M., Willis, J., & You, Y. (2022). Converging to convergence. *NBER Macroeconomics Annual, 36*, 337–412. https://doi.org/10.1086/718672
- Mankiw, N. G., Romer, D., & Weil, D. N. (1992). A contribution to the empirics of economic growth. *Quarterly Journal of Economics, 107*(2), 407–437. https://doi.org/10.2307/2118477
- Patel, D., Sandefur, J., & Subramanian, A. (2021). The new era of unconditional convergence. *Journal of Development Economics, 152*, 102687. https://doi.org/10.1016/j.jdeveco.2021.102687
- Rodrik, D. (2016). Premature deindustrialization. *Journal of Economic Growth, 21*(1), 1–33. https://doi.org/10.1007/s10887-015-9122-3
- Solow, R. M. (1956). A contribution to the theory of economic growth. *Quarterly Journal of Economics, 70*(1), 65–94. https://doi.org/10.2307/1884513
- Swan, T. W. (1956). Economic growth and capital accumulation. *Economic Record, 32*(2), 334–361. https://doi.org/10.1111/j.1475-4932.1956.tb00434.x

*Further reading, to be verified before citing:* Clarete, Esguerra and Hill (Eds.) (2018), *The Philippine Economy: No Longer the East Asian Exception?*, ISEAS (book DOI 10.1355/9789814786621 found; editors still to be confirmed); Balisacan and Hill (Eds.) (2003), *The Philippine Economy: Development, Policies, and Challenges*, Oxford University Press (DOI 10.1093/0195158989.001.0001 found; editors still to be confirmed); Cororaton (2005), Total factor productivity growth in the Philippines: 1960–2000, *Asian Development Review, 22*(1), 97–113 (https://doi.org/10.1142/s0116110505500058).
