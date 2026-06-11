from pathlib import Path

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    data_dir: Path = Path("data")
    db_path: Path = Path("data/carmenv.duckdb")
    reports_dir: Path = Path("reports_output")
    min_amount_ma20: float = 1_000_000
    top_n: int = 10
