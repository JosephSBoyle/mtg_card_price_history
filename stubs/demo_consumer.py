"""An example consumer application"""
import asyncio
import time

import aiohttp
import requests

BASE_URL = "https://mtg-card-price-history.herokuapp.com/"


def get_cardmarket_retail_non_foil_urls():
    ids = requests.get(BASE_URL + "ids").json()
    return [f"{BASE_URL}prices/{id_}/paper/cardmarket/retail/normal" for id_ in ids]


async def get_price_history(session, url):
    async with session.get(url) as resp:
        price_map = await resp.json()
        return price_map


async def get_price_dicts() -> dict[str, list[float]]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in get_cardmarket_retail_non_foil_urls():
            tasks.append(asyncio.ensure_future(get_price_history(session, url)))

        results = await asyncio.gather(*tasks)
        return results


start_time = time.time()
price_dicts = asyncio.run(get_price_dicts())
execution_time = (time.time() - start_time)
print("--- %s seconds ---" % execution_time)
