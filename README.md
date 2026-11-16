# Vision 2040 Indicator Tracker: The Bahamas

A small monitoring-and-evaluation project. It tracks The Bahamas' progress on the four pillars of
[Vision 2040, the National Development Plan](https://observatorioplanificacion.cepal.org/en/plans/vision-2040-national-development-plan-bahamas),
using open World Bank data, and asks three questions:

1. **Can we measure it?** For each indicator, how complete and how current is the Bahamas data?
2. **Is it moving the right way?** Value at the 2016 baseline (when Vision 2040 planning began) against the latest
   value, plus a statistical test of the trend since 2010.
3. **How do we compare?** The Bahamas against Barbados, Jamaica, Trinidad and Tobago and the Caribbean
   small states average.

The plan's working draft sets out 16 goals but no published indicator set, so this project proposes 20
indicators, each mapped to a pillar and goal. The data-availability audit matters as much as the
trends: an indicator with no recent data can't be monitored.

![Headline indicators, The Bahamas vs Caribbean peers](outputs/figures/peer_trends.png)

![Data coverage by indicator and year](outputs/figures/data_coverage.png)

## Results

<!-- RESULTS:START -->
_Generated from World Bank data downloaded on 2026-11-16. Baseline = nearest year to 2016. Re-run `python run_pipeline.py` to refresh._

### Key findings

- **Data availability.** 19 of 20 indicators have any Bahamas data since 2000. On average The Bahamas has a value for 85% of years, against 87% for Barbados, Jamaica and Trinidad and Tobago.

- **Gaps that would block monitoring** (no data, sparse, or more than 3 years old): Intentional homicides (Out of date, latest 2022); Tertiary enrollment (No Bahamas data); Renewable energy share (Out of date, latest 2022); Tourism receipts share of exports (Out of date, latest 2020).

- **Direction of travel since 2010** (linear trend, 95% confidence): 6 improving, 5 worsening, 6 no clear trend, 1 too little data.

- **Improving:** Public education spending (2.59 in 2016 → 2.74 in 2023); Adolescent fertility (29.0 in 2016 → 24.5 in 2024); Protected areas (1.20 in 2016 → 8.30 in 2025); Internet users (80.0 in 2016 → 92.5 in 2024); Unemployment (12.7 in 2016 → 9.21 in 2025); Youth unemployment (25.8 in 2016 → 19.2 in 2025).

- **Worsening:** Government effectiveness (0.66 in 2016 → 0.65 in 2025); Control of corruption (1.09 in 2016 → 1.04 in 2025); Renewable energy share (1.20 in 2016 → 1.10 in 2022); CO2 emissions per capita (3.21 in 2016 → 3.64 in 2024); Central government debt (50.2 in 2016 → 71.5 in 2024).

- **Ahead of all three peers:** Government effectiveness, Adolescent fertility, Protected areas, Internet users, GDP per capita, GDP growth.

- **Behind all three peers:** Public education spending, Unemployment, Youth unemployment.

### Indicator scorecard

| Pillar | Indicator | Baseline | Latest | Trend since 2010 | Rank vs 3 peers |
|---|---|---|---|---|---|
| Governance | Government effectiveness <sub>index (-2.5 to 2.5)</sub> | 0.66 (2016) | 0.65 (2025) | Worsening (-0.02/yr, p=0.001) | 1 of 4 |
| Governance | Control of corruption <sub>index (-2.5 to 2.5)</sub> | 1.09 (2016) | 1.04 (2025) | Worsening (-0.02/yr, p=0.007) | 2 of 4 |
| Governance | Intentional homicides <sub>per 100k people</sub> | 28.6 (2016) | 32.2 (2022) | No clear trend (-0.39/yr, p=0.331) | 2 of 4 |
| Human Capital | Life expectancy at birth <sub>years</sub> | 74.0 (2016) | 74.7 (2024) | No clear trend (-0.01/yr, p=0.920) | 2 of 4 |
| Human Capital | Under-5 mortality <sub>per 1k live births</sub> | 13.8 (2016) | 12.4 (2024) | No clear trend (-0.11/yr, p=0.522) | 2 of 4 |
| Human Capital | Health spending <sub>% of GDP</sub> | 5.66 (2016) | 6.30 (2023) | Context only | – |
| Human Capital | Public education spending <sub>% of GDP</sub> | 2.59 (2016) | 2.74 (2023) | Improving (0.06/yr, p=0.023) | 4 of 4 |
| Human Capital | Tertiary enrollment <sub>% gross</sub> | – | No data | Too little data | – |
| Human Capital | Adolescent fertility <sub>births per 1k women 15-19</sub> | 29.0 (2016) | 24.5 (2024) | Improving (-1.04/yr, p=0.000) | 1 of 4 |
| Environment | Renewable energy share <sub>% of final energy use</sub> | 1.20 (2016) | 1.10 (2022) | Worsening (-0.02/yr, p=0.013) | 3 of 4 |
| Environment | CO2 emissions per capita <sub>t CO2e per person</sub> | 3.21 (2016) | 3.64 (2024) | Worsening (0.06/yr, p=0.008) | 3 of 4 |
| Environment | Protected areas <sub>% of territory</sub> | 1.20 (2016) | 8.30 (2025) | Improving (0.76/yr, p=0.001) | 1 of 4 |
| Environment | Internet users <sub>% of population</sub> | 80.0 (2016) | 92.5 (2024) | Improving (2.75/yr, p=0.000) | 1 of 4 |
| Economy | GDP per capita <sub>constant 2015 US$</sub> | 30,152 (2016) | 33,968 (2024) | No clear trend (75.0/yr, p=0.556) | 1 of 4 |
| Economy | GDP growth <sub>annual %</sub> | -1.16 (2016) | 3.38 (2024) | No clear trend (0.27/yr, p=0.587) | 1 of 4 |
| Economy | Inflation <sub>annual %</sub> | -0.35 (2016) | 1.11 (2025) | No clear trend (0.04/yr, p=0.644) | 3 of 4 |
| Economy | Central government debt <sub>% of GDP</sub> | 50.2 (2016) | 71.5 (2024) | Worsening (3.48/yr, p=0.000) | – |
| Economy | Tourism receipts share of exports <sub>% of exports</sub> | 79.6 (2016) | 59.6 (2020) | Context only | – |
| Economy | Unemployment <sub>% of labour force</sub> | 12.7 (2016) | 9.21 (2025) | Improving (-0.44/yr, p=0.000) | 4 of 4 |
| Economy | Youth unemployment <sub>% of ages 15-24</sub> | 25.8 (2016) | 19.2 (2025) | Improving (-0.85/yr, p=0.000) | 4 of 4 |
<!-- RESULTS:END -->

## Method

| Step | What it does |
|---|---|
| **Indicator framework** | `config/indicators.csv` maps 20 World Bank indicators to the Vision 2040 pillars (Governance, Human Capital, Environment, Economy) and goals, with the desired direction for each (higher or lower is better). Health spending and tourism's share of exports are tracked as context, with no target direction. |
| **Data collection** | `src/fetch.py` calls the [World Bank API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392) for The Bahamas, three peers and the Caribbean small states aggregate, 2000 to today. Raw responses are cached in `data/raw/` for reproducibility. Indicators the API doesn't return are logged, not dropped. |
| **Data audit** | Share of years with a value, first and latest year, and a gap flag: *no data*, *out of date* (latest value more than 3 years old) or *sparse* (under 50% of years). |
| **Baseline vs latest** | Baseline is the observation nearest to 2016, within ±2 years. |
| **Trend test** | OLS regression of value on year, 2010 onward, with at least 6 observations. A trend counts as *improving* or *worsening* only when the slope's p-value is below 0.05. Otherwise it is *no clear trend*. |
| **Peer comparison** | The Bahamas is ranked against Barbados, Jamaica and Trinidad and Tobago on each country's latest value (1 = best). |

## Limitations

- **Simple trend model.** A straight-line trend on annual data is a screening tool, not a forecast. Shocks such
  as COVID-19 in 2020 and Hurricane Dorian in 2019 pull the slope around. Annual series are also often
  autocorrelated, which makes the p-values optimistic.
- **Not like-for-like across countries.** Peers' latest values can come from different years, so the
  ranks are indicative.
- **Proposed indicators, not official ones.** These are World Bank series chosen to fit the plan's goals,
  not an official Vision 2040 results framework. National sources such as the
  [Bahamas National Statistical Institute](https://www.bahamas.gov.bs/statistics) may hold more recent
  figures.
- **Possible code changes.** The governance indicators come from the Worldwide Governance Indicators
  (World Bank source 3). If the API stops returning them, the audit shows it.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name bahamas-vision2040 --display-name "Python (bahamas-vision2040)"
python run_pipeline.py          # fetch, analyse, chart, and rewrite the Results section
jupyter notebook notebooks/vision2040_indicators.ipynb   # walkthrough
```

To add an indicator, add a row to `config/indicators.csv` with its
[World Bank code](https://data.worldbank.org/indicator). To change the comparison countries, edit
`config/countries.csv`.

## Project structure

```
config/        indicator framework and countries
src/fetch.py   World Bank API client with caching
src/analysis.py  coverage audit, baseline vs latest, OLS trend tests, peer ranks
src/charts.py  figures
src/report.py  writes the Results section of this README
notebooks/     step-by-step walkthrough
outputs/       scorecard and audit CSVs, figures
```

**Data:** World Bank, World Development Indicators and Worldwide Governance Indicators (CC BY 4.0).
**Author:** Jyles Romer
