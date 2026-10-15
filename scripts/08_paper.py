"""Build the numbers dictionary n and tables t from output/tables, then render the manuscript.

paper/manuscript_template.md -> paper/manuscript.md -> paper/manuscript.docx (pandoc, citeproc).
No estimate is typed by hand: every number in the manuscript comes from here.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_doc import render  # noqa: E402

T, PAPER = ROOT / "output" / "tables", ROOT / "paper"


def f2(x):
    return f"{x:.2f}"


def f3(x):
    return f"{x:.3f}"


def f4(x):
    return f"{x:.4f}"


def pct(x, k=1):
    return f"{100 * x:.{k}f}"


def stars(b, se):
    if not np.isfinite(se) or se == 0:
        return ""
    t = abs(b / se)
    return "\\*\\*\\*" if t > 2.576 else "\\*\\*" if t > 1.96 else "\\*" if t > 1.645 else ""


def md_table(df, align=None):
    cols = list(df.columns)
    align = align or ["l"] + ["r"] * (len(cols) - 1)
    sep = ["---" if a == "l" else "---:" for a in align]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(sep) + " |"]
    lines += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(lines)


def build():
    n, t = {}, {}
    rep = pd.read_csv(T / "replication_full.csv")
    gate = pd.read_csv(T / "replication_gate.csv")

    def r(table, sample, term, col="beta"):
        x = rep[(rep.table.astype(str) == table) & (rep["sample"] == sample) & (rep.term == term)]
        return float(x[col].iloc[0])

    n["gate_pass"] = bool(gate["pass"].all())
    n["gate_n"] = len(gate)
    n["barro_c1"], n["barro_c1_se"] = f4(r("1", "col1_rgdpch", "ln_y_lag")), f4(r("1", "col1_rgdpch", "ln_y_lag", "se"))
    n["barro_c2"], n["barro_c2_se"] = f4(r("1", "col2_rgdpch", "ln_y_lag")), f4(r("1", "col2_rgdpch", "ln_y_lag", "se"))
    n["barro_c1_r2"], n["barro_c2_r2"] = f3(r("1", "col1_rgdpch", "r2")), f3(r("1", "col2_rgdpch", "r2"))
    n["barro_nobs"] = int(r("1", "col1_rgdpch", "nobs"))
    n["barro_c3"], n["barro_c3_se"] = f4(r("1", "col3_indicative_public_X", "ln_y")), f4(r("1", "col3_indicative_public_X", "ln_y", "se"))
    n["barro_c3_nobs"] = int(r("1", "col3_indicative_public_X", "nobs"))

    # Table 1: replication
    rows = [("MRW Table I, non-oil", "ln s", "1.42", r("I", "nonoil", "ln_s")),
            ("MRW Table I, non-oil", "ln(n + g + δ)", "−1.97", r("I", "nonoil", "ln_ngd")),
            ("MRW Table II, non-oil", "ln s", "0.69", r("II", "nonoil", "ln_s")),
            ("MRW Table II, non-oil", "ln(n + g + δ)", "−1.73", r("II", "nonoil", "ln_ngd")),
            ("MRW Table II, non-oil", "ln SCHOOL", "0.66", r("II", "nonoil", "ln_school")),
            ("MRW Table V, non-oil", "ln y₁₉₆₀", "−0.289", r("V", "nonoil", "ln_y60")),
            ("MRW Table V, non-oil", "λ", "0.0137", r("V", "nonoil", "lambda")),
            ("MRW Table V, intermediate", "λ", "0.0182", r("V", "intermediate", "lambda")),
            ("MRW Table V, OECD", "λ", "0.0203", r("V", "oecd", "lambda")),
            ("MRW Table VI, non-oil", "implied α", "0.48", r("VI", "nonoil", "implied_alpha")),
            ("MRW Table VI, non-oil", "implied β", "0.23", r("VI", "nonoil", "implied_beta")),
            ("Barro Table 1, col. 1 (no fixed effects)", "ln y, lagged", "0.0019 (0.0012)",
             f"{n['barro_c1']} ({n['barro_c1_se']})"),
            ("Barro Table 1, col. 2 (fixed effects)", "ln y, lagged", "−0.0326 (0.0048)",
             f"{n['barro_c2']} ({n['barro_c2_se']})"),
            ("Barro Table 1, col. 3 (indicative)", "ln y, lagged", "−0.0171 (0.0022)",
             f"{n['barro_c3']} ({n['barro_c3_se']})")]
    tab = pd.DataFrame([(a, b, c, d if isinstance(d, str) else (f"{d:.4f}" if abs(d) < 0.1 else f"{d:.3f}"))
                        for a, b, c, d in rows], columns=["Source", "Coefficient", "Published", "This study"])
    tab["Published"] = tab["Published"].str.replace("-", "−")
    tab["This study"] = tab["This study"].str.replace("-", "−")
    t["replication"] = md_table(tab, ["l", "l", "r", "r"])

    # speed
    sp = pd.read_csv(T / "speed.csv")
    bm = sp[(sp.method == "B") & (sp.spec == "main")].iloc[0]
    am = sp[(sp.method == "A") & (sp.spec == "main")].iloc[0]  # latest window first row
    fe = sp[sp.spec == "fe_raw"].iloc[0]
    fc = sp[sp.spec == "fe_corrected"].iloc[0]
    aw = sp[(sp.method == "A")]
    n.update(lam_B=pct(bm.lam), lam_B_lo=pct(bm.lo), lam_B_hi=pct(bm.hi), hl_B=f"{bm.half_life:.0f}",
             b_B=f4(bm.b), lam_A=pct(am.lam), lam_A_lo=pct(am.lo), lam_A_hi=pct(am.hi), hl_A=f"{am.half_life:.0f}",
             lam_A_min=pct(aw.lam.min()), lam_A_max=pct(aw.lam.max()), lam_fe=pct(fe.lam), hl_fe=f"{fe.half_life:.0f}",
             lam_fc=pct(fc.lam), hl_fc=f"{fc.half_life:.0f}", b_fe=f4(fe.b))
    est = pd.read_csv(T / "estimates.csv")
    bmain = est[(est.method == "B") & (est.spec == "main")]
    n["nobs_B"], n["ncty_B"], n["r2_B"] = int(bmain.nobs.iloc[0]), int(bmain.n_units.iloc[0]), f2(bmain.r2.iloc[0])
    a_last = est[(est.method == "A") & (est.spec == "main") & (est.window == "1998-2023")]
    n["nobs_A"], n["r2_A"] = int(a_last.nobs.iloc[0]), f2(a_last.r2.iloc[0])
    a60 = est[(est.method == "A") & (est.spec == "main") & (est.window == "1960-1985")].set_index("term")
    n["a60_b"], n["a60_nobs"] = f3(a60.at["ln_y0", "beta"]), int(a60.nobs.iloc[0])
    n["a60_lam"] = pct(-np.log(1 + a60.at["ln_y0", "beta"]) / 25)

    # Table 2: coefficient table, Method B main and Method A latest window
    labels = {"ln_y": "ln y (start of period)", "inv_life": "1 / life expectancy", "ln_fert": "ln fertility",
              "rule_law": "Rule of law (V-Dem)", "csh_i": "Investment share", "csh_g": "Government consumption share",
              "open": "Openness", "democracy": "Democracy (V-Dem)", "democracy_sq": "Democracy squared",
              "infl_c": "Inflation", "yrs_f": "Female years of schooling", "yrs_m": "Male years of schooling",
              "tot_x_open": "Terms-of-trade growth × openness"}
    rows = []
    for k, lab in labels.items():
        x = bmain.set_index("term").loc[k]
        rows.append((lab, f"{x.beta:.4f}{stars(x.beta, x.se)}".replace("-", "−"), f"({x.se:.4f})"))
    t["coef_B"] = md_table(pd.DataFrame(rows, columns=["Variable", "Coefficient", "(s.e.)"]))
    al = a_last.set_index("term")
    labA = {"ln_y0": "ln y (1998)", "ln_s": "ln s (investment rate)", "ln_ngd": "ln(n + g + δ)",
            "ln_school": "ln SCHOOL", "const": "Constant"}
    rows = [(lab, f"{al.at[k, 'beta']:.3f}{stars(al.at[k, 'beta'], al.at[k, 'se'])}".replace("-", "−"),
             f"({al.at[k, 'se']:.3f})") for k, lab in labA.items()]
    t["coef_A"] = md_table(pd.DataFrame(rows, columns=["Variable", "Coefficient", "(s.e.)"]))

    # distances
    dist = pd.read_csv(T / "ph_distance.csv")
    db = dist[(dist.method == "B") & (dist.spec == "main")].set_index("year")
    da = dist[(dist.method == "A") & (dist.spec == "main")].set_index("year")
    n.update(dB_2020=f2(db.at[2020, "d"]), dB_2020_lo=f2(db.at[2020, "lo"]), dB_2020_hi=f2(db.at[2020, "hi"]),
             dB_1985=f2(db.at[1985, "d"]), dB_1965=f2(db.at[1965, "d"]), dB_1980=f2(db.at[1980, "d"]),
             dB_min=f2(db.loc[1985:2020, "d"].min()), dB_max=f2(db.loc[1985:2020, "d"].max()),
             dB_pct=f"{100 * (1 - np.exp(db.at[2020, 'd'])):.0f}",
             dA_2020=f2(da.at[2020, "d"]), dA_2020_lo=f2(da.at[2020, "lo"]), dA_2020_hi=f2(da.at[2020, "hi"]),
             dA_2023=f2(da.at[2023, "d"]), dA_2023_lo=f2(da.at[2023, "lo"]), dA_2023_hi=f2(da.at[2023, "hi"]),
             dA_1985=f2(da.at[1985, "d"]), d_own_2020=f2(db.at[2020, "d_own"]))
    n["dB_band_has_zero_after_1965"] = bool(((db.loc[1970:, "lo"] < 0) & (db.loc[1970:, "hi"] > 0)).all())
    rows = []
    for y in db.index:
        a = f"{da.at[y, 'd']:.2f} [{da.at[y, 'lo']:.2f}, {da.at[y, 'hi']:.2f}]" if y in da.index else ""
        rows.append((y, f"{db.at[y, 'd']:.2f}", f"[{db.at[y, 'lo']:.2f}, {db.at[y, 'hi']:.2f}]", a))
    rows.append((2023, "", "", f"{da.at[2023, 'd']:.2f} [{da.at[2023, 'lo']:.2f}, {da.at[2023, 'hi']:.2f}]"))
    td = pd.DataFrame(rows, columns=["Year", "Method B: d", "90% band", "Method A: d [90% band]"])
    td = td.astype(str).apply(lambda c: c.str.replace("-", "−"))
    t["distance"] = md_table(td)

    # agreement and reconciliation
    ag = pd.read_csv(T / "agreement.csv")
    n["agree_sign"], n["agree_overlap"], n["agree_lambda"] = [str(x) == "True" for x in ag.ok.iloc[:3]]
    n["agree_corr"] = f2(float(ag.ok.iloc[3]))
    rc = pd.read_csv(T / "reconciliation.csv")
    get = lambda s, c: float(rc[rc.check.str.startswith(s)][c].iloc[0])  # noqa: E731
    n.update(r1_d=f2(get("R1", "d_2020")), r2_d=f2(get("R2", "d_2020")), r1_lam=pct(get("R1", "lam")),
             r3_d2020=f2(get("R3 Method A (1995", "d_2020")), r3_d2023=f2(get("R3 Method A (1998", "d_2023")),
             n_window=pct(get("R3 Method A (1995", "n_window"), 2), n_current=pct(get("R3 Method A (1995", "n_current"), 2))
    mw = pd.read_parquet(ROOT / "data" / "processed" / "mrw_windows.parquet")
    mw = mw[(mw.start == 1995) & mw.sample_A].dropna(subset=["dln_y", "ln_y0", "ln_s", "ln_ngd", "ln_school"])
    nn = np.exp(mw.ln_ngd) - 0.05
    n["n_pctile"] = f"{100 * (nn < float(nn[mw.iso3 == 'PHL'].iloc[0])).mean():.0f}"
    n["n_median"] = pct(nn.median(), 2)
    con = pd.read_csv(T / "steady_state_contributions.csv")
    cA = con[con.method == "A"].set_index("determinant").contribution
    cB = con[con.method == "B"].set_index("determinant").contribution
    n.update(cA_ngd=f2(cA["working-age population growth"]), cA_inv=f2(cA["investment rate"]),
             cB_fert=f2(cB["fertility (log)"]), cB_rule=f2(cB["rule of law"]), cB_infl=f2(cB["inflation"]))
    tc = con.assign(contribution=con.contribution.map(lambda x: f"{x:+.2f}".replace("-", "−")),
                    method=con.method.map({"A": "A (1995–2020)", "B": "B (2020–23)"}))[["method", "determinant", "contribution"]]
    tc.columns = ["Method", "Determinant", "Contribution to ln y\\* relative to sample mean"]
    t["contrib"] = md_table(tc, ["l", "l", "r"])

    # decomposition
    dec = pd.read_csv(T / "decomposition.csv")
    cols = ["closing", "world_shock", "ph_shock", "target_move", "delta_d"]
    post, pre, full = dec[dec.period >= 1985][cols].sum(), dec[dec.period < 1985][cols].sum(), dec[cols].sum()
    for tag, s in [("post", post), ("pre", pre), ("full", full)]:
        for c in cols:
            n[f"dec_{tag}_{c}"] = f2(s[c])
    mv = dec[dec.period >= 1985].filter(like="move_").sum()
    n.update(mv_fert=f2(mv["move_fertility"]), mv_life=f2(mv["move_life expectancy"]), mv_infl=f2(mv["move_inflation"]),
             mv_trend=f2(mv["move_trend"]), mv_inv=f2(mv["move_investment"]), mv_school=f2(mv["move_schooling"]))
    mvp = dec[dec.period < 1985].filter(like="move_").sum()
    n.update(mvp_infl=f2(mvp["move_inflation"]), mvp_rule=f2(mvp["move_rule of law"]), mvp_gov=f2(mvp["move_government consumption"]))
    n["dec_maxcheck"] = f"{dec.check.abs().max():.1e}"
    rows = []
    for x in dec.itertuples():
        rows.append((f"{x.period}–{x.next}", f2(x.d0), f2(x.closing), f2(x.world_shock), f2(x.ph_shock),
                     f2(-x.target_move), f2(x.delta_d)))
    for lab, s in [("Sum 1965–1985", pre), ("Sum 1985–2020", post), ("Sum 1965–2020", full)]:
        rows.append((f"**{lab}**", "", f2(s.closing), f2(s.world_shock), f2(s.ph_shock), f2(-s.target_move), f2(s.delta_d)))
    tdd = pd.DataFrame(rows, columns=["Period", "d at start", "Closing", "World shock", "Philippine shock",
                                      "− Steady state moving", "Change in d"])
    t["decomp"] = md_table(tdd.astype(str).apply(lambda c: c.str.replace("-", "−")))

    # hypotheses
    hy = pd.read_csv(T / "hypotheses.csv").set_index("h")
    for h in hy.index:
        n[f"{h}_ok"] = bool(hy.at[h, "supported"])
        n[f"{h}_val"] = hy.at[h, "value"].replace("-", "−")
    pr = dec.set_index("period")
    n["shock_1980"] = f2(pr.at[1980, "world_shock"] + pr.at[1980, "ph_shock"])
    n["shock_1995"] = f2(pr.at[1995, "world_shock"] + pr.at[1995, "ph_shock"])
    n["shock_2015"] = f2(pr.at[2015, "world_shock"] + pr.at[2015, "ph_shock"])
    bt = pd.read_csv(T / "bootstrap_methodB.csv")
    n["resid_ph"] = f4(db.resid.mean())
    n["resid_lo"], n["resid_hi"] = f4(np.nanpercentile(bt.resid_ph, 5)), f4(np.nanpercentile(bt.resid_ph, 95))

    # robustness
    rb = pd.read_csv(T / "robustness.csv")
    rbB = rb[(rb.method == "B") & rb.d_latest.notna()]
    rbA = rb[(rb.method == "A") & rb.d_latest.notna()]
    n.update(robB_n=len(rbB), robB_neg=int((rbB.d_latest < 0).sum()), robA_n=len(rbA), robA_pos=int((rbA.d_latest > 0).sum()),
             robB_lam_min=pct(rbB[~rbB.check.str.startswith("B9")].lam.min()),
             robB_lam_max=pct(rbB[~rbB.check.str.startswith("B9")].lam.max()),
             robA_min=f2(rbA.d_latest.min()), robA_max=f2(rbA.d_latest.max()))
    getr = lambda s, c="d_latest": float(rb[rb.check.str.startswith(s)][c].iloc[0])  # noqa: E731
    n.update(rob_g015=f2(getr("B1 g* = 0.015")), rob_g025=f2(getr("B1 g* = 0.025")), rob_gus=f2(float(rb[rb.check.str.contains("US at steady")].d_latest.iloc[0])),
             g_us=pct(float(rb[rb.check.str.contains("US at steady")].check.iloc[0].split("= ")[1].split(" ")[0])),
             rob_B0=f2(getr("B0")), rob_raw=f2(getr("B2")), rob_fe=f2(getr("B9 country fixed effects (raw)")),
             rob_A1=f2(getr("A1")), rob_A3=f2(getr("A3")), rob_Ag015=f2(getr("A4 g* = 0.015")))
    rows = []
    for x in rb.itertuples():
        if "time-effect trend" in x.check:
            continue
        rows.append((x.check, x.method, f"{x.lam * 100:.2f}" if np.isfinite(x.lam) else "",
                     f"{x.d_latest:.2f}" if np.isfinite(x.d_latest) else "", str(int(x.year_latest)) if np.isfinite(x.year_latest) else ""))
    tr = pd.DataFrame(rows, columns=["Check", "Method", "λ (%)", "d", "Year of d"])
    t["robust"] = md_table(tr.astype(str).apply(lambda c: c.str.replace("-", "−")), ["l", "l", "r", "r", "r"])
    n["rob_te_g"] = pct(float(rb[rb.check.str.contains("time-effect trend")].check.iloc[0].split("= ")[1].split(" ")[0]))

    # policy
    po = pd.read_csv(T / "policy.csv")
    pg = lambda m, d: float(po[(po.method == m) & (po.determinant.str.startswith(d))].gain_ln_ystar.iloc[0])  # noqa: E731
    n.update(pol_life=f2(pg("B", "life")), pol_fert=f2(pg("B", "fert")), pol_open=f2(pg("B", "open")),
             pol_invB=f2(pg("B", "invest")), pol_invA=f2(pg("A", "invest")), pol_rule=f2(pg("B", "rule")),
             pol_schA=f2(pg("A", "school")), pol_infl=f2(pg("B", "infl")))
    rows = [(f"{'A' if x.method == 'A' else 'B'}", x.determinant, x.ph, x.peer_median, f"{x.gain_ln_ystar:+.2f}",
             f"{x.years_to_close_half:.0f}") for x in po.itertuples()]
    tp = pd.DataFrame(rows, columns=["Method", "Determinant", "Philippines", "ASEAN-4 median", "Gain in ln y\\*",
                                     "Years to half"])
    t["policy"] = md_table(tp.astype(str).apply(lambda c: c.str.replace("-", "−")), ["l", "l", "r", "r", "r", "r"])

    # descriptive
    rel = pd.read_csv(T / "desc_relative_income.csv", index_col=0)
    for y in (1960, 1980, 2000, 2019, 2023):
        for c in ("PHL", "THA", "MYS", "IDN", "KOR"):
            n[f"rel_{c}_{y}"] = f"{rel.at[y, c]:.1f}"
    gd = pd.read_csv(T / "desc_growth_decades.csv", index_col=0)
    for p in gd.index:
        n[f"g_PHL_{p.replace('-', '_')}"] = f"{gd.at[p, 'PHL']:.1f}"
    sh = pd.read_csv(T / "desc_shocks.csv")
    n["shock_years"] = ", ".join(str(int(y)) for y in sh.year)
    n["shock_1984"] = f"{float(sh[sh.year == 1984].growth.iloc[0]):.1f}"
    n["shock_2020"] = f"{float(sh[sh.year == 2020].growth.iloc[0]):.1f}"
    exp = pd.read_csv(ROOT / "output" / "exploration" / "steady_state_gap.csv")
    ky = exp[exp.countrycode == "PHL"].set_index("year").ky
    n["ky_min"], n["ky_max"] = f"{ky.loc[1985:2019].min():.2f}", f"{ky.loc[1985:2019].max():.2f}"
    gt = growth_table(gd)
    t["growth"] = gt
    n = {k: (v.replace("-", "−") if isinstance(v, str) and k not in ("shock_years",) else v) for k, v in n.items()}
    (T / "paper_numbers.json").write_text(json.dumps(n, indent=1, default=str))
    return n, t


def growth_table(gd):
    names = {"PHL": "Philippines", "IDN": "Indonesia", "MYS": "Malaysia", "THA": "Thailand", "VNM": "Viet Nam",
             "KOR": "Korea", "CHN": "China", "USA": "United States"}
    order = ["1960-1970", "1970-1980", "1980-1990", "1990-2000", "2000-2010", "2010-2019", "2019-2023", "1960-2023"]
    g = gd.loc[order].T
    g.index = [names[i] for i in g.index]
    g = g.map(lambda x: "" if pd.isna(x) else f"{x:.1f}".replace("-", "−"))
    g.columns = [c.replace("-", "–") for c in g.columns]
    return md_table(g.reset_index().rename(columns={"index": "Country"}))


if __name__ == "__main__":
    n, t = build()
    render(PAPER / "manuscript_template.md", PAPER / "manuscript.md", numbers=T / "paper_numbers.json",
           bib=PAPER / "references.bib", resource_path=str(PAPER), tables=t)
