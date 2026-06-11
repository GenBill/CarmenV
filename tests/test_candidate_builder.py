import pandas as pd

from carmenv.screening.candidate_builder import build_baseline_candidates


def test_baseline_candidate_rules_select_expected_ticker() -> None:
    features = pd.DataFrame(
        [
            {
                "date": "2026-06-11",
                "ticker": "PASS",
                "close": 120,
                "ma20": 100,
                "ma60": 90,
                "amount_ma20": 2_000_000,
                "return_20d": 0.12,
                "volatility_20d": 0.02,
            },
            {
                "date": "2026-06-11",
                "ticker": "FAIL",
                "close": 80,
                "ma20": 100,
                "ma60": 90,
                "amount_ma20": 2_000_000,
                "return_20d": 0.12,
                "volatility_20d": 0.02,
            },
        ]
    )
    candidates = build_baseline_candidates(features, "2026-06-11")
    assert candidates["ticker"].tolist() == ["PASS"]
    assert candidates.iloc[0]["source"] == "baseline_screen_v1"
