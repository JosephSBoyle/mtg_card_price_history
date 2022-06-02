import logging

from fastapi import FastAPI
import app.data_loader.price_loader as price_loader
from app.models import Format, PriceQuote, Printing, QuoteType, Vendor

logging.basicConfig(level=logging.DEBUG)


app = FastAPI(docs_url="/")

PRICE_FILE = "./data/TestAllPrices.json"
PRICES = price_loader.price_map(PRICE_FILE)
PRICE_IDS = list(PRICES.keys())
FORMATS = [format_.value for format_ in Format]
VENDORS = [vendor.value for vendor in Vendor]
QUOTE_TYPES = [quote_type.value for quote_type in QuoteType]
PRINTINGS = [printing.value for printing in Printing]


@app.get(
    "/prices/{mtgjson_id}/{format}/{vendor}/{quote_type}/{printing}",
    response_model=PriceQuote,
)
async def card_prices(
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


@app.get("/ids/")
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


@app.get("/formats/")
async def formats():
    """
    A list of each of the valid formats

    ### Example usage:
    ```bash
    $ curl <base_url>/formats
    >>> ['paper', 'mtgo']
    ```
    """
    return FORMATS


@app.get("/vendors/")
async def vendors():
    """
    A list of all card vendors

    ### Example usage:
    ```bash
    $ curl <base_url>/formats
    >>> ['tcgplayer', 'cardmarket', ...]
    ```
    """
    return FORMATS


@app.get("/quote_types/")
async def quote_types():
    """
    A list of of the valid formats

    ### Example usage:
    ```bash
    $ curl <base_url>/formats
    >>> ['retail', 'buylist']
    ```
    """
    return QUOTE_TYPES


@app.get("/printings/")
async def printings():
    """
    A list of printing types

    ### Example usage:
    ```bash
    $ curl <base_url>/formats
    >>> ['normal', 'foil']
    ```
    """
    return PRINTINGS
