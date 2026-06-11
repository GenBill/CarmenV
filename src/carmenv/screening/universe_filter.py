import pandas as pd


def active_symbols(symbols: pd.DataFrame) -> pd.DataFrame:
    if symbols.empty or "is_active" not in symbols:
        return symbols.copy()
    return symbols[symbols["is_active"]].copy()
