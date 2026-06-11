import pandas as pd
import pytest

from carmenv.backtest.forward_returns import compute_forward_returns


def test_forward_returns_and_path_extremes() -> None:
    bars = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=5),
            "ticker": ["AAA"] * 5,
            "open": [10, 11, 9, 13, 12],
            "high": [10, 12, 10, 14, 13],
            "low": [10, 10, 8, 12, 11],
            "close": [10, 11, 9, 13, 12],
            "volume": [1000] * 5,
            "amount": [10_000] * 5,
        }
    )
    candidates = pd.DataFrame({"date": [pd.Timestamp("2026-01-01")], "ticker": ["AAA"]})
    result = compute_forward_returns(candidates, bars, [1, 3])

    h1 = result[result["horizon_days"] == 1].iloc[0]
    h3 = result[result["horizon_days"] == 3].iloc[0]
    assert h1["return_pct"] == pytest.approx(0.1)
    assert h1["max_drawdown_pct"] == pytest.approx(0.0)
    assert h1["max_runup_pct"] == pytest.approx(0.2)
    assert h3["return_pct"] == pytest.approx(0.3)
    assert h3["max_drawdown_pct"] == pytest.approx(-0.2)
    assert h3["max_runup_pct"] == pytest.approx(0.4)
