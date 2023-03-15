from yahooquery import Ticker

from whykay.helpers.logs import init_logger

logging = init_logger(name=__name__)

import json
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    confloat,
    root_validator,
    validator,
)

logging = init_logger(name=__name__)


class VerifyInformation(BaseModel):
    """Pydantic model to validate fetched stock/ETF data from Yahoo"""

    isin: Optional[str]
    ticker: str
    investment: confloat(gt=0)
    category: Optional[
        str
    ]  # this works in Python >= 10.x ; in older versions either use `Union[str, None]` or `Optional(str)`


symbol = "MOATo"
ticker = Ticker(symbol)

metadata = ticker.quote_type.get(symbol)
print(ticker.quote_type.get(symbol))
# if not isinstance(metadata, str):
#     logging.info(f"Ticker metadata available: {symbol}")
#     if metadata["quoteType"] == "ETF":
#         _tmp = {}
#         logging.info(f"{symbol} listed as an ETF, fetching holdings information")
