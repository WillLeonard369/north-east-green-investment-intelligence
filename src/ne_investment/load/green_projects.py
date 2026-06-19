from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from src.ne_investment.transform.green_projects import (
    transform_green_projects,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "processed" / "ne_investment.db"


def load_green_projects() -> None:
    dataframe = transform_green_projects()
    retrieved_at = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        geography_ids = {
            code: geography_id
            for geography_id, code in cursor.execute(
                """
                SELECT geography_id, geography_code
                FROM geography
                """
            ).fetchall()
        }

        loaded_rows = 0

        for row in dataframe.itertuples(index=False):
            cursor.execute(
                """
                SELECT source_id
                FROM data_sources
                WHERE source_name = ?
                LIMIT 1
                """,
                (row.source_name,),
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
                        row.source_name,
                        "Green investment project source",
                        row.source_name,
                        row.source_url,
                        None,
                        row.retrieved_at or retrieved_at,
                    ),
                )
                source_id = cursor.lastrowid

            geography_id = geography_ids.get(row.geography_code)

            cursor.execute(
                """
                INSERT OR REPLACE INTO green_investment_projects (
                    project_name,
                    project_type,
                    sector,
                    technology_theme,
                    geography_id,
                    location_name,
                    developer_name,
                    investor_name,
                    announcement_date,
                    expected_completion_date,
                    project_status,
                    regional_linkage_type,
                    regional_linkage_strength,
                    capital_investment_gbp,
                    regional_capital_investment_gbp,
                    capital_value_status,
                    regional_economic_impact_gbp,
                    construction_jobs,
                    operational_jobs,
                    jobs_supported,
                    regional_jobs_announced,
                    capacity_value,
                    capacity_unit,
                    source_id,
                    source_url,
                    retrieved_at,
                    notes
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    row.project_name,
                    row.project_type,
                    row.sector,
                    row.technology_theme,
                    geography_id,
                    row.location_name,
                    row.developer_name,
                    row.investor_name,
                    row.announcement_date,
                    row.expected_completion_date,
                    row.project_status,
                    row.regional_linkage_type,
                    row.regional_linkage_strength,
                    row.capital_investment_gbp,
                    row.regional_capital_investment_gbp,
                    row.capital_value_status,
                    row.regional_economic_impact_gbp,
                    row.construction_jobs,
                    row.operational_jobs,
                    row.jobs_supported,
                    row.regional_jobs_announced,
                    row.capacity_value,
                    row.capacity_unit,
                    source_id,
                    row.source_url,
                    row.retrieved_at or retrieved_at,
                    row.notes,
                ),
            )

            loaded_rows += 1

        connection.commit()

    print(f"Loaded {loaded_rows} green-investment projects.")


if __name__ == "__main__":
    load_green_projects()
