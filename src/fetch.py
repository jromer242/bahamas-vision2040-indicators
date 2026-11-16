"""Download World Bank indicators for The Bahamas and peer countries.

Uses the public World Bank API v2 (no key needed). Each indicator's raw JSON is cached in
data/raw/ so the analysis is reproducible and re-runs don't hit the API again.
"""
from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

API = "https://api.worldbank.org/v2"
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed" / "indicators_long.csv"


def load_config():
    indicators = pd.read_csv(ROOT / "config" / "indicators.csv", dtype={"source": "Int64"})
    countries = pd.read_csv(ROOT / "config" / "countries.csv")
    return indicators, countries


def _get_json(session, url, params, retries=5):
    # The World Bank API often returns 502s or stalls for a while. Back off: 5, 10, 20, 40 seconds.
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, timeout=(10, 60))  # (connect, read)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            if attempt == retries - 1:
                raise
            wait = 5 * 2 ** attempt
            print(f"  retry {attempt + 1}/{retries - 1} in {wait}s after error: {str(e)[:100]}")
            time.sleep(wait)


def fetch_indicator(code, country_codes, start, end, source=None, session=None, refresh=False):
    """Return (rows, status) for one indicator. status is 'ok', 'cached', or an error message."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache = RAW_DIR / f"{code}.json"
    if cache.exists() and not refresh:
        return json.loads(cache.read_text()), "cached"

    session = session or requests.Session()
    url = f"{API}/country/{';'.join(country_codes)}/indicator/{code}"
    params = {"format": "json", "date": f"{start}:{end}", "per_page": 1000}
    if source:
        params["source"] = int(source)

    rows, page, pages = [], 1, 1
    while page <= pages:
        payload = _get_json(session, url, {**params, "page": page})
        # Errors come back as [{"message": [...]}] with HTTP 200
        if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
            msg = payload[0].get("message", [{}])[0].get("value", "no data") if isinstance(payload, list) and payload else "no data"
            return [], f"not available ({msg})"
        pages = payload[0].get("pages", 1)
        rows += payload[1]
        page += 1

    cache.write_text(json.dumps(rows))
    return rows, "ok"


def to_frame(rows):
    out = []
    for r in rows:
        out.append({
            "indicator": r["indicator"]["id"],
            "indicator_name": r["indicator"]["value"],
            # Aggregates such as Caribbean small states have an ISO3-style code too
            "country": r.get("countryiso3code") or r["country"]["id"],
            "country_name": r["country"]["value"],
            "year": int(r["date"]),
            "value": r["value"],
        })
    return pd.DataFrame(out)


def fetch_all(start=2000, end=None, refresh=False, verbose=True):
    """Fetch every indicator in config/indicators.csv. Returns (long dataframe, fetch log)."""
    end = end or date.today().year
    indicators, countries = load_config()
    session = requests.Session()
    frames, log = [], []
    for ind in indicators.itertuples():
        src = None if pd.isna(ind.source) else ind.source
        try:
            rows, status = fetch_indicator(ind.code, countries.code.tolist(), start, end, src, session, refresh)
        except Exception as e:  # keep going; a failed indicator shows up in the data audit
            rows, status = [], f"request failed ({e})"
        if verbose:
            print(f"{ind.code:22s} {status:12.60s} {len(rows):4d} rows")
        log.append({"indicator": ind.code, "status": status, "rows": len(rows)})
        if rows:
            frames.append(to_frame(rows))
        if status == "ok":
            time.sleep(0.3)  # be polite to the API

    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["indicator", "indicator_name", "country", "country_name", "year", "value"])
    df = df.dropna(subset=["value"]).sort_values(["indicator", "country", "year"]).reset_index(drop=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)
    return df, pd.DataFrame(log)


if __name__ == "__main__":
    data, fetch_log = fetch_all()
    print(f"\n{len(data):,} observations saved to {PROCESSED}")
