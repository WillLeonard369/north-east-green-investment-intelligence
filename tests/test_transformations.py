from src.ne_investment.transform.ons_gva import transform_north_east_gva


def test_north_east_gva_transformation():
    dataframe = transform_north_east_gva()

    assert not dataframe.empty
    assert dataframe["geography_code"].eq("TLC").all()
    assert dataframe["indicator_code"].eq("REAL_GVA_INDEX").all()
    assert dataframe["value"].notna().all()
    assert dataframe["period"].min() == "1998"
    assert dataframe["period"].max() == "2023"