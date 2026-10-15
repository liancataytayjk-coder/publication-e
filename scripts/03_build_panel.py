"""Build the analysis datasets.

1. mrw_original      MRW (1992) cross-section, their own data (replication gate).
2. barro70_panel     Barro (2015) 5-year panel on PWT 7.0, his 80 countries (replication gate).
3. mrw_windows       MRW-style cross-sections on PWT 11.0 for rolling 25-year windows (Method A, new data).
4. barro_panel       Barro-style 5-year panel on PWT 11.0 with public X variables (Method B, new data).

All choices are logged in CLAUDE.md (decisions D7-D13).
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
TABLES = ROOT / "output" / "tables"
TABLES.mkdir(parents=True, exist_ok=True)

GD = 0.05  # g + delta, MRW convention

# Barro (2015) Table 2: 80 countries (WP 18295)
BARRO80 = """ARG AUS AUT BEL BGD BOL BRA BWA CAN CHE CHL CHN CIV CMR COG COL CRI CYP DNK DOM DZA ECU EGY ESP FIN FRA GAB
GBR GHA GMB GRC GTM HND HTI IDN IND IRL ISL ITA JAM JOR JPN KEN KOR LKA LUX MAR MEX MLI MWI MYS NER NIC NLD NOR NZL
PAK PAN PER PHL PNG PRT PRY SEN SGP SLE SLV SWE TGO THA TTO TUN TUR TWN UGA URY USA VEN ZAF ZMB""".split()

LAST_YEAR = 2023  # PWT 11.0 ends in 2023; the last 5-year period is 2020-23


# --------------------------------------------------------------------------- 1. MRW original
def build_mrw_original():
    m = pd.read_parquet(PROC / "mrw1992.parquet")
    m = m.dropna(subset=["Y60", "Y85", "pop_growth", "invest", "school"]).copy()
    m["ln_y85"], m["ln_y60"] = np.log(m.Y85), np.log(m.Y60)
    m["dln_y"] = m.ln_y85 - m.ln_y60
    m["ln_s"] = np.log(m.invest / 100)
    m["ln_ngd"] = np.log(m.pop_growth / 100 + GD)
    m["ln_school"] = np.log(m.school / 100)
    m.to_parquet(PROC / "mrw_original.parquet", index=False)
    return m


# --------------------------------------------------------------------------- 2. Barro on PWT 7.0
def build_barro70(series="rgdpch"):
    p = pd.read_parquet(PROC / "pwt70.parquet")
    p = p[p.iso3.isin(BARRO80)].copy()
    p["ln_y"] = np.log(p[series])
    wide = p.pivot(index="iso3", columns="year", values="ln_y")
    rows = []
    for s in range(1960, 2010, 5):
        e = min(s + 5, 2009)
        for c in wide.index:
            y0, y1, yl = wide.at[c, s], wide.at[c, e], wide.at[c, s - 1] if s - 1 in wide.columns else np.nan
            rows.append(dict(iso3=c, period=s, tau=e - s, ln_y=y0, ln_y_inst=yl, growth=(y1 - y0) / (e - s)))
    d = pd.DataFrame(rows).dropna()
    d.to_parquet(PROC / f"barro70_panel_{series}.parquet", index=False)
    return d


# --------------------------------------------------------------------------- shared country-year table (PWT 11 + others)
def country_year():
    p = pd.read_parquet(PROC / "pwt11.parquet")
    w = pd.read_parquet(PROC / "wdi.parquet")
    v = pd.read_parquet(PROC / "vdem.parquet")
    df = p.merge(w, on=["iso3", "year"], how="left").merge(v, on=["iso3", "year"], how="left")
    df = df.sort_values(["iso3", "year"])
    # MRW-style human-capital investment: % of working-age population in secondary school
    pop1519 = df.sh1519_f / 100 * df.pop_f + df.sh1519_m / 100 * df.pop_m
    df["school"] = df.sec_enrol * pop1519 / df.wap            # in percent, like MRW
    df["infl"] = (df.infl_cpi.fillna(df.infl_defl)) / 100
    df["open"] = (df.v_x + df.v_m) / df.v_gdp                  # national current prices
    df["tot"] = df.pl_x / df.pl_m
    return df


# --------------------------------------------------------------------------- 3. Method A windows (PWT 11)
def build_mrw_windows(cy):
    windows = [(s, s + 25) for s in range(1960, 2000, 5)] + [(1998, 2023)]
    out = []
    for s, e in windows:
        g = cy[(cy.year >= s) & (cy.year <= e)].groupby("iso3")
        a = cy[cy.year == s].set_index("iso3")
        b = cy[cy.year == e].set_index("iso3")
        win = cy[(cy.year >= s) & (cy.year < e)]
        wap_growth = win.groupby("iso3").apply(
            lambda x: np.log(x.wap.iloc[-1] / x.wap.iloc[0]) / (len(x) - 1) if x.wap.notna().all() and len(x) > 1 else np.nan,
            include_groups=False)
        pop_growth = win.groupby("iso3").apply(
            lambda x: np.log(x["pop"].iloc[-1] / x["pop"].iloc[0]) / (len(x) - 1) if len(x) > 1 else np.nan,
            include_groups=False)
        f = pd.DataFrame({
            "start": s, "end": e,
            "y0": a.rgdpo / a.wap, "y0_pc": a.rgdpo / a["pop"],
            "dln_y": np.log((b.rgdpna / b.wap) / (a.rgdpna / a.wap)),
            "dln_y_pc": np.log((b.rgdpna / b["pop"]) / (a.rgdpna / a["pop"])),
            "s_k": win.groupby("iso3").csh_i.mean(),
            "n": wap_growth, "n_pc": pop_growth,
            "school": win.groupby("iso3").school.mean(),
            "hc": win.groupby("iso3").hc.mean(),
            "oil": win.groupby("iso3").oil_rents.mean(),
            "pop0": a["pop"],
        })
        f.index.name = "iso3"
        out.append(f.reset_index())
    m = pd.concat(out, ignore_index=True)
    m["ln_y0"], m["ln_y0_pc"] = np.log(m.y0), np.log(m.y0_pc)
    m["ln_s"] = np.log(m.s_k)
    m["ln_ngd"] = np.log(m.n + GD)
    m["ln_ngd_pc"] = np.log(m.n_pc + GD)
    m["ln_school"] = np.log(m.school / 100)
    m["ln_hc"] = np.log(m.hc)
    # D11: non-oil analogue: population >= 1 million at the window start and mean oil rents < 20% of GDP
    m["sample_A"] = (m.pop0 >= 1) & (m.oil.fillna(0) < 20)
    m.to_parquet(PROC / "mrw_windows.parquet", index=False)
    return m


# --------------------------------------------------------------------------- 4. Method B panel (PWT 11)
def build_barro_panel(cy, step=5, last=LAST_YEAR, name="barro_panel"):
    cy = cy[cy.year <= last].copy()
    cy["ln_y"] = np.log(cy.rgdpe / cy["pop"])
    cy["ln_y_na"] = np.log(cy.rgdpna / cy["pop"])
    cy["inv_life"] = 1 / cy.life_exp
    cy["ln_fert"] = np.log(cy.fertility)
    cy["infl_c"] = cy.infl.clip(upper=1.0)                    # D12: cap at 100% a year
    bl = pd.read_parquet(PROC / "barrolee.parquet")
    by = cy.set_index(["iso3", "year"])
    avg_vars = ["inv_life", "ln_fert", "rule_law", "csh_i", "csh_g", "open", "democracy", "infl_c", "hc"]
    rows = []
    for s in range(1960, last, step):
        e = min(s + step, last)
        win = cy[(cy.year >= s) & (cy.year < max(e, s + 1))]
        lag = cy[(cy.year >= s - step) & (cy.year < s)]
        A = win.groupby("iso3")[avg_vars].mean()
        L = lag.groupby("iso3")[avg_vars].mean().add_suffix("_lag")
        y0 = by.xs(s, level="year")
        y1 = by.xs(e, level="year")
        yl = by.xs(s - 1, level="year")
        f = pd.DataFrame({
            "period": s, "tau": e - s,
            "ln_y": y0.ln_y, "ln_y_inst": yl.ln_y,
            "growth": (y1.ln_y - y0.ln_y) / (e - s),
            "growth_na": (y1.ln_y_na - y0.ln_y_na) / (e - s),
            "tot_change": np.log(y1.tot / y0.tot) / (e - s),
            "n_pop": np.log(y1["pop"] / y0["pop"]) / (e - s),
            "n_pop_lag": np.log(y0["pop"] / by.xs(max(s - step, 1950), level="year")["pop"]) / (s - max(s - step, 1950)),
            "pop_m": y0["pop"],
        }).join(A).join(L)
        b_year = min(s, 2015)  # D8: Barro-Lee ends in 2015; 2020 uses 2015
        sch = bl[bl.year == b_year].set_index("iso3")[["yrs_f", "yrs_m", "yrs_all"]]
        f = f.join(sch)
        f["school_carried"] = s > 2015
        f.index.name = "iso3"
        rows.append(f.reset_index())
    d = pd.concat(rows, ignore_index=True)
    d["tot_x_open"] = d.tot_change * d.open
    # MRW-type determinants inside Barro's panel (supplementary reconciliation, D14)
    with np.errstate(divide="ignore", invalid="ignore"):
        d["ln_s"], d["ln_s_lag"] = np.log(d.csh_i), np.log(d.csh_i_lag)
        d["ln_ngd"], d["ln_ngd_lag"] = np.log(d.n_pop + 0.05), np.log(d.n_pop_lag + 0.05)
    d["ln_yrs"] = np.log(d.yrs_all)
    mrw_cols = ["ln_s", "ln_s_lag", "ln_ngd", "ln_ngd_lag", "ln_yrs"]
    d[mrw_cols] = d[mrw_cols].replace([np.inf, -np.inf], np.nan)
    d["democracy_sq"] = d.democracy ** 2
    d["democracy_sq_lag"] = d.democracy_lag ** 2
    # D10: Barro-like sample: GDP data starting by the 1965-70 period, population >= 0.5 million in 1990
    first = d.dropna(subset=["growth", "ln_y"]).groupby("iso3").period.min()
    pop90 = d[d.period == 1990].set_index("iso3").pop_m
    keep = first[first <= 1965].index.intersection(pop90[pop90 >= 0.5].index)
    d["sample_B"] = d.iso3.isin(keep)
    oil = cy[(cy.year >= 1970) & (cy.year <= 2019)].groupby("iso3").oil_rents.mean()
    d["oil_mean"] = d.iso3.map(oil)
    d.to_parquet(PROC / f"{name}.parquet", index=False)
    return d


if __name__ == "__main__":
    m = build_mrw_original()
    print("MRW original:", len(m), "countries; N/I/O:", int(m.N.sum()), int(m.I.sum()), int(m.O.sum()))
    for s in ("rgdpch", "rgdpl"):
        b = build_barro70(s)
        print(f"Barro PWT7 ({s}):", b.iso3.nunique(), "countries,", len(b), "obs")
    cy = country_year()
    w = build_mrw_windows(cy)
    ok = w[w.sample_A].dropna(subset=["ln_y0", "dln_y", "ln_s", "ln_ngd", "ln_school"])
    print("Method A windows (complete, sample_A):", ok.groupby("start").size().to_dict())
    print("PHL in windows:", sorted(ok[ok.iso3 == "PHL"].start.tolist()))
    build_barro_panel(cy, step=10, name="barro_panel10")       # robustness B4
    build_barro_panel(cy, last=2019, name="barro_panel2019")    # robustness B5
    p = build_barro_panel(cy)
    s = p[p.sample_B]
    print("Method B panel:", s.iso3.nunique(), "countries,", len(s.dropna(subset=["growth", "ln_y", "ln_y_inst"])), "obs with growth")
    xs = ["inv_life", "ln_fert", "rule_law", "csh_i", "yrs_f", "yrs_m", "csh_g", "open", "tot_x_open", "democracy", "infl_c"]
    lags = [c + "_lag" for c in ["inv_life", "ln_fert", "rule_law", "csh_i", "csh_g", "open", "democracy", "infl_c"]]
    full = s.dropna(subset=["growth", "ln_y", "ln_y_inst"] + xs + lags)
    print("Method B with X:", full.iso3.nunique(), "countries,", len(full), "obs; periods", sorted(full.period.unique()))
    print("PHL periods with X:", sorted(full[full.iso3 == "PHL"].period.tolist()))
