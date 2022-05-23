import json
import logging


def price_map(path) -> dict:
    """A map of the mtgjson card id to the price dictionary."""

    logging.critical("loading file %s", path)
    import os
    logging.critical("cwd: %s", os.getcwd())

    with open(path, "r") as f:
        payload_str = f.read()
        payload = json.loads(payload_str)

    return payload["data"]
