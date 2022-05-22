from pydantic import BaseModel, condecimal
from datetime import date


class PriceQuote(BaseModel):
    """A date -> price quote mapping.
    
    ### Example
    ```bash
    >>> {"2022-02-21": 0.14, "2022-02-22": 0.17, "2022-03-23": 0.25}
    ```
    """
    __root__: dict[date, condecimal(gt=0, decimal_places=2)]
