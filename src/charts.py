"""Charts for the README and notebook (matplotlib, saved as PNG)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

from .analysis import BASELINE_YEAR, FOCUS, PEERS

FIG_DIR = Path(__file__).resolve().parents[1] / "outputs" / "figures"

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e4e3df"
FOCUS_COLOR = "#2a78d6"      # The Bahamas
PEER_COLOR = "#b5b4ad"       # peers, recessive
EMPTY = "#efeeea"

HEADLINE = ["GOV_WGI_GE.EST", "VC.IHR.PSRC.P5", "SP.DYN.LE00.IN", "SH.DYN.MORT",
            "EG.FEC.RNEW.ZS", "NY.GDP.PCAP.KD", "GC.DOD.TOTL.GD.ZS", "SL.UEM.TOTL.ZS"]


def _style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2, "text.color": TEXT,
        "xtick.color": TEXT_2, "ytick.color": TEXT_2, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    })


def coverage_heatmap(df, indicators, audit, start=2000, end=None, save=True):
    """Which years have Bahamas data, by indicator, grouped by Vision 2040 pillar."""
    _style()
    end = end or int(df.year.max())
    years = list(range(start, end + 1))
    order = indicators.reset_index(drop=True)
    grid = np.zeros((len(order), len(years)))
    bhs = df[df.country == FOCUS]
    for i, code in enumerate(order.code):
        have = set(bhs[bhs.indicator == code].year)
        grid[i] = [y in have for y in years]

    fig, ax = plt.subplots(figsize=(12, 0.36 * len(order) + 1.6))
    ax.imshow(grid, aspect="auto", cmap=plt.matplotlib.colors.ListedColormap([EMPTY, FOCUS_COLOR]),
              vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks(np.arange(len(years))[::2], [str(y) for y in years[::2]])
    labels = [f"{r.pillar}  ·  {r.short_name}" for r in order.itertuples()]
    ax.set_yticks(np.arange(len(order)), labels)
    ax.set_xticks(np.arange(-0.5, len(years)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(order)), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.grid(which="major", visible=False)
    ax.tick_params(which="both", length=0)

    # Separators between pillars
    pillars = order.pillar.tolist()
    for i in range(1, len(pillars)):
        if pillars[i] != pillars[i - 1]:
            ax.axhline(i - 0.5, color=TEXT_2, linewidth=0.8)

    # Coverage share on the right
    cov = audit.set_index("indicator")["bhs_coverage"]
    for i, code in enumerate(order.code):
        ax.text(len(years) - 0.2, i, f" {cov.get(code, 0):.0%}", va="center", ha="left", fontsize=9, color=TEXT_2)
    ax.text(len(years) - 0.2, -0.9, " coverage", ha="left", fontsize=9, color=TEXT_2)

    ax.set_title(f"Which years have data for The Bahamas? World Bank indicators, {start}–{end}",
                 loc="left", pad=14)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout()
    if save:
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIG_DIR / "data_coverage.png", dpi=160, bbox_inches="tight")
    return fig


def peer_trends(df, indicators, codes=HEADLINE, save=True):
    """Small multiples: The Bahamas against Barbados, Jamaica and Trinidad and Tobago."""
    _style()
    meta = indicators.set_index("code")
    codes = [c for c in codes if c in set(df[df.country == FOCUS].indicator)]
    ncols = 4
    nrows = int(np.ceil(len(codes) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(15, 3.3 * nrows), squeeze=False)

    for ax, code in zip(axes.flat, codes):
        d = df[df.indicator == code]
        for p in PEERS:
            s = d[d.country == p]
            ax.plot(s.year, s.value, color=PEER_COLOR, linewidth=1.2)
        css = d[d.country == "CSS"]
        ax.plot(css.year, css.value, color=TEXT_2, linewidth=1.2, linestyle=(0, (3, 2)))
        s = d[d.country == FOCUS]
        ax.plot(s.year, s.value, color=FOCUS_COLOR, linewidth=2.4)
        ax.scatter(s.year.iloc[-1:], s.value.iloc[-1:], color=FOCUS_COLOR, s=28, zorder=3,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.axvline(BASELINE_YEAR, color=TEXT_2, linewidth=0.8, linestyle=":")
        arrow = {"up": "↑ better", "down": "↓ better"}.get(meta.at[code, "better"], "")
        ax.set_title(meta.at[code, "short_name"], loc="left", pad=20)
        ax.text(0, 1.02, f"{meta.at[code, 'unit']}   {arrow}", transform=ax.transAxes,
                fontsize=8.5, color=TEXT_2, va="bottom")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax.grid(axis="x", visible=False)
    for ax in list(axes.flat)[len(codes):]:
        ax.remove()

    handles = [
        plt.Line2D([], [], color=FOCUS_COLOR, linewidth=2.4, label="The Bahamas"),
        plt.Line2D([], [], color=PEER_COLOR, linewidth=1.2, label="Barbados, Jamaica, Trinidad & Tobago"),
        plt.Line2D([], [], color=TEXT_2, linewidth=1.2, linestyle=(0, (3, 2)), label="Caribbean small states"),
        plt.Line2D([], [], color=TEXT_2, linewidth=0.8, linestyle=":", label=f"{BASELINE_YEAR} baseline"),
    ]
    fig.tight_layout(rect=(0, 0, 1, 0.9), h_pad=2.5)
    fig.legend(handles=handles, loc="upper left", ncol=4, frameon=False, bbox_to_anchor=(0.005, 0.955))
    fig.suptitle("Vision 2040 headline indicators: The Bahamas vs Caribbean peers",
                 x=0.012, y=0.995, ha="left", fontsize=14, fontweight="bold")
    if save:
        FIG_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIG_DIR / "peer_trends.png", dpi=160, bbox_inches="tight")
    return fig
