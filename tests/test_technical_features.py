import pandas as pd

from carmenv.features.technical import compute_technical_features


def test_rolling_features_use_trailing_data_only() -> None:
    bars = pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=25),
            "ticker": ["AAA"] * 25,
            "open": range(1, 26),
            "high": [x + 0.5 for x in range(1, 26)],
            "low": [x - 0.5 for x in range(1, 26)],
            "close": range(1, 26),
            "volume": [1000] * 25,
            "amount": [10_000] * 25,
        }
    )
    features = compute_technical_features(bars)
    row5 = features.iloc[4]
    row6 = features.iloc[5]
    row21 = features.iloc[20]

    assert row5["ma5"] == 3
    assert row6["ma5"] == 4
    assert pd.isna(features.iloc[3]["ma5"])
    assert row21["return_20d"] == 20
    assert row21["ma20"] == 11.5
