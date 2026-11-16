"""Run the whole project: fetch -> audit -> scorecard -> charts -> README.

    python run_pipeline.py            # uses cached API responses when present
    python run_pipeline.py --refresh  # re-download everything
"""
import argparse

import matplotlib
matplotlib.use("Agg")

from src import analysis, charts, fetch, report


def main(refresh=False):
    indicators, _ = fetch.load_config()
    df, log = fetch.fetch_all(refresh=refresh)
    print(f"\n{len(df):,} observations for {df.indicator.nunique()} indicators")

    audit = analysis.coverage_audit(df, indicators)
    card = analysis.scorecard(df, indicators)
    out = fetch.ROOT / "outputs"
    audit.to_csv(out / "data_coverage_audit.csv", index=False)
    card.to_csv(out / "indicator_scorecard.csv", index=False)
    log.to_csv(out / "fetch_log.csv", index=False)

    charts.coverage_heatmap(df, indicators, audit)
    charts.peer_trends(df, indicators)
    report.update_readme(card, audit)
    print("Saved outputs/ and updated README.md")
    print(card[["short_name", "latest_year", "latest", "status", "peer_rank"]].to_string(index=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download from the World Bank API")
    main(ap.parse_args().refresh)
