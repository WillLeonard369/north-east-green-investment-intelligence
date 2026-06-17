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

from src.ne_investment.load.bres_employment import (
    load_bres_employment,
)

from src.ne_investment.load.ashe_earnings import (
    load_ashe_earnings,
)

from src.ne_investment.load.green_projects import (
    load_green_projects,
)


def run_pipeline() -> None:
    create_database()
    load_regional_gva()
    load_regional_gva_levels()
    load_regional_labour_market_snapshot()
    load_historical_labour_market()
    load_bres_employment()
    load_ashe_earnings()
    load_green_projects()
    load_subregional_manufacturing()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()


