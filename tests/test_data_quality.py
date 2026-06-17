from src.ne_investment.analysis.gva_analysis import analyse_gva

from src.ne_investment.analysis.bres_employment_growth import (
    calculate_bres_employment_growth,
)

from src.ne_investment.analysis.ashe_earnings_gap import (
    calculate_ashe_earnings_gap,
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