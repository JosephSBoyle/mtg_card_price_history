import json


def price_map(path) -> dict:
    """A map of the mtgjson card id to the price dictionary."""
    with open(path, "r") as f:
        payload_str = f.read()
        payload = json.loads(payload_str)

    return payload["data"]
