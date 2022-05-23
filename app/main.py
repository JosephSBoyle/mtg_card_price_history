import logging

from fastapi import FastAPI

import app.data_loader.price_loader as price_loader
from app.models import (Format, PriceQuote, Printing, QuoteType, UUIDList,
                        Vendor)

logging.basicConfig(level=logging.DEBUG)
logging.info("Just testing")


app = FastAPI(redoc_url="/documentation", docs_url=None)

PRICE_FILE = "./data/TestAllPrices.json"
PRICES = price_loader.price_map(PRICE_FILE)
PRICE_IDS = list(PRICES.keys())

@app.get(
    "/prices/{mtgjson_id}/{format}/{vendor}/{quote_type}/{printing}",
    response_model=PriceQuote,
)
async def card_ids(
    mtgjson_id: str,
    format: Format,
    vendor: Vendor,
    quote_type: QuoteType,
    printing: Printing,
):
    """
    ## A specific price quote series for a given card.

    * Not all vendors quote prices for all formats
    * Not all vendors quote buylist prices

    ### Example usage:
    ```bash
    $ curl <base_url>/prices/076636d3-9d74-50c0-83fa-5988d64c9f98/paper/cardmarket/retail/foil
    >>> {"2022-02-21":0.14,"2022-02-22":0.17, ...,"2022-05-21":0.25}
    ```

    * `mtgjson_id`: the mtg json id of the card
    * `format`: the format of the card 'paper' | 'mtgo'
    * `vendor`: the vendor e.g 'cardmarket'
    * `quote_type`: the type of quote that the prices refer to e.g 'retail' | 'buylist'
    * `printing`: the type of printing that this card is e.g 'foil' | 'normal'
    """
    card_prices = PRICES.get(mtgjson_id, {})
    format_prices = card_prices.get(format, {})
    vendor_prices = format_prices.get(vendor, {})
    retail_prices = vendor_prices.get(quote_type, {})
    return retail_prices.get(printing, {})


@app.get(
    "/ids/",
    response_model=UUIDList,
)
async def card_ids():
    """
    All of the card ids in a flat list.
    
    ### Example usage:
    ```bash
    $ curl <base_url>/ids
    >>> ['00010d56-fe38-5e35-8aed-518019aa36a5', '0001e0d0-2dcd-5640-aadc-a84765cf5fc9', ..., '0003caab-9ff5-5d1a-bc06-976dd0457f19']
    ```
    """
    return PRICE_IDS
