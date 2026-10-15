"""Replication gate (pre-registered in CLAUDE.md, 2026-10-15).

Method A: MRW (1992) Tables I, II, V, VI on MRW's own data.
Method B: Barro (2015) Table 1 columns 1-2 on PWT 7.0, his 80 countries.
Writes output/tables/replication_gate.csv and output/tables/replication_full.csv.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from steadystate.estimators import iv2sls, lam_from_b, ols, wald_linear  # noqa: E402

PROC, TABLES = ROOT / "data" / "processed", ROOT / "output" / "tables"
SAMPLES = {"nonoil": "N", "intermediate": "I", "oecd": "O"}


def mrw_tables(m):
    rows = []
    for name, flag in SAMPLES.items():
        d = m[m[flag] == 1]
        t1 = ols(d, "ln_y85", ["ln_s", "ln_ngd"])
        t2 = ols(d, "ln_y85", ["ln_s", "ln_ngd", "ln_school"])
        t5 = ols(d, "dln_y", ["ln_y60", "ln_s", "ln_ngd", "ln_school"])
        # restricted Table VI: coefficients on ln s, ln school relative to ln(n+g+d)
        d6 = d.assign(x_s=d.ln_s - d.ln_ngd, x_h=d.ln_school - d.ln_ngd)
        t6 = ols(d6, "dln_y", ["ln_y60", "x_s", "x_h"])
        # restricted Table I: implied alpha = b/(1+b)
        d1 = d.assign(x=d.ln_s - d.ln_ngd)
        t1r = ols(d1, "ln_y85", ["x"])
        bI = t1r.params["x"]
        for tab, f in [("I", t1), ("II", t2), ("V", t5), ("VI", t6), ("I-restricted", t1r)]:
            for term in f.params.index:
                rows.append(dict(table=tab, sample=name, term=term, beta=f.params[term], se=f.se[term]))
            rows.append(dict(table=tab, sample=name, term="adj_r2", beta=f.extra["adj_r2"], se=np.nan))
            rows.append(dict(table=tab, sample=name, term="nobs", beta=f.nobs, se=np.nan))
        for tab, f in [("V", t5), ("VI", t6)]:
            b = f.params["ln_y60"]
            lam = lam_from_b(b / 25, 25)  # b here is over 25 years: 1 + b = exp(-25 lambda)
            lam_se = f.se["ln_y60"] / (25 * (1 + b))
            rows.append(dict(table=tab, sample=name, term="lambda", beta=lam, se=lam_se))
        # Table VI implied alpha, beta: x_s coef = a/(1-a-b)*(1-e), x_h = b/(1-a-b)*(1-e), with (1-e) = -coef on ln y60
        k = -t6.params["ln_y60"]
        ps, ph = t6.params["x_s"] / k, t6.params["x_h"] / k
        rows.append(dict(table="VI", sample=name, term="implied_alpha", beta=ps / (1 + ps + ph), se=np.nan))
        rows.append(dict(table="VI", sample=name, term="implied_beta", beta=ph / (1 + ps + ph), se=np.nan))
        rows.append(dict(table="I-restricted", sample=name, term="implied_alpha", beta=bI / (1 + bI), se=np.nan))
        _, p = wald_linear(t1, {"ln_s": 1, "ln_ngd": 1})
        rows.append(dict(table="I", sample=name, term="restriction_p", beta=p, se=np.nan))
    return pd.DataFrame(rows)


def barro_cols(series):
    d = pd.read_parquet(PROC / f"barro70_panel_{series}.parquet")
    c1 = iv2sls(d, "growth", ["ln_y"], [], ["ln_y_inst"], fe=False)
    c2 = iv2sls(d, "growth", ["ln_y"], [], ["ln_y_inst"], fe=True)
    rows = []
    for col, f in [(1, c1), (2, c2)]:
        rows.append(dict(table="1", sample=f"col{col}_{series}", term="ln_y_lag", beta=f.params["ln_y"], se=f.se["ln_y"]))
        rows.append(dict(table="1", sample=f"col{col}_{series}", term="nobs", beta=f.nobs, se=np.nan))
        rows.append(dict(table="1", sample=f"col{col}_{series}", term="r2", beta=f.r2, se=np.nan))
    return pd.DataFrame(rows), c1, c2


def get(df, table, sample, term):
    r = df[(df.table == table) & (df["sample"] == sample) & (df.term == term)]
    return float(r.beta.iloc[0]), float(r.se.iloc[0]) if r.se.notna().iloc[0] else np.nan


def gate(mrw, barro):
    G = []

    def add(g, what, target, est, lo, hi, extra_ok=True):
        G.append(dict(gate=g, criterion=what, target=target, estimate=est, lo=lo, hi=hi,
                      pass_=bool(lo <= est <= hi and extra_ok)))

    b, _ = get(mrw, "I", "nonoil", "ln_s"); add("G1", "MRW I non-oil ln s", 1.42, b, 1.40, 1.44)
    b, _ = get(mrw, "I", "nonoil", "ln_ngd"); add("G1", "MRW I non-oil ln(n+g+d)", -1.97, b, -2.00, -1.94)
    b, _ = get(mrw, "I", "nonoil", "nobs"); add("G1", "MRW I non-oil N", 98, b, 98, 98)
    b, _ = get(mrw, "II", "nonoil", "ln_s"); add("G2", "MRW II non-oil ln s", 0.69, b, 0.67, 0.71)
    b, _ = get(mrw, "II", "nonoil", "ln_ngd"); add("G2", "MRW II non-oil ln(n+g+d)", -1.73, b, -1.76, -1.70)
    b, _ = get(mrw, "II", "nonoil", "ln_school"); add("G2", "MRW II non-oil ln school", 0.66, b, 0.64, 0.68)
    for s, tb, tl in [("nonoil", -0.289, 0.0137), ("intermediate", -0.366, 0.0182), ("oecd", -0.398, 0.0203)]:
        b, _ = get(mrw, "V", s, "ln_y60"); add("G3", f"MRW V {s} ln y60", tb, b, tb - 0.005, tb + 0.005)
        b, _ = get(mrw, "V", s, "lambda"); add("G3", f"MRW V {s} lambda", tl, b, tl - 0.0005, tl + 0.0005)
    b, _ = get(mrw, "VI", "nonoil", "implied_alpha"); add("G4", "MRW VI non-oil implied alpha", 0.48, b, 0.46, 0.50)
    b, _ = get(mrw, "VI", "nonoil", "implied_beta"); add("G4", "MRW VI non-oil implied beta", 0.23, b, 0.21, 0.25)
    b1, s1 = get(barro, "1", "col1_rgdpch", "ln_y_lag")
    add("G5", "Barro col 1 (no FE) ln y lag; not significantly negative", 0.0019, b1, -0.0010, 0.0050, b1 / s1 > -1.96)
    b2, s2 = get(barro, "1", "col2_rgdpch", "ln_y_lag")
    add("G6", "Barro col 2 (FE) ln y lag; significant at 1%", -0.0326, b2, -0.0400, -0.0250, abs(b2 / s2) > 2.576)
    add("G7", "Barro col 2 minus col 1", -0.0345, b2 - b1, -np.inf, -0.020)
    g = pd.DataFrame(G).rename(columns={"pass_": "pass"})
    return g


XB = ["inv_life", "ln_fert", "rule_law", "csh_i", "csh_g", "open", "democracy", "democracy_sq", "infl_c"]
XEXOG = ["yrs_f", "yrs_m", "tot_x_open"]


def barro_col3_indicative():
    """Not part of the gate: col 3 with public substitutes (V-Dem for ICRG and Freedom House)."""
    d = pd.read_parquet(PROC / "barro70_panel_rgdpch.parquet")
    x = pd.read_parquet(PROC / "barro_panel.parquet")
    lags = [c + "_lag" for c in XB]
    d = d.merge(x[["iso3", "period"] + XB + XEXOG + lags], on=["iso3", "period"], how="left")
    f = iv2sls(d, "growth", ["ln_y"] + XB, XEXOG, ["ln_y_inst"] + lags, fe=False)
    rows = [dict(table="1", sample="col3_indicative_public_X", term=k, beta=f.params[k], se=f.se[k])
            for k in ["ln_y"] + XB + XEXOG]
    rows.append(dict(table="1", sample="col3_indicative_public_X", term="nobs", beta=f.nobs, se=np.nan))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    m = pd.read_parquet(PROC / "mrw_original.parquet")
    mrw = mrw_tables(m)
    bch, _, _ = barro_cols("rgdpch")
    bl, _, _ = barro_cols("rgdpl")
    barro = pd.concat([bch, bl, barro_col3_indicative()])
    full = pd.concat([mrw.assign(paper="MRW1992"), barro.assign(paper="Barro2015")])
    full.to_csv(TABLES / "replication_full.csv", index=False, float_format="%.5f")
    g = gate(mrw, barro)
    g.to_csv(TABLES / "replication_gate.csv", index=False, float_format="%.5f")
    pd.set_option("display.width", 200)
    print(g.to_string(index=False))
    print("\nGATE:", "PASS" if g["pass"].all() else "FAIL")
    print(barro.to_string(index=False))
