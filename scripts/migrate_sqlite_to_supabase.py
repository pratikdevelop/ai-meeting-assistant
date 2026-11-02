
import sys
from pathlib import Path

from sqlalchemy import (
    MetaData,
    Table,
    URL,
    create_engine,
    inspect,
    select,
)
from sqlalchemy.dialects.postgresql import insert as pg_insert


# Make the project root importable.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.db.database import engine as target_engine, init_db


SQLITE_PATH = ROOT / "app.db"

TABLES = [
    "meetings",
    "transcripts",
    "meeting_insights",
]


def main():
    if not SQLITE_PATH.exists():
        print(f"SQLite database not found: {SQLITE_PATH}")
        return

    # Create any missing tables in Supabase.
    init_db()

    source_engine = create_engine(
        URL.create(
            "sqlite",
            database=str(SQLITE_PATH),
        ),
        connect_args={
            "check_same_thread": False,
        },
    )

    source_inspector = inspect(source_engine)
    target_inspector = inspect(target_engine)

    total_copied = 0

    try:
        with (
            source_engine.connect() as source,
            target_engine.begin() as target,
        ):

            for table_name in TABLES:

                if not source_inspector.has_table(table_name):
                    print(f"SKIP: {table_name} not in SQLite")
                    continue

                if not target_inspector.has_table(table_name):
                    print(f"SKIP: {table_name} not in Supabase")
                    continue

                source_table = Table(
                    table_name,
                    MetaData(),
                    autoload_with=source_engine,
                )

                target_table = Table(
                    table_name,
                    MetaData(),
                    autoload_with=target_engine,
                )

                rows = source.execute(
                    select(source_table)
                ).mappings().all()

                if not rows:
                    print(f"EMPTY: {table_name}")
                    continue

                target_columns = set(target_table.c.keys())
                source_columns = set(source_table.c.keys())

                payload = [
                    {
                        column: row[column]
                        for column in target_columns & source_columns
                    }
                    for row in rows
                ]

                statement = (
                    pg_insert(target_table)
                    .values(payload)
                    .on_conflict_do_nothing()
                )

                target.execute(statement)

                total_copied += len(payload)

                print(
                    f"IMPORTED: {len(payload)} rows "
                    f"from {table_name}"
                )

        print()
        print("SQLite → Supabase migration finished.")
        print(f"Rows processed: {total_copied}")

    finally:
        source_engine.dispose()


if __name__ == "__main__":
    main()