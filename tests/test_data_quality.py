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

def test_gva_analysis_output():
    dataframe = analyse_gva()

    assert not dataframe.empty
    assert dataframe["period"].is_monotonic_increasing
    assert dataframe["value"].notna().all()
    assert dataframe["annual_growth_pct"].iloc[1:].notna().all()


def test_bres_employment_growth_output():
    dataframe = calculate_bres_employment_growth()

    assert not dataframe.empty
    assert {"2015", "2024", "absolute_change", "growth_pct"}.issubset(
        dataframe.columns
    )
    assert dataframe["2015"].notna().all()
    assert dataframe["2024"].notna().all()
    assert dataframe["growth_pct"].notna().all()
    assert set(dataframe["geography_name"].unique()) == {
        "North East",
        "North West",
    }
    assert len(dataframe) == 34

def test_ashe_earnings_gap_output():
    dataframe = calculate_ashe_earnings_gap()

    assert not dataframe.empty
    assert {
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


def test_green_projects_summary_output():
    dataframe = calculate_green_projects_summary()

    assert not dataframe.empty
    assert set(dataframe["metric"]) == {
        "projects",
        "verified_regional_capital_investment_gbp",
        "regional_economic_impact_gbp",
        "construction_jobs",
        "operational_jobs",
        "jobs_supported",
        "regional_jobs_announced",
    }

    metrics = dataframe.set_index("metric")["value"]

    assert metrics["projects"] == 4
    assert (
        metrics["verified_regional_capital_investment_gbp"]
        == 2_030_000_000
    )
    assert metrics["construction_jobs"] == 3_000
    assert metrics["operational_jobs"] == 1_921
    assert metrics["jobs_supported"] == 1_000
    assert metrics["regional_jobs_announced"] == 5_921
