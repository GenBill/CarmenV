from pathlib import Path


def project_root() -> Path:
    return Path.cwd()


def default_db_path() -> Path:
    return project_root() / "data" / "carmenv.duckdb"


def schema_path() -> Path:
    return Path(__file__).with_name("schema.sql")
