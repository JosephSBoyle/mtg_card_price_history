import json


def price_map(filename=r"AllPrices.json") -> dict:
    """A map of the mtgjson card id to the price dictionary."""
    with open(filename, "r") as f:
        payload_str = f.read()
        payload = json.loads(payload_str)
    
    return payload["data"]
