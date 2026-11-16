"""Write the scorecard and findings into README.md between the auto-generated markers.

Every number in the README comes from the data, so re-running the pipeline keeps it current.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pandas as pd

from .analysis import ALPHA, BASELINE_YEAR, STALE_AFTER, TREND_START

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START, END = "<!-- RESULTS:START -->", "<!-- RESULTS:END -->"


def fmt(v):
    if v is None or pd.isna(v):
        return "–"
    a = abs(v)
    return f"{v:,.0f}" if a >= 100 else f"{v:.1f}" if a >= 10 else f"{v:.2f}"


def has(v):
    return v is not None and not pd.isna(v)


def yr(v):
    return str(int(v)) if has(v) else "–"


def trend_cell(r):
    if r.status in ("Too little data", "Context only", "Out of date") or pd.isna(r.slope_per_year):
        return r.status
    return f"{r.status} ({fmt(r.slope_per_year)}/yr, p={r.p_value:.3f})"


def scorecard_markdown(card):
    lines = ["| Pillar | Indicator | Baseline | Latest | Trend since " f"{TREND_START} | Rank vs 3 peers |",
             "|---|---|---|---|---|---|"]
    for r in card.itertuples():
        base = f"{fmt(r.baseline)} ({yr(r.baseline_year)})" if has(r.baseline_year) else "–"
        latest = f"{fmt(r.latest)} ({yr(r.latest_year)})" if has(r.latest_year) else "No data"
        rank = f"{int(r.peer_rank)} of {int(r.n_ranked)} ({yr(r.rank_year)})" if has(r.peer_rank) else "–"
        name = f"{r.short_name} <sub>{r.unit}</sub>"
        lines.append(f"| {r.pillar} | {name} | {base} | {latest} | {trend_cell(r)} | {rank} |")
    return "\n".join(lines)


def findings(card, audit):
    out = []
    n = len(audit)
    usable = audit[audit.bhs_years > 0]
    gaps = audit[audit.gap != "OK"]
    out.append(
        f"**Data availability.** {len(usable)} of {n} indicators have any Bahamas data since 2000. "
        f"On average The Bahamas has a value for {audit.bhs_coverage.mean():.0%} of years, "
        f"against {audit.peer_coverage.mean():.0%} for Barbados, Jamaica and Trinidad and Tobago.")
    goals = pd.read_csv(ROOT / "config" / "goals.csv")
    covered = set(card.goal.str.extract(r"Goal (\d+)")[0].astype(int))
    missing = goals[~goals.goal.isin(covered)]
    line = f"**Goal coverage.** {len(goals) - len(missing)} of the plan's {len(goals)} goals have at least one indicator."
    if len(missing):
        line += (" Not yet covered: "
                 + "; ".join(f"Goal {r.goal} ({r.name.lower()})" for r in missing.itertuples())
                 + ". International data here is thin, so these will mostly need national sources.")
    out.append(line)
    if len(gaps):
        items = "; ".join(f"{r.short_name} ({r.gap}"
                          + (f", latest {yr(r.latest_year)}" if has(r.latest_year) else "") + ")"
                          for r in gaps.itertuples())
        out.append(f"**Gaps that would block monitoring** (no data, sparse, or more than {STALE_AFTER} "
                   f"years old): {items}.")

    scored = card[~card.status.isin(["Context only"])]
    counts = scored.status.value_counts()
    out.append("**Direction of travel since " f"{TREND_START}** (linear trend, {int((1 - ALPHA) * 100)}% "
               "confidence): " + ", ".join(f"{counts.get(k, 0)} {k.lower()}"
                                           for k in ["Improving", "Worsening", "No clear trend", "Too little data",
                                                     "Out of date"] if counts.get(k, 0))
               + f". The trend uses every year since {TREND_START}, so it can differ from the {BASELINE_YEAR}"
               "-to-latest change shown in brackets.")
    for status in ["Improving", "Worsening"]:
        rows = scored[scored.status == status]
        if len(rows):
            items = "; ".join(f"{r.short_name} ({fmt(r.baseline)} in {yr(r.baseline_year)} → {fmt(r.latest)} in {yr(r.latest_year)})"
                              if has(r.baseline_year) and r.baseline_year != r.latest_year
                              else f"{r.short_name} (latest {fmt(r.latest)}, {yr(r.latest_year)})"
                              for r in rows.itertuples())
            out.append(f"**{status}:** {items}.")

    # Ranks compare all four countries in the latest year they all have data (shown in brackets)
    ranked = card.dropna(subset=["peer_rank"])
    best = [f"{r.short_name} ({yr(r.rank_year)})" for r in ranked[ranked.peer_rank == 1].itertuples()]
    worst = [f"{r.short_name} ({yr(r.rank_year)})" for r in ranked[ranked.peer_rank == 4].itertuples()]
    if best:
        out.append(f"**Ahead of all three peers:** {', '.join(best)}.")
    if worst:
        out.append(f"**Behind all three peers:** {', '.join(worst)}.")
    return "\n\n".join(f"- {o}" for o in out)


def update_readme(card, audit, fetched_on=None):
    fetched_on = fetched_on or date.today().isoformat()
    block = "\n".join([
        START,
        f"_Generated from World Bank data downloaded on {fetched_on}. Baseline = nearest year to "
        f"{BASELINE_YEAR}. Re-run `python run_pipeline.py` to refresh._",
        "",
        "### Key findings",
        "",
        findings(card, audit),
        "",
        "### Indicator scorecard",
        "",
        scorecard_markdown(card),
        END,
    ])
    text = README.read_text()
    text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    README.write_text(text)
