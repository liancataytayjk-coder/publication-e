"""Clean every raw source into tidy country-year tables (data/processed/*.parquet).

Nothing here makes a modelling choice beyond units and identifiers; choices
(periods, samples, transformations) are made in 03_build_panel.py and logged.
"""

import gzip
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC = ROOT / "data" / "raw", ROOT / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

WDI_NAMES = {
    "SP.DYN.LE00.IN": "life_exp", "SP.DYN.TFRT.IN": "fertility", "FP.CPI.TOTL.ZG": "infl_cpi",
    "NY.GDP.DEFL.KD.ZG": "infl_defl", "SP.POP.1564.TO": "wap", "SP.POP.TOTL": "pop_wdi",
    "SP.POP.TOTL.FE.IN": "pop_f", "SP.POP.TOTL.MA.IN": "pop_m", "SP.POP.1519.FE.5Y": "sh1519_f",
    "SP.POP.1519.MA.5Y": "sh1519_m", "SE.SEC.ENRR": "sec_enrol", "NY.GDP.PETR.RT.ZS": "oil_rents",
}


def clean_pwt11():
    p = pd.read_stata(RAW / "pwt" / "pwt110.dta")
    n = pd.read_stata(RAW / "pwt" / "pwt110_na_data.dta")
    keep = ["countrycode", "country", "year", "rgdpe", "rgdpo", "rgdpna", "pop", "emp", "hc", "csh_i", "csh_g",
            "csh_x", "csh_m", "pl_x", "pl_m", "rnna", "delta", "labsh", "pl_n", "pl_gdpo", "cgdpo", "rtfpna", "ctfp"]
    p = p[keep].merge(n[["countrycode", "year", "v_x", "v_m", "v_gdp", "q_gfcf", "q_gdp"]],
                      on=["countrycode", "year"], how="left")
    p = p.rename(columns={"countrycode": "iso3"})
    p["year"] = p.year.astype(int)
    p.to_parquet(PROC / "pwt11.parquet", index=False)
    return p


def clean_pwt70():
    z = zipfile.ZipFile(RAW / "pwt70" / "pwt70_06032011version.zip")
    p = pd.read_csv(z.open("pwt70_w_country_names.csv"))
    p = p.rename(columns={"isocode": "iso3", "POP": "pop"})[["country", "iso3", "year", "pop", "rgdpch", "rgdpl"]]
    p.to_parquet(PROC / "pwt70.parquet", index=False)
    return p


def clean_wdi():
    frames = []
    for code, name in WDI_NAMES.items():
        js = json.loads(gzip.decompress((RAW / "wdi" / f"{code}_1955_2025.json.gz").read_bytes()))
        rows = [(r["countryiso3code"], int(r["date"]), r["value"]) for r in js[1] if r["countryiso3code"]]
        frames.append(pd.DataFrame(rows, columns=["iso3", "year", name]).set_index(["iso3", "year"]))
    w = pd.concat(frames, axis=1).reset_index()
    w.to_parquet(PROC / "wdi.parquet", index=False)
    return w


def clean_barrolee():
    """Years of schooling, ages 25-64, by sex: population-weighted mean of the 10-year age groups."""
    out = []
    for sex, f in [("f", "BL_v3_F.csv"), ("m", "BL_v3_M.csv"), ("all", "BL_v3_MF.csv")]:
        b = pd.read_csv(RAW / "barrolee" / f)
        b = b[(b.agefrom >= 25) & (b.ageto <= 64)]
        g = b.groupby(["WBcode", "year"]).apply(lambda x: np.average(x.yr_sch, weights=x["pop"]), include_groups=False)
        out.append(g.rename(f"yrs_{sex}"))
    bl = pd.concat(out, axis=1).reset_index().rename(columns={"WBcode": "iso3"})
    bl.to_parquet(PROC / "barrolee.parquet", index=False)
    return bl


def clean_vdem():
    r = pd.read_csv(RAW / "owid" / "vdem_rule_of_law.csv").rename(columns={"rule_of_law_vdem__estimate_best": "rule_law"})
    d = pd.read_csv(RAW / "owid" / "vdem_electoral_democracy.csv").rename(columns={"electdem_vdem__estimate_best": "democracy"})
    v = r[["code", "year", "rule_law"]].merge(d[["code", "year", "democracy"]], on=["code", "year"], how="outer")
    v = v.rename(columns={"code": "iso3"}).dropna(subset=["iso3"])
    v = v[v.iso3.str.len() == 3]
    v.to_parquet(PROC / "vdem.parquet", index=False)
    return v


def clean_mrw():
    m = pd.read_csv(RAW / "mrw1992" / "MRW1992.txt", sep="\t", na_values="NA")
    m.to_parquet(PROC / "mrw1992.parquet", index=False)
    return m


if __name__ == "__main__":
    for f in (clean_pwt11, clean_pwt70, clean_wdi, clean_barrolee, clean_vdem, clean_mrw):
        df = f()
        print(f"{f.__name__}: {df.shape}")
