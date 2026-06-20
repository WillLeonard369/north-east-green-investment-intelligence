import pandas as pd


from src.ne_investment.analysis.gva_analysis import analyse_gva

from src.ne_investment.analysis.bres_employment_growth import (
    calculate_bres_employment_growth,
)

from src.ne_investment.analysis.ashe_earnings_gap import (
    calculate_ashe_earnings_gap,
)

from src.ne_investment.analysis.green_projects_summary import (
    calculate_green_projects_summary,
)

from src.ne_investment.analysis.green_projects_sector_summary import (
    calculate_green_projects_sector_summary,
)


def test_gva_analysis_output():
    dataframe = analyse_gva()

    assert not dataframe.empty
    assert dataframe["period"].is_monotonic_increasing
    assert dataframe["value"].notna().all()
    assert dataframe["annual_growth_pct"].iloc[1:].notna().all()


def test_ashe_earnings_gap_output():
    dataframe = calculate_ashe_earnings_gap()

    assert not dataframe.empty
    assert {
        "indicator_code",
        "period",
        "North East",
        "North West",
        "absolute_gap",
        "north_east_gap_pct",
    }.issubset(dataframe.columns)

    assert dataframe["North East"].notna().all()
    assert dataframe["North West"].notna().all()
    assert dataframe["absolute_gap"].notna().all()
    assert dataframe["north_east_gap_pct"].notna().all()

    assert set(dataframe["indicator_code"].unique()) == {
        "MEDIAN_WEEKLY_GROSS_PAY",
        "MEDIAN_HOURLY_PAY_EXCL_OVERTIME",
    }



def test_bres_employment_growth_output():
    dataframe = calculate_bres_employment_growth()

    assert not dataframe.empty
    assert {
        "geography_name",
        "industry_code",
        "industry_name",
        "2015",
        "2024",
        "absolute_change",
        "growth_pct",
    }.issubset(dataframe.columns)

    assert dataframe["2015"].notna().all()
    assert dataframe["2024"].notna().all()
    assert dataframe["growth_pct"].notna().all()

    assert set(dataframe["geography_name"].unique()) == {
        "North East",
        "North West",
    }

    assert dataframe["industry_code"].nunique() == 17
    assert len(dataframe) == 34


def test_green_projects_summary_output():
    dataframe = calculate_green_projects_summary()

    assert not dataframe.empty
    assert set(dataframe["metric"]) == {
        "projects",
        "committed_regional_capital_investment_gbp",
        "estimated_regional_capital_investment_gbp",
        "potential_regional_capital_investment_gbp",
        "regional_economic_impact_gbp",
        "construction_jobs",
        "operational_jobs",
        "jobs_supported",
        "regional_jobs_announced",
    }

    metrics = dataframe.set_index("metric")["value"]

    assert metrics["projects"] == 14
    assert (
        metrics["committed_regional_capital_investment_gbp"]
        == 2_365_600_000
    )
    assert pd.isna(
        metrics["estimated_regional_capital_investment_gbp"]
    )
    assert (
        metrics["potential_regional_capital_investment_gbp"]
        == 2_000_000_000
    )
    assert metrics["regional_economic_impact_gbp"] == 262_200_000
    assert metrics["construction_jobs"] == 3_950
    assert metrics["operational_jobs"] == 2_334
    assert metrics["jobs_supported"] == 13_000
    assert metrics["regional_jobs_announced"] == 19_284


def test_green_projects_sector_summary_output():
    dataframe = calculate_green_projects_sector_summary()

    assert not dataframe.empty

    expected_columns = {
        "sector",
        "technology_theme",
        "projects",
        "committed_regional_capital_gbp",
        "potential_regional_capital_gbp",
        "regional_economic_impact_gbp",
        "construction_jobs",
        "operational_jobs",
        "jobs_supported",
        "regional_jobs_announced",
        "low_risk_projects",
        "medium_risk_projects",
        "high_risk_projects",
    }

    assert expected_columns.issubset(dataframe.columns)
    assert dataframe["projects"].sum() == 14
    assert dataframe["low_risk_projects"].sum() == 9
    assert dataframe["medium_risk_projects"].sum() == 4
    assert dataframe["high_risk_projects"].sum() == 1
    