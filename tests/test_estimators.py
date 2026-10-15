"""Simulation tests: the estimators recover known parameters (Phase 3.1).

Run with `pytest -q`. Every estimate in the paper relies on these functions.
"""

import numpy as np
import pandas as pd
import pytest

from steadystate.estimators import (b_from_lam, distance, half_life, indirect_inference_fe, iv2sls, lam_from_b, ols,
                                    split_panel_jackknife, within_sd)

LAM, TAU, GSTAR = 0.02, 5, 0.02


def test_lambda_roundtrip():
    b = b_from_lam(LAM, TAU)
    assert np.isclose(lam_from_b(b, TAU), LAM)
    assert np.isclose(half_life(0.02), np.log(2) / 0.02)
    # Barro's FE coefficient -0.0326 per year over 5-year periods
    assert 0.034 < lam_from_b(-0.0326, 5) < 0.036


def test_ols_recovers_mrw_type_coefficients():
    rng = np.random.default_rng(1)
    n = 2000
    df = pd.DataFrame({"ls": rng.normal(-1.8, 0.4, n), "lngd": rng.normal(-2.7, 0.15, n), "lsch": rng.normal(1.2, 0.8, n)})
    df["y"] = 7 + 0.7 * df.ls - 1.7 * df.lngd + 0.65 * df.lsch + rng.normal(0, 0.1, n)
    f = ols(df, "y", ["ls", "lngd", "lsch"])
    assert abs(f.params["ls"] - 0.7) < 0.02 and abs(f.params["lngd"] + 1.7) < 0.06 and abs(f.params["lsch"] - 0.65) < 0.01


def simulate_panel(n=100, periods=10, observed_steady_state=True, seed=0, sigma=0.05):
    """ln y converges to a country-specific steady-state path c_i + g* t at speed LAM."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    c = 8 + 0.6 * x if observed_steady_state else 8 + rng.normal(0, 0.6, n)
    d0 = rng.normal(-0.5, 0.4, n)
    rows = []
    for i in range(n):
        lny = c[i] + d0[i]
        lny_prev = lny - 0.01
        for p in range(periods):
            t = p * TAU
            star_now, star_next = c[i] + GSTAR * t, c[i] + GSTAR * (t + TAU)
            lny_next = star_next + np.exp(-LAM * TAU) * (lny - star_now) + rng.normal(0, sigma)
            rows.append(dict(iso3=f"C{i:03d}", period=p, ln_y=lny, ln_y_inst=lny_prev, x=x[i],
                             growth=(lny_next - lny) / TAU, d_true=lny - star_now))
            lny_prev, lny = lny_next - 0.01, lny_next
    return pd.DataFrame(rows)


def test_pooled_iv_recovers_speed_when_steady_state_is_observed():
    df = simulate_panel(observed_steady_state=True, n=300)
    f = iv2sls(df, "growth", endog=["ln_y"], exog=["x"], instruments=["ln_y_inst"])
    assert abs(lam_from_b(f.params["ln_y"], TAU) - LAM) < 0.003


def test_iv_equals_ols_when_instrument_is_regressor():
    df = simulate_panel(n=50)
    a = iv2sls(df, "growth", endog=[], exog=["ln_y", "x"], instruments=[])
    b = iv2sls(df, "growth", endog=["ln_y"], exog=["x"], instruments=["ln_y"])
    assert np.isclose(a.params["ln_y"], b.params["ln_y"])


def test_fixed_effects_overstate_speed():
    """The Hurwicz-Nickell bias that Barro (2015) stresses: FE in a 10-period panel overstates lambda."""
    fe = [iv2sls(simulate_panel(observed_steady_state=False, n=80, seed=s), "growth", ["ln_y"], [], ["ln_y_inst"],
                 fe=True).params["ln_y"] for s in range(20)]
    assert np.mean(fe) - b_from_lam(LAM, TAU) < -0.005


def test_split_panel_jackknife_overcorrects_in_short_persistent_panels():
    """Documents decision D9: with T = 10 and rho = 0.9 the half-panel jackknife overshoots."""
    jk = [split_panel_jackknife(simulate_panel(observed_steady_state=False, n=80, seed=s), "growth", ["ln_y"], [],
                                ["ln_y_inst"])[0]["ln_y"] for s in range(10)]
    assert np.mean(jk) - b_from_lam(LAM, TAU) > 0.005


def test_indirect_inference_removes_fe_bias():
    b_true = b_from_lam(LAM, TAU)
    corrected = []
    for s in range(10):
        df = simulate_panel(observed_steady_state=False, n=80, seed=s)
        f = iv2sls(df, "growth", ["ln_y"], [], ["ln_y_inst"], fe=True)
        sigma = TAU * np.std(f.resid)
        sw = within_sd(f.extra["data"], "ln_y")
        corrected.append(indirect_inference_fe(f.params["ln_y"], sw, n=80, T=10, tau=TAU, sigma=sigma, reps=20)[0])
    assert abs(np.mean(corrected) - b_true) < 0.004


def test_distance_recovers_known_gap():
    """With no noise, time effects absorb the steady-state trend exactly, so d = (pred - g*)/b is exact."""
    df = simulate_panel(observed_steady_state=True, n=100, sigma=0.0)
    f = iv2sls(df, "growth", endog=[], exog=["ln_y", "x"], instruments=[])
    d_hat = distance(f.fitted.values, GSTAR, f.params["ln_y"])
    assert np.allclose(d_hat, df["d_true"].values, atol=1e-6)
