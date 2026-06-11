from pathlib import Path

import pandas as pd

from carmenv.data.providers.base import MarketDataProvider


class CSVBarProvider(MarketDataProvider):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load_daily_bars(self) -> pd.DataFrame:
        df = pd.read_csv(self.path, parse_dates=["date"])
        df["date"] = df["date"].dt.date
        return df
