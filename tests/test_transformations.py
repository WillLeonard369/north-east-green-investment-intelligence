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