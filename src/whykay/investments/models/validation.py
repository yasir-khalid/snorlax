from typing import List, Dict
from whykay.investments.models.data_models import Portfolio
from whykay.helpers.logs import init_logger

logging = init_logger(name=__name__)

def input_validator(data: list[Dict]) -> Portfolio:
    """compares the input data against the defined pydantic model for input"""
    try:
        _validated_output = [Portfolio(**x) for x in data]
        logging.info("Data validation successful")
        return _validated_output
    except:
        logging.error("Input data validation (via pydantic models) failed")
