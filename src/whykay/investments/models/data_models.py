from typing import Dict

from pydantic import BaseModel


class Investment(BaseModel):
    """Pydantic model to validate input stock/ETF data"""

    investments: Dict[str, int]
