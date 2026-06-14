from src.ne_investment.transform.ons_gva import transform_north_east_gva
from src.ne_investment.transform.subregional_manufacturing import (
    transform_subregional_manufacturing,
)
from src.ne_investment.transform.regional_gva_levels import (
    transform_regional_gva_levels,
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