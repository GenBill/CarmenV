# CarmenV

CarmenV is a clean Python rewrite of the Carmen quantitative research system. It is **attribution-first**: every daily candidate, score, trade plan, forward return, and review should be persisted so the system can learn which signals actually work.

## Design goals

The target research flow is:

```text
data ingestion
  -> feature engineering
  -> candidate screening
  -> agent/scoring
  -> trade planning
  -> forward return tracking
  -> attribution analysis
  -> reports
```

The first version is intentionally small: it runs a toy pipeline from CSV bars, computes deterministic technical features, builds candidates, assigns non-LLM baseline scores, labels forward returns, and renders a weekly markdown report.

## Why attribution-first?

Daily stock picks are not useful unless CarmenV can later answer:

- Which screening rules generated the candidate?
- What did each score say at decision time?
- What happened over 1/3/5/10/20 trading days?
- Did high score buckets beat low score buckets?
- Which patterns worked in the current market regime?

Persisting intermediate research artifacts makes the answer auditable instead of anecdotal.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

If you use `uv`:

```bash
uv sync --extra dev
```

## Run the sample pipeline

```bash
carmenv init-db
carmenv run-sample
carmenv build-candidates --date 2026-06-11
carmenv update-forward-returns --horizons 1,3,5,10,20
carmenv report-weekly
```

The sample uses `examples/sample_daily_bars.csv`, writes DuckDB data under `data/`, and writes `reports_output/weekly_review.md`.

## What this version does not do

- No real broker integration.
- No automated trading.
- No live market data connection.
- No LLM or VLM API calls.
- No copied legacy Carmen implementation.

## Roadmap

1. Add production market-data providers for A-shares and US equities.
2. Persist manual trade reviews and actual fills.
3. Add sector strength and market-regime features.
4. Add structured LLM/VLM agents behind stable schemas.
5. Calibrate scoring weights from attribution statistics.
