"""All manuscript figures, black and white, from saved tables (Phase 5).

Writes output/figures/fig*.{png,tiff,pdf}. No titles inside images; captions are in the manuscript.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import fig_style as fs  # noqa: E402

T, OUT, EXP = ROOT / "output" / "tables", ROOT / "output" / "figures", ROOT / "output" / "exploration"
NAMES = {"PHL": "Philippines", "IDN": "Indonesia", "MYS": "Malaysia", "THA": "Thailand", "VNM": "Viet Nam",
         "KOR": "Korea", "CHN": "China", "USA": "United States"}


def fig1_relative_income():
    r = pd.read_csv(T / "desc_relative_income.csv", index_col=0)
    fig, ax = plt.subplots(figsize=(5.5, 3.3))
    styles = {"PHL": fs.A, "THA": fs.B, "IDN": fs.C, "MYS": dict(color=fs.MID, linestyle="-.", marker="d",
                                                              markersize=3.5, markerfacecolor="white")}
    for c, st in styles.items():
        s = r[c].dropna()
        ax.plot(s.index, s.values, label=NAMES[c], **(st | {"markevery": 5}))
    ax.set_xlim(1960, 2024)
    ax.set_ylim(0, 50)
    ax.set_ylabel("GDP per person, % of the United States")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    fs.save(fig, "fig1_relative_income", OUT)


def fig2_capital_output():
    g = pd.read_csv(EXP / "steady_state_gap.csv")
    ph = g[g.countrycode == "PHL"].set_index("year")
    fig, ax = plt.subplots(figsize=(5.5, 3.3))
    ax.plot(ph.index, ph.ky, label="Actual K/Y", **(fs.A | {"markevery": 2}))
    ax.plot(ph.index, ph.ky_star, label="Steady-state K/Y = s/(n + g + δ), g = 0.02", **(fs.B | {"markevery": 2}))
    ax.set_xlim(1970, 2024)
    ax.set_ylabel("Capital-output ratio (national prices)")
    ax.set_xlabel("Year")
    ax.legend(loc="lower right")
    fs.save(fig, "fig2_capital_output", OUT)


def fig3_replication():
    g = pd.read_csv(T / "replication_gate.csv")
    g = g[np.isfinite(g.lo) & (g.criterion.str.contains("N$") == False)]  # noqa: E712
    g = g[~g.criterion.str.contains("minus")]
    g["rel"] = (g.estimate - g.target) / (g.hi - g.lo) * 2  # distance from target in half-widths of the pass band
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    y = np.arange(len(g))[::-1]
    ax.axvspan(-1, 1, color=fs.LIGHT, linewidth=0)
    ax.plot(g.rel, y, "o", color=fs.BLACK, markersize=4)
    ax.axvline(0, color=fs.BLACK, linewidth=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels([c.replace("; not significantly negative", "").replace("; significant at 1%", "")
                        for c in g.criterion], fontsize=7)
    ax.set_xlim(-1.6, 1.6)
    ax.set_xlabel("Estimate minus published value, in half-widths of the pass band")
    fs.save(fig, "fig3_replication", OUT)


def fig4_distance():
    d = pd.read_csv(T / "ph_distance.csv")
    b = d[(d.method == "B") & (d.spec == "main")].sort_values("year")
    a = d[(d.method == "A") & (d.spec == "main")].sort_values("year")
    fig, ax = plt.subplots(figsize=(5.5, 3.4))
    ax.fill_between(b.year, b.lo, b.hi, color=fs.LIGHT, linewidth=0)
    ax.plot(b.year, b.d, label="Method B (Barro panel), start of each 5-year period", **fs.A)
    ax.errorbar(a.year, a.d, yerr=[a.d - a.lo, a.hi - a.d], fmt="s", color=fs.BLACK, markerfacecolor="white",
                markersize=4, capsize=2, linewidth=0.8, label="Method A (MRW cross-section), end of 25-year window")
    fs.zero(ax)
    ax.set_xlim(1962, 2025)
    ax.set_ylabel("d = ln y − ln y* (log points)")
    ax.set_xlabel("Year")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), fontsize=7.5, ncol=1)
    fs.save(fig, "fig4_distance", OUT)


def fig5_decomposition():
    dec = pd.read_csv(T / "decomposition.csv")
    x = np.arange(len(dec))
    parts = [("closing", "Closing (convergence)", dict(color=fs.DARK)),
             ("world_shock", "World shock", dict(color="white", edgecolor=fs.BLACK, hatch="////")),
             ("ph_shock", "Philippine shock", dict(color=fs.MID)),
             ("neg_move", "Steady state moving (−)", dict(color="white", edgecolor=fs.BLACK, hatch="...."))]
    dec["neg_move"] = -dec.target_move
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    pos, neg = np.zeros(len(dec)), np.zeros(len(dec))
    for col, lab, st in parts:
        v = dec[col].values
        bottom = np.where(v >= 0, pos, neg)
        ax.bar(x, v, 0.7, bottom=bottom, label=lab, linewidth=0.5, **({"edgecolor": fs.BLACK} | st))
        pos += np.where(v >= 0, v, 0)
        neg += np.where(v < 0, v, 0)
    ax.plot(x, dec.delta_d, "o", color=fs.BLACK, markerfacecolor="white", markersize=5, label="Change in d (total)",
            zorder=5)
    fs.zero(ax)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{a}–{str(b)[2:]}" for a, b in zip(dec.period, dec.next)], rotation=45, fontsize=7.5)
    ax.set_ylabel("Change in d (log points)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=7, ncol=3)
    fs.save(fig, "fig5_decomposition", OUT)


def fig6_speed():
    s = pd.read_csv(T / "speed.csv")
    rec = pd.read_csv(T / "reconciliation.csv")
    rows = []
    for r in s.itertuples():
        if r.method == "A":
            rows.append((f"A: MRW, {r.window}", r.lam, r.lo, r.hi))
    rows = sorted(set(rows), key=lambda z: z[0])
    b = s[s.method == "B"].set_index("spec")
    rows += [("B: Barro, X variables (main)", b.at["main", "lam"], b.at["main", "lo"], b.at["main", "hi"]),
             ("B: country fixed effects, raw", b.at["fe_raw", "lam"], np.nan, np.nan),
             ("B: fixed effects, bias-corrected", b.at["fe_corrected", "lam"], np.nan, np.nan)]
    r1 = rec[rec.check.str.startswith("R1")].iloc[0]
    rows.append(("B: MRW determinants in panel (R1)", r1.lam, np.nan, np.nan))
    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    y = np.arange(len(rows))[::-1]
    for yi, (lab, lam, lo, hi) in zip(y, rows):
        if np.isfinite(lo):
            ax.plot([100 * lo, 100 * hi], [yi, yi], color=fs.BLACK, linewidth=1)
        ax.plot(100 * lam, yi, "o" if lab.startswith("A") else "s", color=fs.BLACK,
                markerfacecolor=fs.BLACK if lab.startswith("A") else "white", markersize=4.5)
    ax.axvline(2, color=fs.BLACK, linestyle=":", linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=7)
    ax.set_xlabel("Speed of convergence λ (% of the gap closed per year)")
    ax.set_xlim(0, 4.5)
    fs.save(fig, "fig6_speed", OUT)


def fig7_robustness():
    r = pd.read_csv(T / "robustness.csv")
    r = r[r.d_latest.notna() & ~r.check.str.contains("time-effect trend")]
    fig, ax = plt.subplots(figsize=(5.5, 5.0))
    y = np.arange(len(r))[::-1]
    for yi, row in zip(y, r.itertuples()):
        mk = "o" if row.method == "B" else "s"
        ax.plot(row.d_latest, yi, mk, color=fs.BLACK, markerfacecolor=fs.BLACK if row.method == "B" else "white",
                markersize=4.5)
    fs.zero(ax, horizontal=False)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c} ({int(yr)})" for c, yr in zip(r.check, r.year_latest)], fontsize=6.5)
    ax.set_xlabel("Philippine distance d at the latest date (log points)")
    fs.save(fig, "fig7_robustness", OUT)


def fig8_policy():
    p = pd.read_csv(T / "policy.csv")
    p["label"] = np.where(p.method == "A", "A: " + p.determinant, "B: " + p.determinant)
    p = p.sort_values("gain_ln_ystar")
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    y = np.arange(len(p))
    ax.barh(y, 100 * p.gain_ln_ystar, 0.6, color=[fs.MID if m == "B" else "white" for m in p.method],
            edgecolor=fs.BLACK, linewidth=0.6, hatch=None)
    fs.zero(ax, horizontal=False)
    ax.set_yticks(y)
    ax.set_yticklabels(p.label, fontsize=7.5)
    ax.set_xlabel("Change in the steady-state level of GDP per person (log points × 100)")
    fs.save(fig, "fig8_policy", OUT)


def fig9_framework():
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, text, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fill=False, edgecolor=fs.BLACK,
                                    linewidth=0.9, linestyle="--" if dashed else "-"))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7, linespacing=1.3)

    def arrow(a, b, dashed=False):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=9, color=fs.BLACK, linewidth=0.9,
                                     linestyle="--" if dashed else "-"))

    box(0.2, 4.0, 3.4, 2.6, "Steady-state determinants\ninvestment s, schooling h,\npopulation growth n, fertility,\n"
        "health, institutions,\nmacro stability")
    box(0.2, 0.3, 3.4, 1.9, "Policy levers\ninvestment climate, education,\nhealth, rule of law,\nlow inflation",
        dashed=True)
    box(4.6, 4.5, 3.0, 1.6, "Steady-state path\nln y*, rising at g*")
    box(4.6, 0.6, 3.0, 1.4, "Shocks\nworld and Philippine")
    box(8.6, 2.5, 3.2, 2.0, "Actual income ln y\ndistance d = ln y − ln y*\ncloses at speed λ")
    arrow((3.7, 5.3), (4.5, 5.3))
    arrow((1.9, 2.3), (1.9, 3.9), dashed=True)
    arrow((7.7, 5.3), (8.9, 4.6))
    arrow((7.7, 1.3), (8.9, 2.4))
    ax.text(8.6, 5.25, "target", fontsize=7, ha="center")
    ax.text(8.75, 1.45, "push off path", fontsize=7, ha="center")
    fs.save(fig, "fig9_framework", OUT)


if __name__ == "__main__":
    fs.setup()
    for f in (fig1_relative_income, fig2_capital_output, fig3_replication, fig4_distance, fig5_decomposition,
              fig6_speed, fig7_robustness, fig8_policy, fig9_framework):
        f()
        print("wrote", f.__name__)
