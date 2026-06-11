# CarmenV Architecture

CarmenV uses a `src/` layout and keeps each research stage behind a small module boundary.

## Module boundaries

- `config/`: application settings and defaults.
- `data/`: provider interfaces, CSV loader, and raw data validation.
- `storage/`: DuckDB schema, paths, and append/delete-key upsert persistence.
- `features/`: trailing technical, market-regime, and sector-strength features.
- `screening/`: deterministic candidate rules that create daily candidate sets.
- `scoring/`: structured non-LLM baseline scores and future calibration helpers.
- `agents/`: prompt and schema placeholders only; no API calls in v1.
- `planning/`: trade-plan schema and position sizing utilities.
- `backtest/`: forward return labels, event studies, and attribution summaries.
- `reports/`: markdown reports for daily and weekly review.

The CLI orchestrates these modules but does not hide business logic inside command handlers.
