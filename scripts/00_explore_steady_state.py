"""Exploratory look: how far is the Philippines from its Solow steady state?

EXPLORATORY (Phase 1 feasibility check). Nothing here is a pre-registered
estimate. It exists to decide whether the research question can be answered
with public data and which measures are worth formalising.

Idea. In the Solow model the steady state is the point where capital per
effective worker stops changing. There the capital-output ratio is constant:

    (K/Y)* = s / (n + g + delta)                                        (1)

where s is the investment share of GDP, n employment growth, g labour-augmenting
technology growth and delta the depreciation rate. Output per worker is

    y = A^(1/(1-a)) * (K/Y)^(a/(1-a)) * h                               (2)

so, holding technology A and human capital h fixed, the distance of output per
worker from its steady-state path is (a/(1-a)) * [ln(K/Y) - ln(K/Y)*]. The gap
in ln(K/Y) is therefore a direct measure of "how far from the steady state".

Units. PWT's rnna and rgdpna are both in 2021 US$ but converted with
different PPPs (capital with the investment PPP, output with the GDP PPP).
Their ratio is K/Y at international prices. To compare it with an investment
share measured in national prices we rescale by (pl_n / pl_gdpo) in 2021.
For the Philippines this factor is about 0.6, so ignoring it overstates K/Y by
about two thirds (decision D2 in CLAUDE.md).

Reads:  data/raw/pwt/pwt110.dta, data/raw/pwt/pwt110_na_data.dta
Writes: output/exploration/*.csv, output/exploration/fig*.{png,pdf,tiff}
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

import fig_style as fs

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "pwt"
OUT = ROOT / "output" / "exploration"
OUT.mkdir(parents=True, exist_ok=True)

PEERS = ["PHL", "IDN", "THA", "MYS", "VNM", "KOR", "CHN", "IND", "USA"]
G_TECH = 0.02     # MRW (1992) convention for g; sensitivity below uses trend GDP growth
WINDOW = 10       # trailing years used to average s, n, delta (the "current" steady state)
ALPHA = 1 / 3     # capital share for the output-gap translation; PHL labsh ~0.44 is checked below


def load():
    p = pd.read_stata(RAW / "pwt110.dta")
    n = pd.read_stata(RAW / "pwt110_na_data.dta")
    d = p.merge(n[["countrycode", "year", "q_gfcf", "q_gdp"]], on=["countrycode", "year"], how="left")
    return d[d.countrycode.isin(PEERS)].copy()


def steady_state_gap(x):
    """Annual distance from the steady-state capital-output ratio for one country."""
    x = x.set_index("year").sort_index()
    conv = float(x.loc[2021, "pl_n"] / x.loc[2021, "pl_gdpo"])
    out = pd.DataFrame(index=x.index)
    out["ky_ppp"] = x.rnna / x.rgdpna
    out["ky"] = out.ky_ppp * conv                      # national-price K/Y
    out["s"] = x.q_gfcf / x.q_gdp                      # real investment share, national prices
    out["n"] = np.log(x.emp).diff()
    out["gY"] = np.log(x.rgdpna).diff()
    out["delta"] = x.delta
    roll = lambda v: v.rolling(WINDOW, min_periods=WINDOW).mean()  # noqa: E731
    out["s_bar"], out["n_bar"], out["d_bar"], out["gY_bar"] = roll(out.s), roll(out.n), roll(out.delta), roll(out.gY)
    out["ky_star"] = out.s_bar / (out.n_bar + G_TECH + out.d_bar)          # variant V1 (MRW)
    out["ky_star_v2"] = out.s_bar / (out.gY_bar + out.d_bar)               # variant V2 (trend GDP growth)
    out["gap"] = np.log(out.ky) - np.log(out.ky_star)
    out["gap_v2"] = np.log(out.ky) - np.log(out.ky_star_v2)
    out["y_gap_pct"] = 100 * (ALPHA / (1 - ALPHA)) * out.gap
    out["ypw"] = x.rgdpna / x.emp
    out["rtfpna"] = x.rtfpna
    out["labsh"] = x.labsh
    out["hc"] = x.hc
    out["conv_factor"] = conv
    return out


def relative_income(d):
    """Output per worker relative to the US: level from cgdpo in 2019, path from rgdpna growth."""
    rows = []
    us = d[d.countrycode == "USA"].set_index("year")
    us_pw = us.rgdpna / us.emp
    for c, x in d.groupby("countrycode"):
        x = x.set_index("year")
        pw = x.rgdpna / x.emp
        lvl19 = (x.loc[2019, "cgdpo"] / x.loc[2019, "emp"]) / (us.loc[2019, "cgdpo"] / us.loc[2019, "emp"])
        rel = lvl19 * (pw / pw.loc[2019]) / (us_pw / us_pw.loc[2019])
        rows.append(pd.DataFrame({"countrycode": c, "year": rel.index, "rel_ypw_us": 100 * rel.values}))
    return pd.concat(rows)


def speed_of_convergence(g):
    """Delta ln(K/Y)_t = c - lambda * gap_{t-1}: the share of the gap closed per year."""
    z = pd.DataFrame({"dky": np.log(g.ky).diff(), "gap_l": g.gap.shift()}).dropna()
    z = z.loc[1975:2019]  # stop before COVID so one outlier year does not drive the estimate
    res = sm.OLS(z.dky, sm.add_constant(z.gap_l)).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    lam = -res.params["gap_l"]
    return dict(lambda_hat=lam, se=res.bse["gap_l"], half_life=np.log(2) / lam if lam > 0 else np.nan,
                n_obs=int(res.nobs), sample=f"{z.index.min()}-{z.index.max()}")


def decompose_star(g, t0, t1):
    """Contribution of s, n and delta to the change in ln(K/Y)* between two years (V1)."""
    a, b = g.loc[t0], g.loc[t1]
    ds = np.log(b.s_bar) - np.log(a.s_bar)
    dd = -(np.log(a.n_bar + G_TECH + b.d_bar) - np.log(a.n_bar + G_TECH + a.d_bar))
    dn = -(np.log(b.n_bar + G_TECH + b.d_bar) - np.log(a.n_bar + G_TECH + b.d_bar))
    return dict(period=f"{t0}-{t1}", d_ln_star=np.log(b.ky_star) - np.log(a.ky_star),
                from_s=ds, from_n=dn, from_delta=dd, d_ln_ky=np.log(b.ky) - np.log(a.ky))


def main():
    d = load()
    gaps = pd.concat({c: steady_state_gap(x) for c, x in d.groupby("countrycode")}, names=["countrycode"])
    gaps.reset_index().to_csv(OUT / "steady_state_gap.csv", index=False, float_format="%.5f")
    ph = gaps.loc["PHL"]

    rel = relative_income(d)
    rel.to_csv(OUT / "relative_income.csv", index=False, float_format="%.3f")

    speed = pd.DataFrame([speed_of_convergence(gaps.loc[c]) | {"countrycode": c}
                          for c in PEERS if c != "USA"])
    speed.to_csv(OUT / "speed_of_convergence.csv", index=False, float_format="%.4f")

    dec = pd.DataFrame([decompose_star(ph, a, b) for a, b in [(1980, 1990), (1990, 2000), (2000, 2010),
                                                                (2010, 2019), (1980, 2019)]])
    dec.to_csv(OUT / "phl_star_decomposition.csv", index=False, float_format="%.4f")

    snap = ph.loc[[1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2020, 2023],
                  ["ky", "ky_star", "ky_star_v2", "gap", "gap_v2", "y_gap_pct", "s_bar", "n_bar", "d_bar",
                   "gY_bar", "rtfpna", "labsh"]]
    snap.to_csv(OUT / "phl_snapshot.csv", float_format="%.4f")

    # Figures (black and white, no titles inside the image)
    fs.setup()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.plot(ph.index, ph.ky, label="Actual K/Y", **fs.A)
    ax.plot(ph.index, ph.ky_star, label="Steady-state K/Y, V1 (n + 0.02 + δ)", **fs.B)
    ax.plot(ph.index, ph.ky_star_v2, label="Steady-state K/Y, V2 (trend GDP growth + δ)", **fs.C)
    ax.set_xlim(1970, 2024)
    ax.set_ylabel("Capital-output ratio (national prices)")
    ax.legend(loc="lower right", fontsize=7.5)
    fs.save(fig, "fig1_phl_ky_vs_star", OUT)

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    ax.plot(ph.index, 100 * ph.gap, label="V1", **fs.A)
    ax.plot(ph.index, 100 * ph.gap_v2, label="V2", **fs.B)
    fs.zero(ax)
    ax.set_xlim(1970, 2024)
    ax.set_ylabel("ln(K/Y) − ln(K/Y)*, × 100")
    ax.legend(loc="upper right")
    fs.save(fig, "fig2_phl_gap", OUT)

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    styles = {"PHL": fs.A, "THA": fs.B, "IDN": fs.C}
    for c, st in styles.items():
        r = rel[rel.countrycode == c].set_index("year").rel_ypw_us
        ax.plot(r.index, r, label={"PHL": "Philippines", "THA": "Thailand", "IDN": "Indonesia"}[c],
                **(st | {"markevery": 5}))
    ax.set_xlim(1960, 2024)
    ax.set_ylabel("Output per worker, % of US")
    ax.legend(loc="upper left")
    fs.save(fig, "fig3_relative_income", OUT)

    pd.set_option("display.width", 200)
    print("PHL conversion factor pl_n/pl_gdpo (2021):", round(ph.conv_factor.iloc[0], 3))
    print(snap.round(3))
    print(dec.round(3))
    print(speed.round(3))
    print(rel[rel.year.isin([1960, 1980, 2000, 2019, 2023])].pivot(index="year", columns="countrycode",
                                                                    values="rel_ypw_us").round(1))


if __name__ == "__main__":
    main()
