from src.ne_investment.load.create_database import create_database
from src.ne_investment.load.ons_gva import load_regional_gva
from src.ne_investment.load.subregional_manufacturing import (
    load_subregional_manufacturing,
)


def run_pipeline() -> None:
    create_database()
    load_regional_gva()
    load_subregional_manufacturing()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()