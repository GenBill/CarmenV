from pathlib import Path

import pandas as pd

from carmenv.data.providers.csv_provider import CSVBarProvider


def load_sample_daily_bars(path: str | Path = "examples/sample_daily_bars.csv") -> pd.DataFrame:
    return CSVBarProvider(path).load_daily_bars()
