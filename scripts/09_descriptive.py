"""Objective 1: descriptive facts about the Philippine growth path (RQ1).

Writes output/tables/desc_*.csv. Descriptive only; no hypothesis tests.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC, TABLES = ROOT / "data" / "processed", ROOT / "output" / "tables"
COUNTRIES = ["PHL", "IDN", "MYS", "THA", "VNM", "KOR", "CHN", "USA"]


def main():
    p = pd.read_parquet(PROC / "pwt11.parquet")
    w = pd.read_parquet(PROC / "wdi.parquet")
    p = p[p.iso3.isin(COUNTRIES)].copy()
    p["ypc_na"] = p.rgdpna / p["pop"]
    p["ypc_e"] = p.rgdpe / p["pop"]

    # growth of real GDP per person by decade (national-accounts series, PWT's recommendation for growth)
    rows = []
    for c, x in p.groupby("iso3"):
        x = x.set_index("year")
        for a, b in [(1960, 1970), (1970, 1980), (1980, 1990), (1990, 2000), (2000, 2010), (2010, 2019),
                     (2019, 2023), (1960, 2023)]:
            if a in x.index and b in x.index and x.loc[[a, b], "ypc_na"].notna().all():
                rows.append(dict(iso3=c, period=f"{a}-{b}",
                                 growth=100 * np.log(x.at[b, "ypc_na"] / x.at[a, "ypc_na"]) / (b - a)))
    g = pd.DataFrame(rows).pivot(index="period", columns="iso3", values="growth")[COUNTRIES]
    g.to_csv(TABLES / "desc_growth_decades.csv", float_format="%.2f")

    # GDP per person relative to the US (rgdpe: comparable across countries and over time)
    us = p[p.iso3 == "USA"].set_index("year").ypc_e
    rel = p.assign(rel=lambda z: 100 * z.ypc_e / z.year.map(us)).pivot(index="year", columns="iso3", values="rel")
    rel[COUNTRIES].to_csv(TABLES / "desc_relative_income.csv", float_format="%.2f")

    # large negative shocks: years in which Philippine GDP per person fell by more than 2%
    ph = p[p.iso3 == "PHL"].set_index("year")
    gr = 100 * np.log(ph.ypc_na).diff()
    shocks = gr[gr < -2].rename("growth").reset_index()
    shocks.to_csv(TABLES / "desc_shocks.csv", index=False, float_format="%.2f")
    pd.DataFrame({"year": gr.index, "growth": gr.values}).to_csv(TABLES / "desc_ph_growth_annual.csv", index=False,
                                                                 float_format="%.3f")

    # steady-state determinants, Philippines against peers
    ww = w[w.iso3.isin(COUNTRIES)]
    det = []
    for yr in (1970, 1995, 2022):
        a = p[p.year == yr].set_index("iso3")
        b = ww[ww.year == yr].set_index("iso3")
        for c in COUNTRIES:
            det.append(dict(year=yr, iso3=c, investment=a.csh_i.get(c), fertility=b.fertility.get(c),
                            life_exp=b.life_exp.get(c), hc=a.hc.get(c)))
    pd.DataFrame(det).to_csv(TABLES / "desc_determinants.csv", index=False, float_format="%.3f")

    pd.set_option("display.width", 200)
    print(g.round(2))
    print(rel.loc[[1960, 1980, 2000, 2019, 2023], COUNTRIES].round(1))
    print(shocks.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
