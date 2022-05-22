import json

with open(r"AllPrices.json") as f:
    payload_str = f.read()
    payload = json.loads(payload_str)

    keys = list(payload["data"].keys())
    
    keys_to_remove = keys[100:]

    for key in keys_to_remove:
        del payload["data"][key]

    breakpoint()
    assert len(payload["data"]) == 100

    with open(r"outfile.json", "w") as outfile:
        json.dump(payload, outfile)