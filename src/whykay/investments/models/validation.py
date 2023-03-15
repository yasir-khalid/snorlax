<<<<<<< HEAD
from typing import Dict, List

from whykay.helpers.logs import init_logger
from whykay.investments.models.data_models import Portfolio

logging = init_logger(name=__name__)


=======
from typing import List, Dict
from whykay.investments.models.data_models import Portfolio
from whykay.helpers.logs import init_logger

logging = init_logger(name=__name__)

>>>>>>> a49278411eaa38fce3d57fb54577e9b3d996108e
def input_validator(data: list[Dict]) -> Portfolio:
    """compares the input data against the defined pydantic model for input"""
    try:
        _validated_output = [Portfolio(**x) for x in data]
        logging.info("Data validation successful")
        return _validated_output
    except:
        logging.error("Input data validation (via pydantic models) failed")
