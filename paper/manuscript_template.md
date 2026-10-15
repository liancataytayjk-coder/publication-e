---
title: "Approaching but Not Quite: Is the Philippines Converging to Its Own Steady State?"
author: "[Author name], [Affiliation], [email]"
date: "Manuscript draft, October 2026"
---

<#-- Rendered by scripts/08_paper.py. Every number comes from output/tables via the dictionary n; never edit manuscript.md by hand. --#>

**Abstract.** For six decades the Philippines has looked like an economy that has reached its long-run resting point. Its capital-output ratio has hardly moved since 1985, and its GDP per person has stayed at roughly a tenth of the United States level. Yet it never seems to settle. We ask whether the Philippines is approaching its *own* steady state, the long-run path set by its own investment, demography, health, institutions and macroeconomic stability, and why it seems to approach without arriving. We answer with two reference designs that we first replicate: the classic cross-country augmented Solow model of Mankiw, Romer and Weil (1992), and the panel conditional-convergence design of Barro (2015), which corrects for the bias that country fixed effects create. Both are replicated within pre-registered tolerances, then applied to Penn World Table 11.0 for 1960–2023. The two designs agree that convergence is slow: {{ n.lam_A }} to {{ n.lam_B }} percent of any gap closes each year, a half-life of {{ n.hl_B }} to {{ n.hl_A }} years. They disagree on the sign of the current gap. Most of that disagreement disappears once both use current rather than past population growth, and both then place the Philippines close to its steady state. A decomposition shows why the gap does not close. Since 1985, convergence has closed about {{ n.dec_post_closing }} log points of distance, but the steady state itself has risen by about {{ n.dec_post_target_move }} log points more than its trend, mainly through falling fertility and longer lives. Crises in 1984–85, 1997–98 and 2020 also pushed the economy off its path. The Philippines is chasing a target that keeps moving up.

**Keywords:** steady state; conditional convergence; Solow model; Philippines; dynamic panel bias; demographic transition.
**JEL codes:** O47, O53, E13, C23.

# 1. Introduction

Ask a Philippine economist whether the country has "arrived" and the answer is usually some version of "almost". The economy grew by {{ n.g_PHL_2010_2019 }} percent a year per person in 2010–2019, its fastest decade since at least 1960. Its capital-output ratio has stayed between {{ n.ky_min }} and {{ n.ky_max }} in every year from 1985 to 2019, which is the behaviour textbooks associate with an economy on its long-run path [@jones2016]. Yet the same economy produced {{ n.rel_PHL_1960 }} percent of United States GDP per person in 1960 and {{ n.rel_PHL_2023 }} percent in 2023. Over that period Thailand went from {{ n.rel_THA_1960 }} to {{ n.rel_THA_2023 }} percent and Korea from {{ n.rel_KOR_1960 }} to {{ n.rel_KOR_2023 }} percent (Figure 1). The Philippines seems to approach something without ever getting there.

This paper turns that impression into a measurable question. In the neoclassical growth model of @solow1956 and @swan1956, every economy moves towards its own **steady state**: the path on which capital per effective worker, and hence income per person relative to technology, stops changing. The steady state is *conditional*. It depends on the country's own saving, population growth, schooling and, in later extensions, its health, institutions and macroeconomic policy [@mrw1992; @barrosala1992]. A poor country need not converge to the United States. It converges to *its* steady state, which may itself be low. We ask three things about the Philippines. First, how far is it from its own steady state, and is that distance shrinking? Second, how fast does it close the distance? Third, if it closes the distance at all, why does it never seem to arrive?

We answer with two reference designs, chosen to give two independent views of the same question. The first is the classic: the augmented Solow model of @mrw1992 ("MRW"), estimated on a cross-section of countries. Following the logic of @chograham1996, MRW's fitted convergence equation tells us where each country's steady state lies, and therefore how far each country sits above or below it. The second is more recent and pays closer attention to econometric pitfalls: the panel conditional-convergence design of @barro2015. It estimates convergence from five-year growth rates within a panel of about one hundred countries, holding constant a rich set of steady-state determinants. It also argues carefully that adding country fixed effects, an apparently harmless way to allow each country its own steady state, badly overstates the speed of convergence when the panel is short [@nickell1981; @barro2015]. Before using either design on new data we reproduce each paper's published results, with pass ranges fixed in advance. We then apply both to Penn World Table 11.0 [@feenstra2015] for 1960–2023, with the Philippines as the focus.

The two designs give a clear answer on speed and a more interesting answer on distance. On speed they agree. The Philippines, like the average country, closes about {{ n.lam_A }}–{{ n.lam_B }} percent of the gap to its steady state each year. That means half of any gap takes {{ n.hl_B }}–{{ n.hl_A }} years to close, close to the "iron law" of two percent [@barrosala1992]. On the current distance they disagree, and the reason is informative. The MRW design measures the Philippine steady state with population growth averaged over the past 25 years, which was fast. It therefore sees a low steady state that the Philippines has already overtaken. The Barro design measures it with current fertility, which has fallen close to replacement, and sees a higher steady state that the Philippines has not yet reached. Once the MRW design uses current population growth too, the two designs move most of the way together, and both place the Philippines within about a quarter of a log point of its steady state. The steady state is moving up because the demographic transition is under way, and the two designs catch it at different points.

The decomposition in Section 5 shows why the Philippines seems to approach without arriving. From 1985 to 2020 the closing of the gap through convergence was almost exactly offset by the steady state rising faster than its trend, mainly because fertility fell and lives lengthened faster than in the rest of the world. Shocks did the rest: the debt crisis of 1984–85, the Asian financial crisis and the COVID-19 contraction each pushed income away from its path. The distance in 2020 ({{ n.dB_2020 }} log points in the Barro design) is almost the same as in 1985 ({{ n.dB_1985 }}). The Philippines is not stuck. It is running towards a target that keeps moving.

The paper makes three contributions. It brings two canonical convergence designs to bear on one country's steady state and reports where they agree and where they do not, rather than choosing one. It shows how to turn a convergence regression into an exact accounting of why a gap persists, separating convergence, the movement of the steady state, and shocks. And it documents a practical lesson for applied work: a country's estimated steady state depends on whether its demography is measured as it was or as it is, which matters most for countries in the middle of their demographic transition. Section 2 sets out the concepts and hypotheses, Section 3 the related literature, Section 4 the data and methods, Section 5 the results and Section 6 the discussion.

# 2. Concepts and hypotheses

**The steady state.** Output per person grows for two reasons in the Solow model: technology improves, and capital per worker rises. The second force fades as capital accumulates, because each extra machine adds less than the one before. The steady state is the path on which the second force has died out, so that income per person grows only at the rate of technology, g\*. We write the steady-state level of log income per person at date t as $\ln y^*_t$. *Example:* if the Philippine steady state in 2020 were 9.3 and actual log income were 9.05, the Philippines would be 0.25 log points, or about 22 percent, below its steady state.

**Distance from the steady state.** We call the gap the distance:

$$d_t = \ln y_t - \ln y^*_t. \qquad (1)$$

A negative d means the economy is below its steady state and should grow faster than g\*. A positive d means it is above and should grow more slowly.

**Speed of convergence.** Near the steady state the economy closes a constant share λ of the remaining distance each year:

$$d_{t+\tau} = e^{-\lambda \tau} d_t, \qquad \text{half-life} = \frac{\ln 2}{\lambda}. \qquad (2)$$

*Example:* with λ = 0.02, half of any distance closes in 35 years and three-quarters in 69 years. Because a constant *share* closes each year, the distance shrinks but never reaches exactly zero. Part of "approaching but not quite" is therefore built into the theory.

**From a growth regression to the steady state.** Both reference designs estimate a growth regression. Over a period of τ years, annual growth of income per person is regressed on log income at the start and on the determinants of the steady state:

$$\frac{\ln y_{i,t+\tau} - \ln y_{i,t}}{\tau} = a_t + b \ln y_{i,t} + X_{i,t}'\gamma + e_{i,t}. \qquad (3)$$

The coefficient b is negative when poorer countries, *given their determinants X*, grow faster. It maps into the speed of convergence through $b = -(1 - e^{-\lambda \tau})/\tau$. Predicted growth minus steady-state growth equals b times the distance, so the distance can be recovered from the fitted regression:

$$d_{i,t} = \frac{\hat g_{i,t} - g^*}{b}, \qquad \hat g_{i,t} = \tilde a_t + b \ln y_{i,t} + X_{i,t}'\hat\gamma. \qquad (4)$$

*Example:* if the model predicts that the Philippines will grow at 2.4 percent a year when the steady-state rate is 2 percent, and b = −0.02, then d = (0.024 − 0.020)/(−0.02) = −0.20. The Philippines is 0.20 log points below its steady state. This is the logic @chograham1996 applied to the MRW equations. As in MRW, we set g\* = 0.02.

**Why the gap may persist: an exact decomposition.** Equations (3) and (4) imply an identity for the change in distance between two period starts:

$$\Delta d_t = \underbrace{\tau b\, d_t}_{\text{closing}} + \underbrace{\tau (a_t - \tilde a_t)}_{\text{world shock}} + \underbrace{\tau e_{i,t}}_{\text{country shock}} - \underbrace{(\Delta \ln y^*_t - g^* \tau)}_{\text{steady state moving}}. \qquad (5)$$

The first term is convergence. It is positive when the economy starts below its steady state, because convergence raises d towards zero. The second and third terms are shocks: world-wide surprises in growth, measured as deviations of the time effects $a_t$ from their trend $\tilde a_t$, and surprises specific to the country, the regression residual. The last term is the movement of the steady state beyond its trend growth g\*. If the steady state rises faster than g\*, the economy has to run just to keep its distance. Equation (5) holds exactly, so every movement in the Philippine distance can be assigned to one of these sources.

**Hypotheses.** The identity gives four competing explanations for "approaching but not quite". Each comes with a decision rule fixed before the estimates were seen. **H1, ordinary convergence:** the Philippines is below its steady state and the distance trends towards zero. **H2, a moving target:** the steady state rises faster than trend, by at least half as much as convergence closes. **H3, shocks:** large negative shocks hit in at least two of the three crisis periods named in advance (1980–85, 1995–2000 and 2015–20). **H4, a low own steady state:** the Philippines grows persistently less than its determinants predict, so that something specific to the country, not captured by X, holds its steady state down. Figure 9 summarises the framework.

# 3. Related literature

The empirical study of steady states began with MRW, who showed that differences in saving, population growth and schooling explain most of the cross-country variation in income. They also showed that, holding these constant, poorer countries grow faster at about two percent a year. @barrosala1992 found the same rate across United States states and countries, and @islam1995 and @caselli1996 moved the analysis to panels. Panels allow each country its own unobserved steady state, through country fixed effects, and they deal with endogenous regressors. These estimates suggested much faster convergence. @barro2015 argued that much of that speed is an artefact. With ten or so time periods, the fixed-effects estimator of a dynamic equation is biased towards faster convergence [@nickell1981; @kiviet1995]. In a long panel since 1870 the bias is small and convergence is about 2.4 percent a year. In the post-1960 panel, controlling for observed determinants without fixed effects gives about 1.7 percent. Recent work finds that unconditional convergence has emerged since the 1990s, partly because the determinants of steady states have themselves converged [@patel2021; @kremer2022; @johnson2020]. Our decomposition makes that idea concrete for one country: it measures how much of the change in the gap comes from the determinants moving.

On bias correction, @dhaene2015 propose the split-panel jackknife and @gourieroux2010 indirect inference. In our simulations (Section 4.5) the jackknife over-corrects in panels as short and persistent as ours, so we use indirect inference. On the role of shocks, @easterly1993 show that growth rates are far less persistent than country characteristics, so shocks explain much of the variation in decade growth. @pritchett2000 documents how often developing economies switch between growth regimes. On demography, @bloom1998 attribute a large part of East Asia's growth to the demographic transition, which is the channel that matters most for the Philippines here.

Work specific to the Philippines has long described a low-investment economy whose growth repeatedly stopped and started. @bocchi2008 describes a "low-capital-stock equilibrium" in which growth rose in the 2000s while investment fell. @cororaton2005 measures total factor productivity growth over 1960–2000. Development accounting shows that cross-country income gaps are mostly productivity gaps [@halljones1999; @caselli2005]. None of these studies asks how far the Philippines is from its own steady state, or why the distance persists. That is the gap this paper fills.

# 4. Data and methods

## 4.1 Data

Table A1 lists every variable, its source and its use. The main source is Penn World Table 11.0 [@feenstra2015], covering 185 countries from 1950 to 2023. It provides real GDP comparable across countries and over time, population, employment, investment and government-consumption shares, and price levels for exports and imports. Life expectancy, fertility, inflation, working-age population, the population aged 15–19 and secondary enrolment come from the World Bank's World Development Indicators. Years of schooling by sex come from the Barro–Lee data set [@barrolee2013]. Barro used the International Country Risk Guide's law-and-order index, which is proprietary, and Freedom House's political-rights index. We use the public V-Dem rule-of-law and electoral-democracy indices in their place [@vdem2025]. The replication uses each paper's own data: the MRW data set and Penn World Table 7.0. All series are official statistics or published research data. The distances, decompositions and groupings are this study's own constructions. Every raw file is stored unchanged and logged with its source and checksum.

## 4.2 Method A: Mankiw, Romer and Weil (1992)

MRW estimate equation (3) once, across countries, over a 25-year window:

$$\ln y_{i,T} - \ln y_{i,0} = c + b \ln y_{i,0} + \gamma_1 \ln s_{k,i} + \gamma_2 \ln(n_i + g + \delta) + \gamma_3 \ln \text{SCHOOL}_i + e_i, \qquad (6)$$

Here y is real GDP per working-age person, $s_k$ the investment share of GDP, n the growth rate of the working-age population, and g + δ = 0.05 the sum of technology growth and depreciation (MRW's value). SCHOOL is the share of the working-age population in secondary school, which stands in for investment in human capital. Equation (6) is estimated by ordinary least squares (OLS), with conventional standard errors as in MRW. The speed of convergence is λ = −ln(1 + b)/25. We build modern versions of MRW's variables: investment from Penn World Table, working-age population from the World Bank, and SCHOOL as secondary gross enrolment times the share of 15–19-year-olds in the working-age population, MRW's own construction. We estimate equation (6) for rolling windows 1960–1985, 1965–1990, …, 1995–2020 and 1998–2023. Each window uses countries with at least one million people at its start and oil rents below 20 percent of GDP, the modern counterpart of MRW's "non-oil" sample. The Philippine distance at the start of a window is $d_0 = (\hat\Delta - g^* T)/b$, from equation (4) applied to the whole window. At the end of the window it is $d_T = d_0 + (\Delta - g^* T)$, which uses actual growth Δ.

## 4.3 Method B: Barro (2015)

Barro estimates equation (3) on a panel of five-year periods. The dependent variable is the annual growth rate of real GDP per person over each period. The regressors are log GDP per person at the start of the period, time effects (one constant per period, which absorbs world-wide booms and slumps), and determinants averaged over the period: the reciprocal of life expectancy, log fertility, rule of law, the investment share, years of schooling by sex, the government-consumption share, openness to trade, democracy and its square, and inflation (capped at 100 percent a year). A terms-of-trade term is added: the growth of export relative to import prices, times openness. Barro treats this as a temporary influence on growth, not a steady-state determinant, and so do we when computing distances. Income and the period-average determinants respond to growth within the period, so they are instrumented with values from before the period: log income one year earlier and averages from the previous period. The equation is estimated by two-stage least squares, with standard errors clustered by country so that each country's errors may be correlated over time. The sample follows Barro's rule: countries with data starting by the 1965–70 period and at least half a million people in 1990. That gives {{ n.ncty_B }} countries and {{ n.nobs_B }} country-periods from 1965–70 to 2020–23. The Philippine distance at each period start comes from equation (4). The trend $\tilde a_t$ of the time effects replaces the time effects themselves, so that a world recession is counted as a shock rather than as a fall in the Philippine steady state.

## 4.4 Fixed effects and their bias

A natural way to give each country its own steady state is a country fixed effect: a separate constant for each country. With few time periods this biases b towards faster convergence, because the country mean of income contains the very shocks the regression tries to separate from convergence [@nickell1981]. We report the fixed-effects estimate and a corrected version. The correction uses indirect inference [@gourieroux2010]: it finds the true speed of convergence and the spread of starting gaps that, in simulated panels of our exact size, reproduce both the fixed-effects estimate and the observed variation of income within countries.

## 4.5 Validation and pre-registration

We checked the estimators before using them. Simulation tests confirm that our two-stage least squares estimator recovers a known speed of convergence when the steady state is observed. They show that fixed effects in a ten-period panel roughly double the speed when the true value is two percent, as Barro warned. They show that the split-panel jackknife of @dhaene2015 over-corrects in panels this short and persistent, and that indirect inference removes most of the bias. The tests also confirm that equation (4) recovers a known distance exactly. We then wrote down a replication gate before running any replication. It has seventeen criteria, each with a target and a pass range: MRW Tables I, II, V and VI on MRW's data, and Barro's Table 1, columns 1 and 2, on Penn World Table 7.0. The estimation plan (samples, variables, the value of g\*, the hypotheses and their decision rules, the rule for judging whether the two methods agree, and a menu of robustness checks) was written and committed before any estimate on new data. We label everything else as *supplementary*, meaning specified before running but after seeing the main results, or as *exploratory*. One correction was made after the first run: in the pre-registered plan the terms-of-trade term was wrongly counted as a steady-state determinant. Section 5.7 reports both versions.

Uncertainty comes from a bootstrap that resamples countries (499 draws). Each draw re-estimates the model and recomputes the Philippine quantities, and we report 90 percent intervals.

# 5. Results

## 5.1 The Philippine growth path (RQ1)

Table 2 shows growth of real GDP per person by decade. The Philippines grew {{ n.g_PHL_1970_1980 }} percent a year in the 1970s, shrank by {{ n.g_PHL_1980_1990 | replace("−", "") }} percent a year in the 1980s, grew {{ n.g_PHL_1990_2000 }} percent in the 1990s, {{ n.g_PHL_2000_2010 }} percent in the 2000s and {{ n.g_PHL_2010_2019 }} percent in 2010–2019, then {{ n.g_PHL_2019_2023 }} percent over 2019–2023. Over 1960–2023 it averaged {{ n.g_PHL_1960_2023 }} percent, about the same as the United States. That is why its relative income barely changed. GDP per person fell by more than two percent in {{ n.shock_years }}, including falls of {{ n.shock_1984 | replace("−", "") }} percent in 1984 and {{ n.shock_2020 | replace("−", "") }} percent in 2020. Figure 2 shows the exploratory capital-output calculation that motivated the paper. The ratio has been flat since 1985, but its implied steady-state value rose in the 2010s as investment rose.

## 5.2 Replication

The replication gate passed on all {{ n.gate_n }} criteria (Table 1, Figure 3). On MRW's own data our estimates match the published coefficients to the second decimal. On Penn World Table 7.0 we rebuild Barro's sample exactly: 80 countries and {{ n.barro_nobs }} country-periods. Without fixed effects the coefficient on lagged income is {{ n.barro_c1 }} (standard error {{ n.barro_c1_se }}; published 0.0019), and with fixed effects it is {{ n.barro_c2 }} ({{ n.barro_c2_se }}; published −0.0326). The R² values are {{ n.barro_c1_r2 }} and {{ n.barro_c2_r2 }} (published 0.095 and 0.381). As an indicative check outside the gate, Barro's column 3, rebuilt with the public V-Dem indices in place of the proprietary ones, gives {{ n.barro_c3 }} ({{ n.barro_c3_se }}) against his −0.0171 (0.0022). Both designs therefore reproduce their originals before we use them on new data.

## 5.3 How far is the Philippines from its own steady state? (RQ2)

Table 3 and Figure 4 show the Philippine distance d over time. In Method B the Philippines starts far below its steady state in 1965 ({{ n.dB_1965 }}), rises above it by 1980 ({{ n.dB_1980 }}), falls back below it in the 1984–85 crisis, and then stays below it at every period start from 1985 to 2020, with d between {{ n.dB_min }} and {{ n.dB_max }}. In 2020 the distance is {{ n.dB_2020 }}: income about {{ n.dB_pct }} percent below the steady state. The 90 percent interval runs from {{ n.dB_2020_lo }} to {{ n.dB_2020_hi }}{% if n.dB_band_has_zero_after_1965 %}, and the interval includes zero at every date after 1965{% endif %}. Method A, using the MRW determinants, tells a different story. The Philippines is well below its steady state at the end of the 1960–1985 window ({{ n.dA_1985 }}) but above it from 2000 onwards: {{ n.dA_2020 }} in 2020 (interval {{ n.dA_2020_lo }} to {{ n.dA_2020_hi }}) and {{ n.dA_2023 }} in 2023 ({{ n.dA_2023_lo }} to {{ n.dA_2023_hi }}).

The pre-registered agreement rule asks for three things in 2020: the same sign, overlapping intervals, and each method's speed of convergence inside the other's interval. {% if n.agree_sign %}The signs agree{% else %}The signs disagree{% endif %}, {% if n.agree_overlap %}the intervals overlap{% else %}the intervals do not overlap{% endif %}, and {% if n.agree_lambda %}the speeds agree{% else %}the speeds agree only one way (Section 5.4){% endif %}. By our own rule, then, the two methods do not converge on one answer for the level of the distance. The two Philippine paths are also negatively correlated over 1985–2020 ({{ n.agree_corr }}). We report this as it is, and Section 5.5 investigates why.

## 5.4 How fast does the gap close? (RQ3)

Here the two designs agree much more closely (Figure 6). In Method B, b = {{ n.b_B }}, which implies λ = {{ n.lam_B }} percent a year (90 percent interval {{ n.lam_B_lo }}–{{ n.lam_B_hi }}) and a half-life of {{ n.hl_B }} years. In Method A, λ is between {{ n.lam_A_min }} and {{ n.lam_A_max }} percent in every window. In the latest window (1998–2023) it is {{ n.lam_A }} percent ({{ n.lam_A_lo }}–{{ n.lam_A_hi }}), a half-life of {{ n.hl_A }} years. Method A's estimate lies inside Method B's interval, but not the other way round. Adding country fixed effects raises λ to {{ n.lam_fe }} percent (half-life {{ n.hl_fe }} years). Correcting the fixed-effects estimate for its bias brings it back to {{ n.lam_fc }} percent (half-life {{ n.hl_fc }} years), which confirms Barro's argument on modern data. Every credible estimate lies between about one and two and a half percent. Whatever the Philippine distance is, half of it takes three to six decades to close.

## 5.5 Why the two methods disagree on the distance (supplementary)

Three supplementary checks, specified after the agreement rule failed, locate the source of the disagreement. The first swaps the sets of determinants. Method B with only the MRW determinants still puts the Philippines below its steady state ({{ n.r1_d }} in 2020). Method A with Barro's determinants added still puts it above ({{ n.r2_d }}). So the panel and the cross-section differ even with the same variables.

The second check decomposes each method's Philippine steady state into the contributions of its determinants, relative to the sample average (Table 4). In Method A one item dominates. Philippine working-age population grew {{ n.n_window }} percent a year over 1995–2020, faster than {{ n.n_pctile }} percent of the countries in the sample (median {{ n.n_median }} percent). In the MRW model fast population growth spreads capital thinly, so this alone lowers the Philippine steady state by {{ n.cA_ngd | replace("−", "") }} log points. The low investment rate subtracts a further {{ n.cA_inv | replace("−", "") }}. In Method B the corresponding demographic variable is *current* fertility, which in the Philippines is now below the sample average, and it *raises* the steady state by {{ n.cB_fert }}. Low inflation adds {{ n.cB_infl }}. Weak rule of law subtracts {{ n.cB_rule | replace("−", "") }}.

The third check measures population growth in Method A over the last five years of each window instead of its average over 25 years: {{ n.n_current }} rather than {{ n.n_window }} percent for the Philippines. The Philippine distance then falls from {{ n.dA_2020 }} to {{ n.r3_d2020 }} in 2020, and from {{ n.dA_2023 }} to {{ n.r3_d2023 }} in 2023. That lies well inside Method B's interval, though still on the other side of zero from Method B's point estimate.

The two methods are therefore measuring the same moving object at different moments. A cross-section over 25 years sees the steady state of a country with fast population growth. A panel of five-year periods sees the steady state of a country whose fertility has already fallen. With current demography in both, the Philippines is close to its steady state: within about a quarter of a log point of it, a gap neither method can distinguish from zero with confidence. This reconciliation is supplementary and should be read as such.

## 5.6 Why "approaching but not quite"? (RQ4)

Table 5 and Figure 5 apply the identity (5) to the Philippines in Method B. The terms add up exactly in every period (largest discrepancy {{ n.dec_maxcheck }}). Two eras stand out.

*1965–1985.* The steady state fell sharply relative to its trend (by {{ n.dec_pre_target_move | replace("−", "") }} log points). High inflation, a weakening rule of law and rising government consumption all lowered it. As a result the Philippines found itself *above* its steady state by 1980, without any acceleration of its own. Then the 1984–85 crisis struck: the shocks in 1980–85 sum to {{ n.shock_1980 }} log points.

*1985–2020.* Convergence closed {{ n.dec_post_closing }} log points of distance, but the steady state rose {{ n.dec_post_target_move }} log points faster than its two-percent trend, so the two almost cancelled. Shocks netted {{ n.dec_post_ph_shock }} (Philippine) and {{ n.dec_post_world_shock }} (world). The distance in 2020 was therefore almost identical to that in 1985. Most of the rise in the steady state came from fertility ({{ n.mv_fert }}) and life expectancy ({{ n.mv_life }}), offset by the world trend ({{ n.mv_trend }}): demographic improvements raise the Philippine steady state only to the extent that they outpace the rest of the world's. Lower inflation added {{ n.mv_infl }}, investment {{ n.mv_inv }}, and schooling {{ n.mv_school }}.

Against the pre-registered decision rules the hypotheses fare as follows. **H1** (ordinary convergence) is {% if n.H1_ok %}supported{% else %}not supported{% endif %}: {{ n.H1_val }}. The Philippines has been below its steady state on average but has not been closing on it. **H2** (moving target) is {% if n.H2_ok %}supported{% else %}not supported over 1965–2020{% endif %} ({{ n.H2_val }}), because the fall of the steady state before 1985 offsets its rise afterwards. As an *exploratory* reading, H2 holds clearly after 1985: the steady state rose by {{ n.dec_post_target_move }}, more than half the closing term of {{ n.dec_post_closing }}. **H3** (shocks) is {% if n.H3_ok %}supported{% else %}not supported{% endif %}: the combined shocks were negative in all three named crisis periods ({{ n.H3_val }}). **H4** (a low own steady state) is {% if n.H4_ok %}supported{% else %}not supported{% endif %}: the average Philippine residual is {{ n.resid_ph }} (interval {{ n.resid_lo }} to {{ n.resid_hi }}). The Philippines grows about as fast as its determinants predict. Its steady state is low because its determinants are weak, not because of some unexplained national handicap. Allowing for the residual barely moves the distance ({{ n.d_own_2020 }} in 2020).

## 5.7 Robustness

Table 6 and Figure 7 report the pre-registered robustness menu. In Method B the Philippine distance at the latest date is negative in {{ n.robB_neg }} of {{ n.robB_n }} checks. It turns positive only when g\* is raised to 2.5 percent ({{ n.rob_g025 }}) and in the pre-registered version that wrongly treats the terms of trade as a steady-state determinant ({{ n.rob_B0 }}). The *level* of the distance is the most fragile number in the paper. Lowering g\* to 1.5 percent moves it to {{ n.rob_g015 }}. Choosing the g\* at which the United States sits on its steady state on average ({{ n.g_us }} percent) gives {{ n.rob_gus }}. Using raw rather than smoothed time effects gives {{ n.rob_raw }}, because 2020–23 was a rebound period. The g\* implied by the trend of the time effects ({{ n.rob_te_g }} percent) is not meaningful, and we exclude it from the figure. In Method A the distance is positive in all {{ n.robA_n }} checks, from {{ n.robA_min }} to {{ n.robA_max }}, but it is smallest under the restricted form ({{ n.rob_A1 }}), in per-capita terms ({{ n.rob_A3 }}) and with g\* = 1.5 percent ({{ n.rob_Ag015 }}). The speed of convergence is far more stable: across the Method B checks without fixed effects it ranges from {{ n.robB_lam_min }} to {{ n.robB_lam_max }} percent.

## 5.8 What would move the steady state? (RQ5)

Table 7 and Figure 8 ask how much the Philippine steady state would rise if each determinant moved to the median of four neighbours: Indonesia, Malaysia, Thailand and Viet Nam. In Method B the largest gains come from health and demography. Life expectancy at the peer median would add {{ n.pol_life }} log points and fertility {{ n.pol_fert }}. Openness would add {{ n.pol_open }}, but investment only {{ n.pol_invB }}, because once income and other determinants are held constant and the investment share is instrumented, investment adds little, as in Barro's results. Method A attributes much more to investment: {{ n.pol_invA }} log points if the Philippine investment rate rose to the peer median. The two designs therefore disagree most on investment. That is consistent with the concern, which motivates Barro's use of lagged instruments, that cross-section estimates partly reflect causation running from income to investment [@barro2015]. Any of these gains would arrive slowly: at the estimated speeds, half of the resulting gap closes in {{ n.hl_B }} to {{ n.hl_A }} years.

# 6. Discussion and conclusion

**What the evidence says.** Is the Philippines approaching its own steady state? Our answer is that it is near it, close enough that neither method can say with confidence on which side it stands, and moving towards it at the standard slow speed. It does not arrive because the target keeps moving. Between 1965 and 1985 the steady state fell as inflation and weakening institutions lowered it, and the Philippines found itself above a declining target just before the debt crisis. Since 1985 the steady state has risen faster than trend as fertility fell and health improved, and convergence has only just kept pace. The crises of 1984–85, 1997–98 and 2020 cost years of progress each time. We find no evidence of a uniquely Philippine handicap: the country grows about as fast as its determinants predict.

**Why the two reference designs differ, and what that teaches.** The user of either design alone would reach a confident but opposite conclusion. The classic cross-section says the Philippines has overshot a low steady state. The panel says it is a fifth below a higher one. The difference comes from measuring demography as it was rather than as it is, in a country moving fast through its demographic transition. For countries in that position, steady-state estimates built on long-window averages will lag the truth.

**Policy.** Three implications follow, each tied to a specific estimate. First, because the steady state rather than the speed of convergence is what policy can move, the large estimated gains from health and demography ({{ n.pol_life }} and {{ n.pol_fert }} log points at peer levels) point to continued investment in health and in the conditions behind the fertility decline. Second, macroeconomic stability matters for the steady state: falling inflation was one of the largest contributors to its rise after 1985. Third, the payoff from investment is uncertain: large in the cross-section ({{ n.pol_invA }}), small in the panel ({{ n.pol_invB }}). Investment-led strategies should not be sold on the cross-section estimate alone. Because half of any gain takes three to six decades to arrive, avoiding the crises that repeatedly knocked the economy off its path may be worth as much as raising the target.

**Limitations.** The level of the distance depends on the assumed steady-state growth rate g\*, on how world shocks are separated from trend, and on the method; we report all of these rather than choosing one. Public V-Dem indices replace Barro's proprietary institutional measures, and the replication of his column 3 is indicative only. Barro's targets come from the 2012 working-paper version of his article. Penn World Table 11.0 ends in 2023, so the post-COVID recovery is only partly observed. The reconciliation in Section 5.5 and the post-1985 reading of H2 were specified after the main results were seen and are labelled accordingly. The steady state is a model concept: the numbers here measure distance from the steady state *implied by each model*, not from an observable quantity.

**Conclusion.** The Philippines looks as if it is approaching a steady state because, by the standard measures, it is close to one and closing slowly. It never quite arrives because the steady state has been moving, down before 1985 and up since, while crises keep resetting the clock. Raising the target and avoiding the setbacks are the two levers that remain.

# Declarations

**Funding:** [to be completed]. **Competing interests:** none declared [to be confirmed]. **Data and code availability:** all data are public, and every raw file, script and output is in the replication repository; `run_all.sh` rebuilds every number, table and figure from the raw files. **Use of AI tools:** [to be completed by the author in line with the journal's policy].

# References

::: {#refs}
:::

# Tables

**Table 1. Replication of the reference papers.** Published coefficients against this study's estimates on the original data. Standard errors in parentheses where the gate used them. All {{ n.gate_n }} pre-registered criteria pass.

{{ t.replication }}

**Table 2. Growth of real GDP per person by period (percent a year).** Penn World Table 11.0, national-accounts series (rgdpna per person).

{{ t.growth }}

**Table 3. The Philippine distance from its own steady state, d = ln y − ln y\*.** Method B: start of each five-year period, with 90 percent country-bootstrap bands (499 draws). Method A: end of each 25-year window, with 90 percent bands. Negative values mean below the steady state. g\* = 0.02.

{{ t.distance }}

**Table 4. Contributions of each determinant to the Philippine steady state, relative to the sample mean (log points).** Method A: window 1995–2020. Method B: period 2020–23. Supplementary.

{{ t.contrib }}

**Table 5. Why the distance persists: decomposition of the change in d (Method B, log points).** Change in d = closing + world shock + Philippine shock − steady state moving (equation 5). The "− steady state moving" column is the negative of the steady state's rise above its 2 percent trend.

{{ t.decomp }}

**Table 6. Robustness checks.** Speed of convergence λ and the Philippine distance d at the latest date. B0 is the pre-registered treatment of the terms of trade; the main specification moves it to the shocks (see Section 4.5).

{{ t.robust }}

**Table 7. Steady-state gains if each Philippine determinant moved to the ASEAN-4 median (Indonesia, Malaysia, Thailand, Viet Nam).** Latest period. Gains are changes in ln y\*. "Years to half" is the half-life at each method's estimated speed of convergence.

{{ t.policy }}

**Table 8. Method B estimates (two-stage least squares, time effects, no fixed effects; {{ n.ncty_B }} countries, {{ n.nobs_B }} observations, R² {{ n.r2_B }}) and Method A estimates (OLS, 1998–2023, {{ n.nobs_A }} countries, adjusted R² {{ n.r2_A }}).** Standard errors in parentheses; \*, \*\*, \*\*\* significant at 10, 5 and 1 percent.

{{ t.coef_B }}

{{ t.coef_A }}

**Table A1. Variables and sources.**

| Variable | Symbol | Source | Coverage | Use |
| --- | --- | --- | --- | --- |
| Real GDP (expenditure side, chained PPPs) | rgdpe | Penn World Table 11.0 | 1950–2023 | Method B income and growth |
| Real GDP (output side) and national-accounts growth | rgdpo, rgdpna | Penn World Table 11.0 | 1950–2023 | Method A levels and growth |
| Population | pop | Penn World Table 11.0 | 1950–2023 | per-person measures |
| Investment and government-consumption shares | csh_i, csh_g | Penn World Table 11.0 | 1950–2023 | s_k; Method B determinants |
| Export and import price levels | pl_x, pl_m | Penn World Table 11.0 | 1950–2023 | terms of trade |
| Exports, imports, GDP at current national prices | v_x, v_m, v_gdp | Penn World Table 11.0 | 1950–2023 | openness |
| Working-age population (15–64) | wap | World Development Indicators | 1960–2025 | n, y per working-age person |
| Secondary gross enrolment; population 15–19 by sex | — | World Development Indicators | 1970–2025 | SCHOOL |
| Life expectancy, fertility, CPI and GDP-deflator inflation, oil rents | — | World Development Indicators | 1960–2025 | Method B determinants; sample |
| Years of schooling, ages 25–64, by sex | yrs_f, yrs_m | Barro–Lee v3 | 1950–2015 (5-yearly) | Method B determinants |
| Rule of law; electoral democracy | — | V-Dem via Our World in Data | 1789–2025 | Method B determinants |
| MRW data set | — | Mankiw, Romer & Weil (1992) | 1960–1985 | replication |
| Real GDP per person (chain) | rgdpch | Penn World Table 7.0 | 1950–2009 | replication of Barro |

# Figures

![Figure 1. GDP per person relative to the United States, 1960–2023 (percent; Penn World Table 11.0, rgdpe per person). The Philippines (solid line, filled circles) compared with Thailand, Indonesia and Malaysia.](../output/figures/fig1_relative_income.png){width=85%}

![Figure 2. The Philippine capital-output ratio in national prices and its implied steady-state value s/(n + g + δ), with 10-year averages of s, n and δ and g = 0.02. Exploratory calculation from Penn World Table 11.0.](../output/figures/fig2_capital_output.png){width=85%}

![Figure 3. Replication gate. Each dot is this study's estimate minus the published value, divided by half the width of its pre-registered pass band; the grey band is the pass range. All criteria pass.](../output/figures/fig3_replication.png){width=85%}

![Figure 4. The Philippine distance from its own steady state, d = ln y − ln y\* (log points). Solid line: Method B (Barro panel), with the grey band showing the 90 percent country-bootstrap interval. Squares with bars: Method A (MRW cross-section), end of each 25-year window, with 90 percent intervals. Below zero means below the steady state.](../output/figures/fig4_distance.png){width=85%}

![Figure 5. Decomposition of the change in the Philippine distance by five-year period (Method B, log points). Bars stack the four terms of equation (5); circles show the total change in d.](../output/figures/fig5_decomposition.png){width=85%}

![Figure 6. Speed of convergence λ (percent of the gap closed per year) across methods and specifications, with 90 percent intervals where available. The dotted line marks two percent.](../output/figures/fig6_speed.png){width=85%}

![Figure 7. Robustness: the Philippine distance at the latest date under each pre-registered check. Circles: Method B; squares: Method A.](../output/figures/fig7_robustness.png){width=85%}

![Figure 8. Gains in the Philippine steady state (log points × 100) if each determinant moved to the ASEAN-4 median. Grey: Method B; white: Method A.](../output/figures/fig8_policy.png){width=85%}

![Figure 9. Conceptual framework. Determinants set the steady-state path; shocks push actual income off it; convergence closes the distance at speed λ. Dashed: policy levers.](../output/figures/fig9_framework.png){width=85%}
