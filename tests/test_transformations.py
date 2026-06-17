from src.ne_investment.transform.ons_gva import transform_north_east_gva
from src.ne_investment.transform.subregional_manufacturing import (
    transform_subregional_manufacturing,
)
from src.ne_investment.transform.regional_gva_levels import (
    transform_regional_gva_levels,
)
from src.ne_investment.transform.regional_labour_market_snapshot import (
    transform_regional_labour_market_snapshot,
)
from src.ne_investment.transform.historical_labour_market import (
    transform_historical_labour_market,
)

from src.ne_investment.transform.bres_employment import (
    transform_bres_employment,
)

from src.ne_investment.transform.ashe_earnings import (
    transform_ashe_earnings,
)

from src.ne_investment.transform.green_projects import (
    transform_green_projects,
)

def test_north_east_gva_transformation():
    dataframe = transform_north_east_gva()

    assert not dataframe.empty
    assert dataframe["geography_code"].eq("TLC").all()
    assert dataframe["indicator_code"].eq("REAL_GVA_INDEX").all()
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "1998"
    assert dataframe["period"].max() == "2023"


def test_subregional_manufacturing_transformation():
    dataframe = transform_subregional_manufacturing()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {"TLC3", "TLC4"}
    assert dataframe["indicator_code"].eq("MANUFACTURING_GVA_INDEX").all()
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "1998"
    assert dataframe["period"].max() == "2023"
    assert len(dataframe) == 52


def test_regional_gva_levels_transformation():
    dataframe = transform_regional_gva_levels()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {"TLC", "TLD"}
    assert dataframe["indicator_code"].eq("REAL_GVA_GBP_MILLION").all()
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "1998"
    assert dataframe["period"].max() == "2023"
    assert len(dataframe) == 52


def test_regional_labour_market_snapshot_transformation():
    dataframe = transform_regional_labour_market_snapshot()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {
        "E12000001",
        "E12000002",
    }
    assert set(dataframe["indicator_code"].unique()) == {
        "ECONOMIC_ACTIVITY_RATE",
        "EMPLOYMENT_RATE",
        "UNEMPLOYMENT_RATE",
        "ECONOMIC_INACTIVITY_RATE",
    }
    assert dataframe["value"].notna().all()
    assert dataframe["period"].eq("2026-Q1").all()
    assert len(dataframe) == 8


def test_historical_labour_market_transformation():
    dataframe = transform_historical_labour_market()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {
        "E12000001",
        "E12000002",
    }
    assert set(dataframe["indicator_code"].unique()) == {
        "ECONOMIC_ACTIVITY_RATE",
        "EMPLOYMENT_RATE",
        "UNEMPLOYMENT_RATE",
        "ECONOMIC_INACTIVITY_RATE",
    }
    assert dataframe["value"].notna().all()
    assert dataframe["frequency"].eq("rolling_3_month").all()
    assert dataframe["period"].str.match(
        r"^[A-Z][a-z]{2} \d{4}-[A-Z][a-z]{2} \d{4}$"
    ).all()


def test_bres_employment_transformation():
    dataframe = transform_bres_employment()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {
        "E12000001",
        "E12000002",
    }
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "2015"
    assert dataframe["period"].max() == "2024"
    assert dataframe["frequency"].eq("annual").all()
    assert dataframe["unit"].eq("employment_count").all()
    assert dataframe["industry_code"].nunique() == 17
    assert len(dataframe) == 340


def test_ashe_earnings_transformation():
    dataframe = transform_ashe_earnings()

    assert not dataframe.empty
    assert set(dataframe["geography_code"].unique()) == {
        "E12000001",
        "E12000002",
    }
    assert set(dataframe["indicator_code"].unique()) == {
        "MEDIAN_WEEKLY_GROSS_PAY",
        "MEDIAN_HOURLY_PAY_EXCL_OVERTIME",
    }
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "1997"
    assert dataframe["frequency"].eq("annual").all()
    assert set(dataframe["unit"].unique()) == {
        "gbp_per_week",
        "gbp_per_hour",
    }


def test_green_projects_transformation():
    dataframe = transform_green_projects()

    expected_columns = {
        "project_name",
        "project_type",
        "sector",
        "technology_theme",
        "geography_code",
        "location_name",
        "developer_name",
        "investor_name",
        "announcement_date",
        "expected_completion_date",
        "project_status",
        "regional_linkage_type",
        "regional_linkage_strength",
        "total_project_value_gbp",
        "regional_value_gbp",
        "total_jobs_announced",
        "regional_jobs_announced",
        "capacity_value",
        "capacity_unit",
        "source_name",
        "source_url",
        "retrieved_at",
        "notes",
    }

    assert expected_columns.issubset(dataframe.columns)