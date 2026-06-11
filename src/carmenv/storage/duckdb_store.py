from pathlib import Path

import duckdb
import pandas as pd

from carmenv.storage.paths import schema_path


class DuckDBStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as con:
            con.execute(schema_path().read_text())

    def upsert_daily_bars(self, df: pd.DataFrame) -> None:
        self._upsert(df, "daily_bars", ["date", "ticker"])

    def upsert_features(self, df: pd.DataFrame) -> None:
        self._upsert(df, "technical_features", ["date", "ticker"])

    def upsert_candidates(self, df: pd.DataFrame) -> None:
        self._upsert(df, "candidates", ["date", "ticker", "source"])

    def upsert_scores(self, df: pd.DataFrame) -> None:
        self._upsert(df, "agent_scores", ["date", "ticker"])

    def upsert_trade_plans(self, df: pd.DataFrame) -> None:
        self._upsert(df, "trade_plans", ["date", "ticker"])

    def upsert_forward_returns(self, df: pd.DataFrame) -> None:
        self._upsert(df, "forward_returns", ["date", "ticker", "horizon_days"])

    def query_df(
        self, sql: str, params: list[object] | tuple[object, ...] | None = None
    ) -> pd.DataFrame:
        with self._connect() as con:
            return con.execute(sql, params or []).fetchdf()

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.db_path))

    def _upsert(self, df: pd.DataFrame, table: str, key_columns: list[str]) -> None:
        if df.empty:
            return
        self.initialize()
        data = df.copy()
        with self._connect() as con:
            con.register("incoming", data)
            key_predicate = " AND ".join([f"{table}.{col} = incoming.{col}" for col in key_columns])
            con.execute(f"DELETE FROM {table} USING incoming WHERE {key_predicate}")
            columns = [row[1] for row in con.execute(f"PRAGMA table_info('{table}')").fetchall()]
            insert_columns = [col for col in columns if col in data.columns]
            col_sql = ", ".join(insert_columns)
            con.execute(f"INSERT INTO {table} ({col_sql}) SELECT {col_sql} FROM incoming")
