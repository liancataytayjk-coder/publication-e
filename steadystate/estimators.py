"""Estimators for the two reference designs.

Method A (Mankiw, Romer & Weil 1992): cross-section OLS with conventional
standard errors, as in the original tables.

Method B (Barro 2015): panel growth regressions on 5-year periods, estimated
by two-stage least squares (2SLS) with time effects, optional country fixed
effects (as dummies, "LSDV") and standard errors clustered by country, i.e.
allowing the errors of one country to be correlated over time. The
split-panel jackknife of Dhaene & Jochmans (2015) removes most of the
Hurwicz-Nickell bias that fixed effects create in short panels.

Convergence speed. In a growth regression with the annual growth rate over a
period of tau years on the left and ln y at the start on the right, the
coefficient b on ln y relates to the speed of convergence lambda by
b = -(1 - exp(-lambda * tau)) / tau, so lambda = -ln(1 + b * tau) / tau.
"""

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class Fit:
    params: pd.Series
    se: pd.Series
    nobs: int
    r2: float
    resid: pd.Series
    fitted: pd.Series
    k: int
    extra: dict = field(default_factory=dict)

    def t(self, name):
        return self.params[name] / self.se[name]


# --------------------------------------------------------------------------- OLS (Method A)
def ols(df, y, xvars, const=True):
    """OLS with conventional (homoskedastic) standard errors, as MRW report."""
    d = df[[y] + list(xvars)].dropna()
    X = d[list(xvars)].astype(float)
    if const:
        X = X.assign(const=1.0)[["const"] + list(xvars)]
    Y = d[y].astype(float).values
    Xm = X.values
    XtX_inv = np.linalg.inv(Xm.T @ Xm)
    beta = XtX_inv @ Xm.T @ Y
    e = Y - Xm @ beta
    n, k = Xm.shape
    s2 = e @ e / (n - k)
    se = np.sqrt(np.diag(XtX_inv) * s2)
    sst = ((Y - Y.mean()) ** 2).sum()
    r2 = 1 - (e @ e) / sst
    adj = 1 - (1 - r2) * (n - 1) / (n - k)
    f = Fit(pd.Series(beta, X.columns), pd.Series(se, X.columns), n, r2,
            pd.Series(e, d.index), pd.Series(Xm @ beta, d.index), k,
            extra={"adj_r2": adj, "see": np.sqrt(s2), "vcov": pd.DataFrame(XtX_inv * s2, X.columns, X.columns)})
    return f


def wald_linear(fit, R, r=0.0):
    """Wald test of R'beta = r for one linear restriction (returns t-stat and two-sided p-value)."""
    from scipy import stats
    V = fit.extra["vcov"]
    Rv = pd.Series(R).reindex(fit.params.index).fillna(0.0)
    est = float(Rv @ fit.params) - r
    var = float(Rv @ V @ Rv)
    tstat = est / np.sqrt(var)
    return tstat, 2 * (1 - stats.t.cdf(abs(tstat), fit.nobs - fit.k))


# --------------------------------------------------------------------------- 2SLS panel (Method B)
def _design(df, cols, time, unit, fe, time_effects):
    parts = [df[cols].astype(float)]
    if time_effects:
        parts.append(pd.get_dummies(df[time], prefix="T", dtype=float))  # one dummy per period, no constant
    if fe:
        u = pd.get_dummies(df[unit], prefix="U", dtype=float)
        parts.append(u.iloc[:, 1:])  # drop one country; time dummies carry the levels
    return pd.concat(parts, axis=1)


def iv2sls(df, y, endog, exog, instruments, time="period", unit="iso3", fe=False, time_effects=True):
    """2SLS growth regression with time effects (no global constant: one dummy per period),
    optional country fixed effects (LSDV) and country-clustered standard errors.

    endog: regressors instrumented (e.g. ln y at period start, period-average X)
    exog: regressors used as their own instruments
    instruments: excluded instruments (e.g. ln y one year earlier, lagged X)
    """
    endog, exog, instruments = list(endog), list(exog), list(instruments)
    need = list(dict.fromkeys([y, time, unit] + endog + exog + instruments))
    d = df[need].dropna().reset_index(drop=True)
    W = _design(d, endog + exog, time, unit, fe, time_effects)
    Z = _design(d, instruments + exog, time, unit, fe, time_effects)
    Y = d[y].astype(float).values
    Wm, Zm = W.values, Z.values
    # first stage projection
    ZtZ_inv = np.linalg.pinv(Zm.T @ Zm)
    What = Zm @ (ZtZ_inv @ (Zm.T @ Wm))
    A = np.linalg.pinv(What.T @ What)
    beta = A @ What.T @ Y
    e = Y - Wm @ beta
    # cluster-robust covariance
    G = d[unit].nunique()
    n = len(d)
    k_report = len(endog) + len(exog) + (d[time].nunique() if time_effects else 0)
    meat = np.zeros((Wm.shape[1], Wm.shape[1]))
    for _, idx in d.groupby(unit).indices.items():
        s = What[idx].T @ e[idx]
        meat += np.outer(s, s)
    adj = G / (G - 1) * (n - 1) / (n - k_report)
    V = adj * A @ meat @ A
    params = pd.Series(beta, W.columns)
    se = pd.Series(np.sqrt(np.clip(np.diag(V), 0, None)), W.columns)
    sst = ((Y - Y.mean()) ** 2).sum()
    r2 = 1 - (e @ e) / sst
    fit = Fit(params, se, n, r2, pd.Series(e), pd.Series(Wm @ beta), k_report,
              extra={"data": d, "W": W, "n_units": G, "vcov": pd.DataFrame(V, W.columns, W.columns), "fe": fe})
    return fit


def time_effects(fit, prefix="T_"):
    return fit.params[[c for c in fit.params.index if c.startswith(prefix)]]


def country_effects(fit, unit="iso3"):
    """Country fixed effects relative to the dropped country (zero for it)."""
    d = fit.extra["data"]
    units = sorted(d[unit].unique())
    fx = {u: fit.params.get(f"U_{u}", 0.0) for u in units}
    return pd.Series(fx)


def split_panel_jackknife(df, y, endog, exog, instruments, time="period", unit="iso3", term="ln_y"):
    """Dhaene & Jochmans (2015) half-panel jackknife for a fixed-effects regression.

    beta_JK = 2 * beta_full - (beta_half1 + beta_half2) / 2, where the halves split
    the time periods into the first and second half (overlapping by one period when
    the number of periods is odd).
    """
    full = iv2sls(df, y, endog, exog, instruments, time, unit, fe=True)
    periods = sorted(full.extra["data"][time].unique())
    T = len(periods)
    h1 = periods[: int(np.ceil(T / 2))]
    h2 = periods[int(np.floor(T / 2)):]
    f1 = iv2sls(df[df[time].isin(h1)], y, endog, exog, instruments, time, unit, fe=True)
    f2 = iv2sls(df[df[time].isin(h2)], y, endog, exog, instruments, time, unit, fe=True)
    common = [c for c in endog + exog]
    jk = 2 * full.params[common] - (f1.params[common] + f2.params[common]) / 2
    return jk, full, (f1, f2)


# --------------------------------------------------------------------------- convergence helpers
def lam_from_b(b, tau):
    """Speed of convergence implied by coefficient b on ln y in an annualised growth regression."""
    return -np.log(1 + np.asarray(b) * tau) / tau


def b_from_lam(lam, tau):
    return -(1 - np.exp(-np.asarray(lam) * tau)) / tau


def half_life(lam):
    return np.log(2) / np.asarray(lam)


def distance(pred_growth, g_star, b):
    """Distance from the steady state, d = ln y - ln y*, from predicted annual growth.

    In the growth regression, predicted growth minus steady-state growth equals
    b * (ln y - ln y*). So d = (pred_growth - g_star) / b. With b < 0, an economy
    predicted to grow faster than g* is below its steady state (d < 0).
    """
    return (np.asarray(pred_growth) - g_star) / np.asarray(b)


# --------------------------------------------------------------------------- FE bias correction
def _dm2(a):
    return a - a.mean(axis=1, keepdims=True) - a.mean(axis=0, keepdims=True) + a.mean()


def _sim_stats(lam, sd0, n, T, tau, sigma, reps, rng):
    """Mean FE slope and mean within s.d. of ln y in simulated two-way FE panels."""
    rho = np.exp(-lam * tau)
    eps = rng.normal(0, sigma, (reps, n, T))
    d = np.empty((reps, n, T + 1))
    d[:, :, 0] = rng.normal(0, sd0, (reps, n))
    for p in range(T):
        d[:, :, p + 1] = rho * d[:, :, p] + eps[:, :, p]
    lny, growth = d[:, :, :T], (d[:, :, 1:] - d[:, :, :T]) / tau
    x = lny - lny.mean(axis=2, keepdims=True) - lny.mean(axis=1, keepdims=True) + lny.mean(axis=(1, 2), keepdims=True)
    yv = growth - growth.mean(axis=2, keepdims=True) - growth.mean(axis=1, keepdims=True) + growth.mean(axis=(1, 2), keepdims=True)
    b = (x * yv).sum(axis=(1, 2)) / (x * x).sum(axis=(1, 2))
    sw = np.sqrt((x * x).mean(axis=(1, 2)))
    return b.mean(), sw.mean()


def indirect_inference_fe(b_fe, sw_obs, n, T, tau, sigma, reps=40, seed=0,
                          lam_grid=None, sd0_grid=None):
    """Correct a fixed-effects convergence coefficient for the Hurwicz-Nickell bias.

    Indirect inference (Gourieroux, Phillips & Yu 2010): choose the true speed lambda and
    the spread of initial gaps sd0 so that simulated panels of the same size reproduce two
    observed statistics: the fixed-effects slope b_fe and the within (two-way demeaned)
    standard deviation of ln y, sw_obs. The bias depends on how far countries start from
    their steady states, which is why the second statistic is needed.
    sigma is the s.d. of the tau-year shock to ln y (= tau x s.d. of the growth residual).
    Returns (b_corrected, lambda_corrected).
    """
    lam_grid = np.linspace(0.001, 0.08, 40) if lam_grid is None else lam_grid
    sd0_grid = np.geomspace(0.02, 1.5, 30) if sd0_grid is None else sd0_grid
    rng = np.random.default_rng(seed)
    best, arg = np.inf, None
    for lam in lam_grid:
        for sd0 in sd0_grid:
            b, sw = _sim_stats(lam, sd0, n, T, tau, sigma, reps, rng)
            loss = ((b - b_fe) / 0.002) ** 2 + ((sw - sw_obs) / (0.05 * sw_obs)) ** 2
            if loss < best:
                best, arg = loss, lam
    return float(b_from_lam(arg, tau)), float(arg)


def within_sd(df, col, unit="iso3", time="period"):
    """Standard deviation of a variable after removing country and period means (balanced approx.)."""
    x = df[col] - df.groupby(unit)[col].transform("mean") - df.groupby(time)[col].transform("mean") + df[col].mean()
    return float(np.sqrt((x ** 2).mean()))
