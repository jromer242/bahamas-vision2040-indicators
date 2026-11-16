"""Indicator analysis: data availability audit, baseline vs latest, trend tests, peer comparison."""
from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import statsmodels.api as sm

FOCUS = "BHS"
PEERS = ["BRB", "JAM", "TTO"]
BASELINE_YEAR = 2016     # Vision 2040 planning began in 2016; 2nd working draft published 2017
BASELINE_WINDOW = 2      # accept the nearest observation within +/- 2 years
TREND_START = 2010       # trend tests use observations from this year on
MIN_TREND_POINTS = 6
ALPHA = 0.05
STALE_AFTER = 3          # latest value older than this many years counts as out of date


def coverage_audit(df, indicators, start=2000, end=None):
    """How much Bahamas data exists for each indicator, compared with peers."""
    end = end or int(df.year.max())   # latest year published for any country
    span = end - start + 1
    rows = []
    for ind in indicators.itertuples():
        d = df[(df.indicator == ind.code) & df.year.between(start, end)]
        bhs = d[d.country == FOCUS]
        peer_cov = [d[d.country == p].year.nunique() / span for p in PEERS]
        latest = int(bhs.year.max()) if len(bhs) else None
        rows.append({
            "indicator": ind.code, "short_name": ind.short_name, "pillar": ind.pillar,
            "bhs_years": bhs.year.nunique(),
            "bhs_coverage": bhs.year.nunique() / span,
            "peer_coverage": float(np.mean(peer_cov)),
            "first_year": int(bhs.year.min()) if len(bhs) else None,
            "latest_year": latest,
            "years_out_of_date": (end + 1 - latest) if latest else None,
        })
    out = pd.DataFrame(rows)
    out["gap"] = np.select(
        [out.bhs_years == 0, out.years_out_of_date > STALE_AFTER, out.bhs_coverage < 0.5],
        ["No Bahamas data", "Out of date", "Sparse series"], default="OK")
    return out


def baseline_latest(series: pd.Series):
    """series: values indexed by year. Returns (baseline_year, baseline, latest_year, latest)."""
    s = series.dropna().sort_index()
    if s.empty:
        return None, None, None, None
    near = s[(s.index >= BASELINE_YEAR - BASELINE_WINDOW) & (s.index <= BASELINE_YEAR + BASELINE_WINDOW)]
    if near.empty:
        b_year = b_val = None
    else:
        b_year = int(min(near.index, key=lambda y: (abs(y - BASELINE_YEAR), y)))
        b_val = float(near[b_year])
    return b_year, b_val, int(s.index[-1]), float(s.iloc[-1])


def trend_test(series: pd.Series):
    """OLS of value on year since TREND_START. Returns slope per year, 95% CI, p-value, n."""
    s = series.dropna()
    s = s[s.index >= TREND_START]
    if len(s) < MIN_TREND_POINTS:
        return {"n": len(s), "slope": np.nan, "ci_low": np.nan, "ci_high": np.nan, "p_value": np.nan}
    X = sm.add_constant(np.asarray(s.index, dtype=float))
    fit = sm.OLS(np.asarray(s.values, dtype=float), X).fit()
    lo, hi = fit.conf_int(alpha=ALPHA)[1]
    return {"n": len(s), "slope": fit.params[1], "ci_low": lo, "ci_high": hi, "p_value": fit.pvalues[1]}


def classify(better, t):
    if better == "none":
        return "Context only"
    if np.isnan(t["slope"]):
        return "Too little data"
    if t["p_value"] >= ALPHA:
        return "No clear trend"
    improving = (t["slope"] > 0) == (better == "up")
    return "Improving" if improving else "Worsening"


def peer_rank(df, code, better):
    """Rank The Bahamas among itself and the three peers on each country's latest value (1 = best)."""
    latest = (df[(df.indicator == code) & df.country.isin([FOCUS] + PEERS)]
              .sort_values("year").groupby("country").tail(1).set_index("country"))
    # Only compare values from roughly the same period
    latest = latest[latest.year >= latest.year.max() - STALE_AFTER] if len(latest) else latest
    if FOCUS not in latest.index or better == "none" or len(latest) < 2:
        return None, len(latest)
    ranks = latest["value"].rank(ascending=(better == "down"), method="min")
    return int(ranks[FOCUS]), len(latest)


def scorecard(df, indicators):
    rows = []
    for ind in indicators.itertuples():
        s = df[(df.indicator == ind.code) & (df.country == FOCUS)].set_index("year")["value"]
        b_year, b_val, l_year, l_val = baseline_latest(s)
        t = trend_test(s)
        rank, n_ranked = peer_rank(df, ind.code, ind.better)
        css = df[(df.indicator == ind.code) & (df.country == "CSS")].sort_values("year")
        rows.append({
            "pillar": ind.pillar, "goal": ind.goal, "indicator": ind.code, "short_name": ind.short_name,
            "unit": ind.unit, "better": ind.better,
            "baseline_year": b_year, "baseline": b_val, "latest_year": l_year, "latest": l_val,
            "change": (l_val - b_val) if b_val is not None and l_val is not None else None,
            "trend_n": t["n"], "slope_per_year": t["slope"], "slope_ci_low": t["ci_low"],
            "slope_ci_high": t["ci_high"], "p_value": t["p_value"],
            "status": classify(ind.better, t),
            "peer_rank": rank, "n_ranked": n_ranked,
            "caribbean_small_states_latest": float(css.value.iloc[-1]) if len(css) else None,
        })
    return pd.DataFrame(rows)
