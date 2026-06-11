from pathlib import Path

from carmenv.config.schema import AppConfig


def default_config(project_root: Path | None = None) -> AppConfig:
    root = project_root or Path.cwd()
    return AppConfig(
        project_root=root,
        data_dir=root / "data",
        db_path=root / "data" / "carmenv.duckdb",
        reports_dir=root / "reports_output",
    )
