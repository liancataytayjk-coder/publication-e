"""Download every raw file used by the study, unchanged.

Each file is saved under data/raw/<source>/ exactly as served (World Bank API
responses are gzipped JSON). Every file has a row in data/raw/source_log.md.
Run with --force to re-download files that already exist.

Sources
  pwt       Penn World Table 11.0 (main data, 1950-2023)
  pwt70     Penn World Table 7.0 (Barro 2015 replication)
  mrw1992   Mankiw, Romer & Weil (1992) dataset, as distributed by B. Hansen
  wdi       World Development Indicators API (life expectancy, fertility,
            inflation, working-age population, secondary enrolment)
  barrolee  Barro-Lee educational attainment v3, by sex
  owid      V-Dem rule-of-law and electoral-democracy indices via Our World in Data
"""

import gzip
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

FILES = {
    "pwt/pwt110.dta": "https://dataverse.nl/api/access/datafile/554030",
    "pwt/pwt110_na_data.dta": "https://dataverse.nl/api/access/datafile/554024",
    "pwt70/pwt70_06032011version.zip": "https://www.rug.nl/ggdc/docs/pwt70_06032011version.zip",
    "pwt70/pwt70_vars_forweb.xls": "https://www.rug.nl/ggdc/docs/pwt70_vars_forweb.xls",
    "mrw1992/MRW1992.txt": "https://www.ssc.wisc.edu/~bhansen/econometrics/MRW1992.txt",
    "barrolee/BL_v3_F.csv": "https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL_v3_F.csv",
    "barrolee/BL_v3_M.csv": "https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL_v3_M.csv",
    "barrolee/BL_v3_MF.csv": "https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL_v3_MF.csv",
    "owid/vdem_rule_of_law.csv": "https://ourworldindata.org/grapher/rule-of-law-index.csv?v=1&csvType=full&useColumnShortNames=true",
    "owid/vdem_electoral_democracy.csv": "https://ourworldindata.org/grapher/electoral-democracy-index.csv?v=1&csvType=full&useColumnShortNames=true",
}

WDI = {
    "SP.DYN.LE00.IN": "life expectancy at birth",
    "SP.DYN.TFRT.IN": "total fertility rate",
    "FP.CPI.TOTL.ZG": "CPI inflation, annual %",
    "NY.GDP.DEFL.KD.ZG": "GDP deflator inflation, annual %",
    "SP.POP.1564.TO": "population aged 15-64",
    "SP.POP.TOTL": "population, total",
    "SP.POP.TOTL.FE.IN": "population, female",
    "SP.POP.TOTL.MA.IN": "population, male",
    "SP.POP.1519.FE.5Y": "population aged 15-19, female (% of female population)",
    "SP.POP.1519.MA.5Y": "population aged 15-19, male (% of male population)",
    "SE.SEC.ENRR": "school enrolment, secondary (% gross)",
    "NY.GDP.PETR.RT.ZS": "oil rents (% of GDP)",
}


def get(url, tries=4):
    for k in range(tries):
        try:
            r = requests.get(url, timeout=180, headers={"User-Agent": "publication-e research download"})
            r.raise_for_status()
            return r.content
        except requests.RequestException as e:
            if k == tries - 1:
                raise
            print("  retry after", e)
            time.sleep(2 ** (k + 1))


def main(force=False):
    for rel, url in FILES.items():
        out = RAW / rel
        if out.exists() and not force:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        print("downloading", rel)
        out.write_bytes(get(url))
    for code in WDI:
        out = RAW / "wdi" / f"{code}_1955_2025.json.gz"
        if out.exists() and not force:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=30000&date=1955:2025"
        print("downloading WDI", code)
        out.write_bytes(gzip.compress(get(url), mtime=0))


if __name__ == "__main__":
    main(force="--force" in sys.argv)
