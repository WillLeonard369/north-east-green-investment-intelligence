from src.ne_investment.analysis.gva_analysis import analyse_gva


def test_gva_analysis_output():
    dataframe = analyse_gva()

    assert not dataframe.empty
    assert dataframe["period"].is_monotonic_increasing
    assert dataframe["value"].notna().all()
    assert dataframe["annual_growth_pct"].iloc[1:].notna().all()