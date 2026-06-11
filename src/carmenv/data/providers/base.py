from abc import ABC, abstractmethod

import pandas as pd


class MarketDataProvider(ABC):
    @abstractmethod
    def load_daily_bars(self) -> pd.DataFrame:
        raise NotImplementedError
