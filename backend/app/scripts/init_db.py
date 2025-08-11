from pathlib import Path
from ..db import get_db_conn

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


def run_migration(sql_path: Path) -> None:
    print(f"Applying migration: {sql_path.name}")
    with sql_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def main():
    files = sorted(p for p in MIGRATIONS_DIR.glob("*.sql"))
    for p in files:
        run_migration(p)
    print("Migrations applied.")


if __name__ == "__main__":
    main()