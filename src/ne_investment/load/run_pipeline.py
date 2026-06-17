from src.ne_investment.load.create_database import create_database
from src.ne_investment.load.ons_gva import load_regional_gva
from src.ne_investment.load.regional_gva_levels import (
    load_regional_gva_levels,
)
from src.ne_investment.load.subregional_manufacturing import (
    load_subregional_manufacturing,
)
from src.ne_investment.load.regional_labour_market_snapshot import (
    load_regional_labour_market_snapshot,
)

from src.ne_investment.load.historical_labour_market import (
    load_historical_labour_market,
)


def run_pipeline() -> None:
    create_database()
    load_regional_gva()
    load_regional_gva_levels()
    load_regional_labour_market_snapshot()
    load_historical_labour_market()
    load_subregional_manufacturing()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()