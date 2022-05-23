import random
import time

from app.models.enums import Format, Printing, QuoteType, Vendor
from app.main import PRICES, app
from app.models.models import PriceQuote
from fastapi.testclient import TestClient

PRICES_KEYS = list(PRICES.keys())

client = TestClient(app)


def test_query_card_price():
    """Test requesting the price of a single mtg card by mtgjson id."""
    mtgjson_id = "076636d3-9d74-50c0-83fa-5988d64c9f98"

    response = client.get(
        f"/prices/{mtgjson_id}/{Format.paper}/{Vendor.cardmarket}/{QuoteType.retail}/{Printing.foil}"
    )
    parsed_price_quote = PriceQuote.parse_obj(response.json())

    assert response.status_code == 200
    assert parsed_price_quote

def test_query_parameter_combinations():
    """Test querying various combinations of the query parameters."""
    requests = min(len(PRICES_KEYS), 1000)
    keys = random.sample(PRICES_KEYS, requests)

    for mtgjson_id in keys:
        format = random.choice(list(Format))
        vendor = random.choice(list(Vendor))
        quote_type = random.choice(list(QuoteType))
        printing = random.choice(list(Printing))
        response = client.get(
            f"/prices/{mtgjson_id}/{format}/{vendor}/{quote_type}/{printing}"
        )
        assert response.status_code == 200


def test_performance():
    """A crude performance test."""
    requests = min(len(PRICES_KEYS), 1000)
    min_requests_per_second = 100

    t0 = time.time()
    keys = random.sample(PRICES_KEYS, requests)

    urls = [
        f"/prices/{mtgjson_id}/{Format.paper}/{Vendor.cardmarket}/{QuoteType.retail}/{Printing.normal}"
        for mtgjson_id in keys
    ]

    for url in urls:
        client.get(url)

    t1 = time.time()

    elapsed_time = t1 - t0
    requests_per_second = requests / elapsed_time
    assert requests_per_second > min_requests_per_second
