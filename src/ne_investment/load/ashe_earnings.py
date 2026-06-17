from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.ne_investment.transform.ashe_earnings import (
    transform_ashe_earnings,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def load_ashe_earnings() -> None:
    dataframe = transform_ashe_earnings()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT source_id
            FROM data_sources
            WHERE source_name = ?
              AND dataset_name = ?
            LIMIT 1
            """,
            (
                "Nomis ASHE",
                "Annual Survey of Hours and Earnings workplace analysis",
            ),
        )

        source = cursor.fetchone()

        if source:
            source_id = source[0]
        else:
            cursor.execute(
                """
                INSERT INTO data_sources (
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
                    "Nomis ASHE",
                    "Annual Survey of Hours and Earnings workplace analysis",
                    "Office for National Statistics via Nomis",
                    "Nomis ASHE workbook",
                    "Open Government Licence",
                    retrieved_at,
                ),
            )
            source_id = cursor.lastrowid

        regions = (
            dataframe[
                ["geography_code", "geography_name"]
            ]
            .drop_duplicates()
            .itertuples(index=False)
        )

        for region in regions:
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
                (
                    region.geography_code,
                    region.geography_name,
                    "ONS_REGION",
                    "E92000001",
                ),
            )

        geography_ids = {
            code: geography_id
            for geography_id, code in cursor.execute(
                """
                SELECT geography_id, geography_code
                FROM geography
                """
            ).fetchall()
        }

        rows = [
            (
                geography_ids[row.geography_code],
                row.indicator_code,
                row.period,
                row.frequency,
                row.value,
                row.confidence_pct,
                row.unit,
                source_id,
                retrieved_at,
            )
            for row in dataframe.itertuples(index=False)
        ]

        cursor.executemany(
            """
            INSERT OR REPLACE INTO regional_earnings (
                geography_id,
                indicator_code,
                period,
                frequency,
                value,
                confidence_pct,
                unit,
                source_id,
                retrieved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        connection.commit()

    print(
        f"Loaded {len(dataframe)} ASHE earnings observations "
        f"for {dataframe['geography_code'].nunique()} regions."
    )


if __name__ == "__main__":
    load_ashe_earnings()