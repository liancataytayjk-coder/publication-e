"""Estimation on new data (Phase 4), following the pre-specified plan in CLAUDE.md.

Method A (MRW 1992) on rolling 25-year windows of PWT 11.0.
Method B (Barro 2015) on a 5-year panel of PWT 11.0, 1965-2023.

Writes to output/tables/:
  estimates.csv        every coefficient of every model (long format)
  ph_distance.csv      the Philippines' distance from its steady state, both methods, with 90% bootstrap bands
  speed.csv            lambda and half-life by method/spec, with bands
  decomposition.csv    RQ4 period-by-period identity for the Philippines (Method B main)
  hypotheses.csv       H1-H4 decision rules and outcomes
  agreement.csv        the pre-registered agreement rule between the two methods
  robustness.csv       the pre-registered robustness menu
  policy.csv           RQ5 steady-state gains from moving to the ASEAN-peer median
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from steadystate.estimators import (half_life, indirect_inference_fe, iv2sls, lam_from_b, ols,  # noqa: E402
                                    within_sd)

PROC, TABLES = ROOT / "data" / "processed", ROOT / "output" / "tables"
G_STAR = 0.02
B_REPS = 499
SEED = 20261015
PH = "PHL"
PEERS = ["IDN", "MYS", "THA", "VNM"]

XB = ["inv_life", "ln_fert", "rule_law", "csh_i", "csh_g", "open", "democracy", "democracy_sq", "infl_c"]
XEXOG = ["yrs_f", "yrs_m", "tot_x_open"]
VDEM = ["rule_law", "democracy", "democracy_sq"]
CRISIS_PERIODS = [1980, 1995, 2015]  # periods containing 1983-85, 1997-98, 2020 (named in the plan)
SHOCK_VARS = ["tot_x_open"]  # D13: contemporaneous terms-of-trade growth is a shock, not a steady-state determinant


def lags(xs):
    return [x + "_lag" for x in xs]


# =========================================================================== Method B
def fit_b(d, xb=XB, xexog=XEXOG, fe=False, y="growth", iv=True):
    if iv:
        return iv2sls(d, y, ["ln_y"] + xb, xexog, ["ln_y_inst"] + lags(xb), fe=fe)
    return iv2sls(d, y, [], ["ln_y"] + xb + xexog, [], fe=fe)


def b_sample(d, periods_from=1965, extra=None):
    s = d[d.sample_B & (d.period >= periods_from)]
    if extra is not None:
        s = s[extra(s)]
    return s


def time_trend(fit):
    """Estimated time effects a_t and their fitted linear trend in the period start year."""
    te = fit.params[[c for c in fit.params.index if c.startswith("T_")]]
    yrs = np.array([int(c[2:]) for c in te.index], dtype=float)
    k, c0 = np.polyfit(yrs, te.values, 1)
    return pd.Series(te.values, yrs.astype(int)), pd.Series(c0 + k * yrs, yrs.astype(int)), k


def country_rows(fit, d, iso, xb=XB, xexog=XEXOG, g_star=G_STAR, smooth=True, fe=False, y="growth",
                 shock_vars=SHOCK_VARS):
    """Distance from the steady state for one country, period by period (Method B).

    Steady-state determinants are all X except shock_vars (D13), whose contribution
    is kept apart as a shock term ("xshock")."""
    a, a_s, _ = time_trend(fit)
    b = fit.params["ln_y"]
    xs = xb + xexog
    ss = [x for x in xs if x not in shock_vars]
    sh = [x for x in xs if x in shock_vars]
    r = d[d.iso3 == iso].dropna(subset=["ln_y", y] + xs).sort_values("period").copy()
    mu = fit.params.get(f"U_{iso}", 0.0) if fe else 0.0
    r["a"] = r.period.map(a)
    r["a_s"] = r.period.map(a_s)
    a_use = r.a_s if smooth else r.a
    r["xg"] = r[ss].values @ fit.params[ss].values
    r["xshock"] = r[sh].values @ fit.params[sh].values if sh else 0.0
    r["g_hat"] = a_use + mu + b * r.ln_y + r.xg
    r["resid"] = r[y] - (r.a + mu + b * r.ln_y + r.xg + r.xshock)
    r["d"] = (r.g_hat - g_star) / b
    r["ln_ystar"] = r.ln_y - r.d
    r["b"] = b
    return r


def ph_mean_resid(fit, d, iso=PH, **kw):
    return country_rows(fit, d, iso, **kw).resid.mean()


def decomposition(fit, d, iso=PH, xb=XB, xexog=XEXOG, g_star=G_STAR):
    r = country_rows(fit, d, iso, xb, xexog, g_star).set_index("period")
    b = fit.params["ln_y"]
    xs = xb + xexog
    groups = {"life expectancy": ["inv_life"], "fertility": ["ln_fert"], "rule of law": ["rule_law"],
              "investment": ["csh_i"], "schooling": ["yrs_f", "yrs_m"], "government consumption": ["csh_g"],
              "openness": ["open"], "democracy": ["democracy", "democracy_sq"], "inflation": ["infl_c"]}
    rows = []
    per = list(r.index)
    for t0, t1 in zip(per[:-1], per[1:]):
        x0, x1 = r.loc[t0], r.loc[t1]
        tau = x0.tau
        closing = tau * b * x0.d
        world = tau * (x0.a - x0.a_s)
        own = tau * (x0.resid + x0.xshock)
        move = (x1.ln_ystar - x0.ln_ystar) - g_star * tau
        row = dict(period=t0, next=t1, tau=tau, d0=x0.d, d1=x1.d, delta_d=x1.d - x0.d, closing=closing,
                   world_shock=world, ph_shock=own, tot_part_of_ph_shock=tau * x0.xshock, target_move=move,
                   check=closing + world + own - move - (x1.d - x0.d))
        for g, cols in groups.items():
            row["move_" + g] = -sum(fit.params[c] * (x1[c] - x0[c]) for c in cols) / b
        row["move_trend"] = -(x1.a_s - x0.a_s) / b - g_star * tau
        rows.append(row)
    return pd.DataFrame(rows)


def bootstrap_b(d, reps=B_REPS, seed=SEED, **kw):
    """Country-cluster bootstrap of Method B: coefficients re-estimated; Philippine quantities recomputed."""
    rng = np.random.default_rng(seed)
    units = d.iso3.unique()
    out = []
    for r in range(reps):
        draw = rng.choice(units, size=len(units), replace=True)
        bd = pd.concat([d[d.iso3 == u].assign(iso3=f"{u}_{k}") for k, u in enumerate(draw)], ignore_index=True)
        try:
            f = fit_b(bd, **kw)
        except np.linalg.LinAlgError:
            continue
        ph = country_rows(f, d, PH)
        out.append(dict(rep=r, b=f.params["ln_y"], lam=lam_from_b(f.params["ln_y"], 5), resid_ph=ph.resid.mean(),
                        **{f"d_{p}": v for p, v in zip(ph.period, ph.d)},
                        **{f"down_{p}": v for p, v in zip(ph.period, (ph.g_hat + ph.resid.mean() - G_STAR) / ph.b)}))
    return pd.DataFrame(out)


# =========================================================================== Method A
def fit_a(w, y="dln_y", ly="ln_y0", ngd="ln_ngd", h="ln_school", restricted=False):
    if restricted:
        w = w.assign(x_s=w.ln_s - w[ngd], x_h=w[h] - w[ngd])
        return ols(w, y, [ly, "x_s", "x_h"])
    return ols(w, y, [ly, "ln_s", ngd, h])


def a_window_sample(m, start, cols):
    return m[(m.start == start) & m.sample_A].dropna(subset=cols)


def a_distance(f, w, iso=PH, ly="ln_y0", y="dln_y", g_star=G_STAR):
    r = w[w.iso3 == iso].iloc[0]
    T = r.end - r.start
    xcols = [c for c in f.params.index if c != "const"]
    pred = f.params["const"] + sum(f.params[c] * (r[c] if c in r else (r.ln_s - r.ln_ngd if c == "x_s" else r.ln_school - r.ln_ngd)) for c in xcols)
    bcum = f.params[ly]
    d0 = (pred - g_star * T) / bcum
    dT = d0 + r[y] - g_star * T
    return d0, dT, pred, r[y]


def method_a_all(m, spec="main", g_star=G_STAR, reps=B_REPS, seed=SEED):
    cfg = dict(main=dict(), restricted=dict(restricted=True), hc=dict(h="ln_hc"),
               percapita=dict(y="dln_y_pc", ly="ln_y0_pc", ngd="ln_ngd_pc"))[spec]
    y, ly, ngd, h = cfg.get("y", "dln_y"), cfg.get("ly", "ln_y0"), cfg.get("ngd", "ln_ngd"), cfg.get("h", "ln_school")
    cols = [y, ly, "ln_s", ngd, h]
    est, dist = [], []
    rng = np.random.default_rng(seed)
    for start in sorted(m.start.unique()):
        w = a_window_sample(m, start, cols)
        if spec == "hc":
            w = w.assign(ln_school=w.ln_hc)  # so a_distance finds the human-capital column
        f = fit_a(w, y, ly, ngd, "ln_school" if spec == "hc" else h, restricted=cfg.get("restricted", False))
        T = int(w.end.iloc[0] - w.start.iloc[0])
        bcum = f.params[ly]
        lam = -np.log(1 + bcum) / T
        for term in f.params.index:
            est.append(dict(method="A", spec=spec, window=f"{start}-{start + T}", term=term, beta=f.params[term],
                            se=f.se[term], nobs=f.nobs, r2=f.extra["adj_r2"]))
        ww = w.rename(columns={y: "dln_y_use"}) if False else w
        d0, dT, pred, act = a_distance(f, ww, ly=ly, y=y, g_star=g_star)
        boots = []
        if reps:
            units = w.iso3.values
            for _ in range(reps):
                idx = rng.integers(0, len(w), len(w))
                fb = fit_a(w.iloc[idx], y, ly, ngd, "ln_school" if spec == "hc" else h,
                           restricted=cfg.get("restricted", False))
                b0, bT, _, _ = a_distance(fb, w, ly=ly, y=y, g_star=g_star)
                boots.append((b0, bT, -np.log(1 + fb.params[ly]) / T))
            boots = np.array(boots)
        q = (lambda k: np.nanpercentile(boots[:, k], [5, 95]) if reps else (np.nan, np.nan))
        dist.append(dict(method="A", spec=spec, window=f"{start}-{start + T}", start=start, end=start + T,
                         d_start=d0, d_start_lo=q(0)[0], d_start_hi=q(0)[1], d_end=dT, d_end_lo=q(1)[0],
                         d_end_hi=q(1)[1], lam=lam, lam_lo=q(2)[0], lam_hi=q(2)[1], b=bcum, nobs=f.nobs,
                         pred_growth=pred, actual_growth=act))
    return pd.DataFrame(est), pd.DataFrame(dist)


# =========================================================================== main
def coef_rows(f, method, spec, period="1965-2023"):
    return [dict(method=method, spec=spec, window=period, term=t, beta=f.params[t], se=f.se[t], nobs=f.nobs,
                 r2=f.r2, n_units=f.extra["n_units"]) for t in f.params.index]


def main():
    panel = pd.read_parquet(PROC / "barro_panel.parquet")
    d = b_sample(panel)
    est = []

    # ---------------- Method B main and bootstrap
    fb = fit_b(d)
    est += coef_rows(fb, "B", "main")
    ph = country_rows(fb, d, PH)
    boot = bootstrap_b(d)
    boot.to_csv(TABLES / "bootstrap_methodB.csv", index=False, float_format="%.6f")
    resid_ph = ph.resid.mean()
    ph["d_own"] = (ph.g_hat + resid_ph - G_STAR) / ph.b
    ph["d_lo"] = [np.nanpercentile(boot[f"d_{p}"], 5) for p in ph.period]
    ph["d_hi"] = [np.nanpercentile(boot[f"d_{p}"], 95) for p in ph.period]
    ph["d_own_lo"] = [np.nanpercentile(boot[f"down_{p}"], 5) for p in ph.period]
    ph["d_own_hi"] = [np.nanpercentile(boot[f"down_{p}"], 95) for p in ph.period]
    b_main = fb.params["ln_y"]
    lam_b = lam_from_b(b_main, 5)
    lam_b_ci = np.nanpercentile(boot.lam, [5, 95])

    # ---------------- Method B fixed effects, raw and corrected (B9 / RQ3)
    ffe = fit_b(d, fe=True)
    est += coef_rows(ffe, "B", "fe_raw")
    sigma = 5 * np.std(ffe.resid)
    n_units, T = ffe.extra["n_units"], ffe.extra["data"].period.nunique()
    b_corr, lam_corr = indirect_inference_fe(ffe.params["ln_y"], within_sd(ffe.extra["data"], "ln_y"),
                                             n_units, T, 5, sigma, reps=40, seed=SEED)
    ph_fe = country_rows(ffe, d, PH, fe=True)

    # ---------------- Method A (all windows) and robustness specs
    m = pd.read_parquet(PROC / "mrw_windows.parquet")
    a_est, a_dist = method_a_all(m, "main")
    est += a_est.to_dict("records")
    a_rob = {s: method_a_all(m, s, reps=0) for s in ["restricted", "hc", "percapita"]}
    for s, (e_, _) in a_rob.items():
        est += e_.to_dict("records")
    a_g = {g: method_a_all(m, "main", g_star=g, reps=0)[1] for g in (0.015, 0.025)}

    # ---------------- distance table
    dist = [dict(method="B", spec="main", year=int(r.period), d=r.d, lo=r.d_lo, hi=r.d_hi, d_own=r.d_own,
                 d_own_lo=r.d_own_lo, d_own_hi=r.d_own_hi, ln_y=r.ln_y, ln_ystar=r.ln_ystar, growth=r.growth,
                 g_hat=r.g_hat, resid=r.resid) for r in ph.itertuples()]
    dist += [dict(method="B", spec="fe_raw", year=int(r.period), d=r.d) for r in ph_fe.itertuples()]
    for r in a_dist.itertuples():
        dist.append(dict(method="A", spec="main", year=int(r.end), d=r.d_end, lo=r.d_end_lo, hi=r.d_end_hi,
                         window=r.window, d_start=r.d_start, d_start_lo=r.d_start_lo, d_start_hi=r.d_start_hi,
                         start=int(r.start)))
    dist = pd.DataFrame(dist)
    dist.to_csv(TABLES / "ph_distance.csv", index=False, float_format="%.5f")
    a_dist.to_csv(TABLES / "methodA_windows.csv", index=False, float_format="%.5f")

    # ---------------- speed table
    a_last = a_dist.iloc[-1]
    speed = [dict(method="A", spec="main", window=a_last.window, b=a_last.b, lam=a_last.lam, lo=a_last.lam_lo,
                  hi=a_last.lam_hi, half_life=half_life(a_last.lam))]
    speed += [dict(method="A", spec="main", window=r.window, b=r.b, lam=r.lam, lo=r.lam_lo, hi=r.lam_hi,
                   half_life=half_life(r.lam)) for r in a_dist.itertuples()][:-1]
    speed += [dict(method="B", spec="main", window="1965-2023", b=b_main, lam=lam_b, lo=lam_b_ci[0], hi=lam_b_ci[1],
                   half_life=half_life(lam_b)),
              dict(method="B", spec="fe_raw", window="1965-2023", b=ffe.params["ln_y"],
                   lam=lam_from_b(ffe.params["ln_y"], 5), half_life=half_life(lam_from_b(ffe.params["ln_y"], 5))),
              dict(method="B", spec="fe_corrected", window="1965-2023", b=b_corr, lam=lam_corr,
                   half_life=half_life(lam_corr))]
    speed = pd.DataFrame(speed)
    speed.to_csv(TABLES / "speed.csv", index=False, float_format="%.5f")

    # ---------------- RQ4 decomposition
    dec = decomposition(fb, d)
    dec.to_csv(TABLES / "decomposition.csv", index=False, float_format="%.5f")

    # ---------------- hypotheses
    tr = np.polyfit(ph.period, ph.d, 1)[0]
    cum_close, cum_move = dec.closing.sum(), dec.target_move.sum()
    shocks = dec.set_index("period")[["world_shock", "ph_shock"]].sum(axis=1)
    n_neg = int((shocks.reindex(CRISIS_PERIODS) < 0).sum())
    r_ci = np.nanpercentile(boot.resid_ph, [5, 95])
    hyp = pd.DataFrame([
        dict(h="H1", rule="d < 0 and trend of d over 1965-2020 towards zero",
             value=f"mean d {ph.d.mean():.3f}; trend {tr * 10:.4f} per decade",
             supported=bool(ph.d.mean() < 0 and tr > 0)),
        dict(h="H2", rule="cumulative target movement > 0 and >= half the cumulative closing term",
             value=f"cum move {cum_move:.3f}; cum closing {cum_close:.3f}",
             supported=bool(cum_move > 0 and cum_move >= 0.5 * cum_close)),
        dict(h="H3", rule="shock terms negative in >= 2 of the 3 crisis periods (1980-85, 1995-2000, 2015-20)",
             value="; ".join(f"{p}: {shocks.get(p, np.nan):.3f}" for p in CRISIS_PERIODS), supported=bool(n_neg >= 2)),
        dict(h="H4", rule="Philippine mean residual < 0 with 90% bootstrap interval below zero",
             value=f"{resid_ph:.4f} [{r_ci[0]:.4f}, {r_ci[1]:.4f}]", supported=bool(r_ci[1] < 0)),
    ])
    hyp.to_csv(TABLES / "hypotheses.csv", index=False)

    # ---------------- agreement rule (latest common date 2020)
    a20 = a_dist[a_dist.end == 2020].iloc[0]
    b20 = ph[ph.period == 2020].iloc[0]
    overlap = not (a20.d_end_hi < b20.d_lo or b20.d_hi < a20.d_end_lo)
    lam_a20 = a20.lam
    common = pd.merge(dist[(dist.method == "A") & (dist.spec == "main")][["year", "d"]],
                      dist[(dist.method == "B") & (dist.spec == "main")][["year", "d"]], on="year", suffixes=("_A", "_B"))
    common = common[(common.year >= 1985) & (common.year <= 2020)]
    agree = pd.DataFrame([
        dict(rule="(i) same sign of d in 2020", A=a20.d_end, B=b20.d, ok=bool(np.sign(a20.d_end) == np.sign(b20.d))),
        dict(rule="(ii) 90% intervals overlap in 2020", A=f"[{a20.d_end_lo:.3f}, {a20.d_end_hi:.3f}]",
             B=f"[{b20.d_lo:.3f}, {b20.d_hi:.3f}]", ok=bool(overlap)),
        dict(rule="(iii) lambda of each inside the other's 90% interval",
             A=f"{lam_a20:.4f} [{a20.lam_lo:.4f}, {a20.lam_hi:.4f}] (1995-2020)",
             B=f"{lam_b:.4f} [{lam_b_ci[0]:.4f}, {lam_b_ci[1]:.4f}]",
             ok=bool(lam_b_ci[0] <= lam_a20 <= lam_b_ci[1] and a20.lam_lo <= lam_b <= a20.lam_hi)),
        dict(rule="correlation of A and B distance paths 1985-2020 (descriptive)", A=len(common), B="",
             ok=float(np.corrcoef(common.d_A, common.d_B)[0, 1])),
    ])
    agree.to_csv(TABLES / "agreement.csv", index=False)

    # ---------------- robustness menu
    rob = []

    def rob_b(label, f, dd, smooth=True, g=G_STAR, fe=False, xb=XB, xexog=XEXOG, y="growth", tau=5,
              shock_vars=SHOCK_VARS):
        rr = country_rows(f, dd, PH, xb=xb, xexog=xexog, g_star=g, smooth=smooth, fe=fe, y=y, shock_vars=shock_vars)
        last = rr.iloc[-1]
        rob.append(dict(check=label, method="B", b=f.params["ln_y"], se=f.se["ln_y"], lam=lam_from_b(f.params["ln_y"], tau),
                        d_latest=last.d, year_latest=int(last.period), d_mean=rr.d.mean(), resid_ph=rr.resid.mean(),
                        nobs=f.nobs, n_units=f.extra["n_units"]))

    rob_b("B main", fb, d)
    for g in (0.015, 0.025):
        rob_b(f"B1 g* = {g}", fb, d, g=g)
    us = country_rows(fb, d, "USA")
    g_us = us.g_hat.mean()
    rob_b(f"B1 g* = {g_us:.4f} (US at steady state on average)", fb, d, g=g_us)
    _, _, kslope = time_trend(fb)
    g_te = -kslope / b_main
    rob_b(f"B1 g* = {g_te:.4f} (implied by time-effect trend)", fb, d, g=g_te)
    rob_b("B0 pre-registered: terms of trade inside the steady state (before D13)", fb, d, shock_vars=[])
    rob_b("B2 raw time effects", fb, d, smooth=False)
    f3 = fit_b(d, y="growth_na")
    rob_b("B3 growth from rgdpna", f3, d, y="growth_na")
    p10 = b_sample(pd.read_parquet(PROC / "barro_panel10.parquet"), periods_from=1970)
    f4 = fit_b(p10)
    rob_b("B4 10-year periods", f4, p10, tau=10)
    p19 = b_sample(pd.read_parquet(PROC / "barro_panel2019.parquet"))
    rob_b("B5 data end in 2019", fit_b(p19), p19)
    rob_b("B6 OLS instead of 2SLS", fit_b(d, iv=False), d)
    xb7 = [x for x in XB if x not in VDEM]
    rob_b("B7 without V-Dem variables", fit_b(d, xb=xb7), d, xb=xb7)
    d8 = d[d.oil_mean.fillna(0) <= 20]
    rob_b("B8 excluding oil-rich countries", fit_b(d8), d8)
    rob_b("B9 country fixed effects (raw)", ffe, d, fe=True)
    rob.append(dict(check="B9 country fixed effects, indirect-inference corrected", method="B", b=b_corr, lam=lam_corr))
    d10 = d[d.period <= 2005]
    rob_b("B10 Barro's window, periods 1965-2005", fit_b(d10), d10)
    rob.append(dict(check="A main", method="A", b=a_last.b, lam=a_last.lam, d_latest=a_last.d_end,
                    year_latest=int(a_last.end)))
    for s, (_, dd) in a_rob.items():
        last = dd.iloc[-1]
        rob.append(dict(check=dict(restricted="A1 restricted (Table VI)", hc="A2 ln hc instead of SCHOOL",
                                   percapita="A3 per capita")[s],
                        method="A", b=last.b, lam=last.lam, d_latest=last.d_end, year_latest=int(last.end)))
    for g, dd in a_g.items():
        last = dd.iloc[-1]
        rob.append(dict(check=f"A4 g* = {g}", method="A", b=last.b, lam=last.lam, d_latest=last.d_end,
                        year_latest=int(last.end)))
    rob = pd.DataFrame(rob)
    rob.to_csv(TABLES / "robustness.csv", index=False, float_format="%.5f")

    # ---------------- Supplementary reconciliation (D14): swap the determinant sets between methods
    rec = []
    xm = ["ln_s", "ln_ngd"]
    dm = d.dropna(subset=xm + lags(xm) + ["ln_yrs"])
    f_r1 = iv2sls(dm, "growth", ["ln_y"] + xm, ["ln_yrs"], ["ln_y_inst"] + lags(xm))
    r1 = country_rows(f_r1, dm, PH, xb=xm, xexog=["ln_yrs"], shock_vars=[])
    rec.append(dict(check="R1 Method B (panel) with MRW determinants only (ln s, ln(n+g+d), ln schooling years)",
                    method="B", b=f_r1.params["ln_y"], se=f_r1.se["ln_y"], lam=lam_from_b(f_r1.params["ln_y"], 5),
                    d_2020=float(r1[r1.period == 2020].d.iloc[0]), d_mean_1985_2020=r1[r1.period >= 1985].d.mean(),
                    nobs=f_r1.nobs))
    est += coef_rows(f_r1, "B", "R1_mrw_determinants")
    w95 = a_window_sample(m, 1995, ["dln_y", "ln_y0", "ln_s", "ln_ngd", "ln_school"])
    xavg = panel[(panel.period >= 1995) & (panel.period <= 2015)].groupby("iso3")[
        ["inv_life", "ln_fert", "rule_law", "csh_g", "open", "democracy", "democracy_sq", "infl_c", "yrs_f", "yrs_m"]].mean()
    w95x = w95.merge(xavg, left_on="iso3", right_index=True, how="inner").dropna()
    xa = ["ln_y0", "ln_s", "ln_ngd", "ln_school"] + list(xavg.columns)
    f_r2 = ols(w95x, "dln_y", xa)
    r = w95x[w95x.iso3 == PH].iloc[0]
    pred = f_r2.params["const"] + sum(f_r2.params[c] * r[c] for c in xa)
    d0 = (pred - G_STAR * 25) / f_r2.params["ln_y0"]
    rec.append(dict(check="R2 Method A (cross-section 1995-2020) with Barro's determinants added",
                    method="A", b=f_r2.params["ln_y0"], se=f_r2.se["ln_y0"], lam=-np.log(1 + f_r2.params["ln_y0"]) / 25,
                    d_2020=d0 + r.dln_y - G_STAR * 25, d_mean_1985_2020=np.nan, nobs=f_r2.nobs))
    for t_ in f_r2.params.index:
        est.append(dict(method="A", spec="R2_barro_determinants", window="1995-2020", term=t_, beta=f_r2.params[t_],
                        se=f_r2.se[t_], nobs=f_r2.nobs, r2=f_r2.extra["adj_r2"]))
    # R3: Method A with population growth measured over the last 5 years of the window (current demographics)
    wdi = pd.read_parquet(PROC / "wdi.parquet")
    for st in (1995, 1998):
        w = a_window_sample(m, st, ["dln_y", "ln_y0", "ln_s", "ln_ngd", "ln_school"]).copy()
        e = int(w.end.iloc[0])
        f_a = fit_a(w)
        last5 = wdi[(wdi.year >= e - 5) & (wdi.year <= e)].sort_values("year").groupby("iso3").wap.agg(
            lambda x: np.log(x.iloc[-1] / x.iloc[0]) / (len(x) - 1))
        w3 = w.assign(ln_ngd=np.log(w.iso3.map(last5) + 0.05))
        _, dT, _, _ = a_distance(f_a, w3)
        rec.append(dict(check=f"R3 Method A ({st}-{e}) with current population growth ({e - 5}-{e}) in the steady state",
                        method="A", b=f_a.params["ln_y0"], lam=-np.log(1 + f_a.params["ln_y0"]) / (e - st),
                        d_2020=dT if e == 2020 else np.nan, d_2023=dT if e == 2023 else np.nan,
                        n_window=float(np.exp(w[w.iso3 == PH].ln_ngd.iloc[0]) - 0.05), n_current=float(last5[PH])))
    a95 = a_dist[a_dist.start == 1995].iloc[0]
    rec.insert(0, dict(check="A main (1995-2020 window)", method="A", b=a95.b, lam=a95.lam, d_2020=a95.d_end,
                       d_2023=a_last.d_end))
    rec.insert(1, dict(check="B main", method="B", b=b_main, lam=lam_b, d_2020=float(ph[ph.period == 2020].d.iloc[0]),
                       d_mean_1985_2020=ph[ph.period >= 1985].d.mean()))
    rec = pd.DataFrame(rec)
    rec.to_csv(TABLES / "reconciliation.csv", index=False, float_format="%.5f")

    # ---------------- RQ5 policy: move each determinant to the ASEAN-peer median (latest period)
    last_p = d.period.max()
    full = panel[panel.period == last_p].set_index("iso3")
    x_ph, x_peer = full.loc[PH], full.loc[PEERS].median(numeric_only=True)
    groups = {"life expectancy": ["inv_life"], "fertility": ["ln_fert"], "rule of law": ["rule_law"],
              "investment": ["csh_i"], "schooling (years, both sexes)": ["yrs_f", "yrs_m"],
              "government consumption": ["csh_g"], "openness": ["open"],
              "democracy": ["democracy", "democracy_sq"], "inflation": ["infl_c"]}
    pol = []
    for g, cols in groups.items():
        dx = {c: x_peer[c] - x_ph[c] for c in cols}
        if g == "democracy":
            dx["democracy_sq"] = x_peer["democracy"] ** 2 - x_ph["democracy"] ** 2
        gain = -sum(fb.params[c] * dx[c] for c in cols) / b_main
        pol.append(dict(method="B", determinant=g, ph=", ".join(f"{x_ph[c]:.3f}" for c in cols),
                        peer_median=", ".join(f"{x_peer[c]:.3f}" for c in cols), gain_ln_ystar=gain))
    w_last = a_window_sample(m, m.start.max(), ["dln_y", "ln_y0", "ln_s", "ln_ngd", "ln_school"]).set_index("iso3")
    fa = fit_a(w_last.reset_index())
    pa = w_last.reindex(PEERS).median(numeric_only=True)
    for g, c in [("investment", "ln_s"), ("schooling (secondary enrolment)", "ln_school")]:
        gain = -fa.params[c] * (pa[c] - w_last.loc[PH, c]) / fa.params["ln_y0"]
        pol.append(dict(method="A", determinant=g, ph=f"{np.exp(w_last.loc[PH, c]):.3f}",
                        peer_median=f"{np.exp(pa[c]):.3f}", gain_ln_ystar=gain))
    pol = pd.DataFrame(pol)
    pol["years_to_close_half"] = np.where(pol.method == "B", half_life(lam_b), half_life(a_last.lam))
    pol.to_csv(TABLES / "policy.csv", index=False, float_format="%.4f")

    est = pd.DataFrame(est)
    est.to_csv(TABLES / "estimates.csv", index=False, float_format="%.6f")

    # ---------------- console summary
    pd.set_option("display.width", 220)
    print("Method B main: b =", round(b_main, 4), "se", round(fb.se["ln_y"], 4), "lambda", round(lam_b, 4), lam_b_ci.round(4),
          "N", fb.nobs, "countries", fb.extra["n_units"])
    print("FE raw b", round(ffe.params["ln_y"], 4), "lambda", round(lam_from_b(ffe.params["ln_y"], 5), 4),
          "| corrected lambda", round(lam_corr, 4))
    print(ph[["period", "ln_y", "growth", "g_hat", "resid", "d", "d_lo", "d_hi", "d_own"]].round(3).to_string(index=False))
    print(a_dist[["window", "nobs", "b", "lam", "lam_lo", "lam_hi", "d_start", "d_end", "d_end_lo", "d_end_hi"]].round(3).to_string(index=False))
    print(dec.round(3).to_string(index=False))
    print(hyp.to_string(index=False))
    print(agree.to_string(index=False))
    print(rob.round(4).to_string(index=False))
    print(pol.round(3).to_string(index=False))
    print(rec.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
