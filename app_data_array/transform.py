import json
import numpy as np
import pandas as pd
import xarray as xr

N_DAYS = 90


def price_map(path) -> dict:
    """A map of the mtgjson card id to the price dictionary."""
    with open(path, "r") as f:
        payload_str = f.read()
        payload = json.loads(payload_str)

    return payload


def dict_to_xarray(payload, features: list[str]) -> "xarray.DataArray":
    """Convert the data component of an AllPrices.json dictionary to a xarray.DataArray.

    :returns: a 3D DataArray with the following indexes:
        - card ids
        - features (features)
        - timesteps (YYYY-MM-DD)

    """
    meta_data = payload["meta"]
    data = payload["data"]

    n_cards = len(data)
    ids = list(data.keys())

    date_range = pd.date_range(end=meta_data["date"], periods=N_DAYS, freq="D")
    date_index = pd.DatetimeIndex(date_range)

    price_matrices = []
    for feature in features:
        accessor_0, accessor_1, accessor_2, accessor_3 = feature.split("_")
        price_matrix = np.full(
            (N_DAYS, n_cards), fill_value=np.nan, dtype=np.float32
        )  # 90 timesteps
        for i, (card_id, price_map) in enumerate(data.items()):
            try:
                price_dict = price_map[accessor_0][accessor_1][accessor_2][accessor_3]
            except KeyError:
                continue

            series = pd.Series(price_dict, dtype=np.float32)
            series.index = pd.DatetimeIndex(series.index)
            series = series.reindex(date_index, method="nearest")

            # if len(series) == N_DAYS: # Todo maybe remove this condition if it's always met?
            price_matrix[:, i] = series

        price_matrices.append(price_matrix)

    all_data = np.array(price_matrices).swapaxes(
        0, 2
    )  # order the indexes: cards, timesteps, features
    return xr.DataArray(
        all_data,
        dims=("cards", "timesteps", "features"),
        coords={"cards": ids, "timesteps": list(date_index), "features": features},
    )


if __name__ == "__main__":
    data = price_map("../data/TestAllPrices.json")

    features = ["paper_cardmarket_retail_normal", "paper_tcgplayer_retail_normal"]
    data_array = dict_to_xarray(data, features=features)
