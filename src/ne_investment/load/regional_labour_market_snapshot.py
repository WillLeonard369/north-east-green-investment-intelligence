from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.ne_investment.transform.regional_labour_market_snapshot import (
    transform_regional_labour_market_snapshot,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def load_regional_labour_market_snapshot() -> None:
    dataframe = transform_regional_labour_market_snapshot()
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
                "ONS Regional Labour Market",
                "S01 Regional labour market summary",
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
                    "ONS Regional Labour Market",
                    "S01 Regional labour market summary",
                    "Office for National Statistics",
                    "ONS S01 regional labour market workbook",
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

    print(
        f"Loaded {len(dataframe)} labour-market observations "
        f"for {dataframe['geography_code'].nunique()} regions."
    )


if __name__ == "__main__":
    load_regional_labour_market_snapshot()