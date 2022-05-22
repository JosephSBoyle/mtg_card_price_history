#### Get a card based on it's MTGJSON ID:

##### Request
>>> {"type": "priceHistory", "cardId": <MtgJsonID>}
##### Response
>>> {"date": price1, "date": price2 ...}

##### Performance requirements
100 requests per second.