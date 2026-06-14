from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"
SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"
VIEWS_PATH = PROJECT_ROOT / "database" / "views.sql"


def create_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        views = VIEWS_PATH.read_text(encoding="utf-8")

        connection.executescript(schema)
        connection.executescript(views)

    print(f"Database created at: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()