<<<<<<< HEAD
import json
from typing import Dict, List, Optional

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    confloat,
    root_validator,
    validator,
)
from rich import print

from whykay.helpers.logs import init_logger

logging = init_logger(name=__name__)
=======
from typing import Dict, List

from pydantic import BaseModel, ValidationError, validator, root_validator, Field, confloat
import json
from typing import Optional
from whykay.helpers.logs import init_logger
>>>>>>> a49278411eaa38fce3d57fb54577e9b3d996108e

from rich import print
logging = init_logger(name=__name__)

class Portfolio(BaseModel):
    """Pydantic model to validate input stock/ETF data"""
    isin: str
    investment: confloat(gt = 0)
    category: Optional[str] # this works in Python >= 10.x ; in older versions either use `Union[str, None]` or `Optional(str)`

<<<<<<< HEAD
    isin: Optional[str]
    ticker: str
    investment: confloat(gt=0)
    category: Optional[
        str
    ]  # this works in Python >= 10.x ; in older versions either use `Union[str, None]` or `Optional(str)`


class WeightedInvestmentsModel(BaseModel):
    """"Child model for Pydantic `WeightedInvestments` model to validate pandas dataframes"""


class WeightedInvestments(BaseModel):
    """Pydantic model to validate the weighted holdings from the investment porfolio supplied"""

    dataframe: List[WeightedInvestmentsModel]

=======
class WeightedInvestmentsModel(BaseModel):
    """"Child model for Pydantic `WeightedInvestments` model to validate pandas dataframes"""

class WeightedInvestments(BaseModel):
    """Pydantic model to validate the weighted holdings from the investment porfolio supplied"""
    dataframe: List[WeightedInvestmentsModel]    
>>>>>>> a49278411eaa38fce3d57fb54577e9b3d996108e

def main():
    logging.warn("Running the model validator on sample data, not real data")
    try:
<<<<<<< HEAD
        logging.info(
            "Reading sample dataset from: datasets/stock_portfolio_modelling.json ..."
        )
        with open("datasets/stock_portfolio_modelling.json") as holdings_dummy_data:
            sample_data = json.loads(holdings_dummy_data.read())
        logging.info("Sample dataset read successful")
    except FileNotFoundError:
        logging.error("Sample data file not found. Check path")
        raise SystemExit

=======
        logging.info("Reading sample dataset from: datasets/stock_portfolio_modelling.json ...")
        with open('datasets/stock_portfolio_modelling.json') as holdings_dummy_data:
            sample_data = json.loads(
                            holdings_dummy_data.read()
                        )
        logging.info("Sample dataset read successful")
    except FileNotFoundError:
        logging.error("Sample data file not found. Check path")
        raise SystemExit    
>>>>>>> a49278411eaa38fce3d57fb54577e9b3d996108e
    output = [Portfolio(**x) for x in sample_data]
    print(output)


if __name__ == "__main__":
    main()
