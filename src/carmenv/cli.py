from pathlib import Path

import pandas as pd
import typer

from carmenv.backtest.forward_returns import compute_forward_returns
from carmenv.config.defaults import default_config
from carmenv.data.loaders import load_sample_daily_bars
from carmenv.data.validators import validate_daily_bars
from carmenv.features.technical import compute_technical_features
from carmenv.reports.weekly_review import render_weekly_review
from carmenv.scoring.baseline import score_candidates
from carmenv.screening.candidate_builder import build_baseline_candidates
from carmenv.storage.duckdb_store import DuckDBStore

app = typer.Typer(help="CarmenV attribution-first research pipeline")


def _store() -> DuckDBStore:
    cfg = default_config(Path.cwd())
    return DuckDBStore(cfg.db_path)


@app.command("init-db")
def init_db() -> None:
    """Initialize the DuckDB research database."""
    store = _store()
    store.initialize()
    typer.echo(f"Initialized DuckDB at {store.db_path}")


@app.command("run-sample")
def run_sample() -> None:
    """Run the toy end-to-end pipeline on examples/sample_daily_bars.csv."""
    cfg = default_config(Path.cwd())
    store = DuckDBStore(cfg.db_path)
    store.initialize()

    bars = load_sample_daily_bars(cfg.project_root / "examples" / "sample_daily_bars.csv")
    validate_daily_bars(bars)
    store.upsert_daily_bars(bars)

    features = compute_technical_features(bars)
    store.upsert_features(features)

    unique_dates = sorted(pd.to_datetime(bars["date"]).dt.date.unique())
    as_of_date = str(unique_dates[-21] if len(unique_dates) > 20 else unique_dates[-1])
    candidates = build_baseline_candidates(features, as_of_date, cfg.min_amount_ma20, cfg.top_n)
    store.upsert_candidates(candidates)

    scores = score_candidates(candidates)
    store.upsert_scores(scores)

    forward = compute_forward_returns(candidates, bars, [1, 3, 5, 10, 20])
    store.upsert_forward_returns(forward)

    report = render_weekly_review(candidates, scores, forward)
    cfg.reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = cfg.reports_dir / "weekly_review.md"
    report_path.write_text(report)
    typer.echo(report)
    typer.echo(f"Wrote {report_path}")


@app.command("build-candidates")
def build_candidates(
    date: str = typer.Option(..., "--date", help="Candidate date YYYY-MM-DD"),
) -> None:
    """Build and store baseline candidates for a date."""
    cfg = default_config(Path.cwd())
    store = DuckDBStore(cfg.db_path)
    bars = _load_bars_from_store_or_sample(store, cfg.project_root)
    features = compute_technical_features(bars)
    store.upsert_features(features)
    candidates = build_baseline_candidates(features, date, cfg.min_amount_ma20, cfg.top_n)
    store.upsert_candidates(candidates)
    scores = score_candidates(candidates)
    store.upsert_scores(scores)
    typer.echo(f"Built {len(candidates)} candidates for {date}")


@app.command("update-forward-returns")
def update_forward_returns(
    horizons: str = typer.Option("1,3,5,10,20", "--horizons", help="Comma-separated horizons"),
) -> None:
    """Compute and store forward returns for stored candidates."""
    cfg = default_config(Path.cwd())
    store = DuckDBStore(cfg.db_path)
    bars = _load_bars_from_store_or_sample(store, cfg.project_root)
    candidates = store.query_df("SELECT * FROM candidates")
    parsed_horizons = [int(item.strip()) for item in horizons.split(",") if item.strip()]
    forward = compute_forward_returns(candidates, bars, parsed_horizons)
    store.upsert_forward_returns(forward)
    typer.echo(f"Stored {len(forward)} forward return rows")


@app.command("report-weekly")
def report_weekly() -> None:
    """Render the latest weekly research review."""
    cfg = default_config(Path.cwd())
    store = DuckDBStore(cfg.db_path)
    store.initialize()
    candidates = store.query_df("SELECT * FROM candidates")
    scores = store.query_df("SELECT * FROM agent_scores")
    forward = store.query_df("SELECT * FROM forward_returns")
    report = render_weekly_review(candidates, scores, forward)
    cfg.reports_dir.mkdir(parents=True, exist_ok=True)
    path = cfg.reports_dir / "weekly_review.md"
    path.write_text(report)
    typer.echo(report)


def _load_bars_from_store_or_sample(store: DuckDBStore, root: Path) -> pd.DataFrame:
    store.initialize()
    bars = store.query_df("SELECT * FROM daily_bars")
    if bars.empty:
        bars = load_sample_daily_bars(root / "examples" / "sample_daily_bars.csv")
        validate_daily_bars(bars)
        store.upsert_daily_bars(bars)
    return bars


if __name__ == "__main__":
    app()
