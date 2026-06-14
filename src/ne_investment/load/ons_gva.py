from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.ne_investment.transform.ons_gva import transform_north_east_gva


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def load_north_east_gva() -> None:
    dataframe = transform_north_east_gva()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO data_sources (
                source_name,
                dataset_name,
                publisher,
                source_url,
                licence,
                accessed_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "ONS Regional GVA",
                "Regional gross value added balanced by industry",
                "Office for National Statistics",
                "ONS regional GVA workbook",
                "Open Government Licence",
                retrieved_at,
            ),
        )

        cursor.execute(
            """
            SELECT source_id
            FROM data_sources
            WHERE source_name = ?
              AND dataset_name = ?
            ORDER BY source_id DESC
            LIMIT 1
            """,
            (
                "ONS Regional GVA",
                "Regional gross value added balanced by industry",
            ),
        )
        source_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT OR IGNORE INTO geography (
                geography_code,
                geography_name,
                geography_type,
                parent_code
            )
            VALUES (?, ?, ?, ?)
            """,
            ("TLC", "North East", "ITL1", "UK"),
        )

        cursor.execute(
            """
            SELECT geography_id
            FROM geography
            WHERE geography_code = ?
            """,
            ("TLC",),
        )
        geography_id = cursor.fetchone()[0]

        rows = [
            (
                geography_id,
                row.indicator_code,
                row.period,
                row.frequency,
                row.value,
                row.unit,
                source_id,
                retrieved_at,
            )
            for row in dataframe.itertuples(index=False)
        ]

        cursor.executemany(
            """
            INSERT OR REPLACE INTO economic_observations (
                geography_id,
                indicator_code,
                period,
                frequency,
                value,
                unit,
                source_id,
                retrieved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        connection.commit()

    print(f"Loaded {len(dataframe)} GVA observations into the database.")


if __name__ == "__main__":
    load_north_east_gva()
    