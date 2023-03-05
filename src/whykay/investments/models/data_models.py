from typing import Dict

from pydantic import BaseModel, ValidationError, validator, root_validator, Field, confloat
import json
from typing import Optional
from whykay.helpers.logs import init_logger

from rich import print
logging = init_logger(name=__name__)

class Portfolio(BaseModel):
    """Pydantic model to validate input stock/ETF data"""
    isin: str
    investment: confloat(gt = 0)
    category: Optional[str] # this works in Python >= 10.x ; in older versions either use `Union[str, None]` or `Optional(str)`

def main():
    logging.warn("Running the model validator on sample data, not real data")
    try:
        logging.info("Reading sample dataset from: datasets/stock_portfolio_modelling.json ...")
        with open('datasets/stock_portfolio_modelling.json') as holdings_dummy_data:
            sample_data = json.loads(
                            holdings_dummy_data.read()
                        )
        logging.info("Sample dataset read successful")
    except:
        logging.error("Sample data read unsuccessful. Check path")
    
    output = [Portfolio(**x) for x in sample_data]
    print(output)


if __name__ == "__main__":
    main()
