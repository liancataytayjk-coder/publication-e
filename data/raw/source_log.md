# Raw data source log

One row per raw file. Files in `data/raw/` are never edited.

| File | Source / URL | Date pulled | Base year / units | Coverage | SHA-256 | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `pwt/pwt110.dta` | Penn World Table 11.0, Groningen Growth and Development Centre. Dataverse doi:10.34894/FABVLR; file https://dataverse.nl/api/access/datafile/554030 | 2026-10-15 | 2021 US$ (PPP and national-accounts series) | 185 countries, 1950–2023 | `2a0d214958dd46ad6cb9966f5dfa2fc8ad546475c79ed70564caf7383777aaa1` | Main PWT file: rgdpna, rnna, emp, hc, rtfpna, delta, labsh, pl_n, pl_gdpo, cgdpo, ctfp. |
| `pwt/pwt110_na_data.dta` | Same dataset; file https://dataverse.nl/api/access/datafile/554024 | 2026-10-15 | National currency, current (v_) and constant 2021 (q_) prices | 1950–2025 (most series end 2023) | `238e23459de1a96b686873cf9e45473854a55da28ddc9e002b12473340dbc105` | National-accounts inputs: q_gfcf, q_gdp used for the real investment share. |

Cite as: Feenstra, R. C., Inklaar, R., & Timmer, M. P. (2015). The next generation of the Penn World Table. *American Economic Review, 105*(10), 3150–3182.
