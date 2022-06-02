from app.main import PRICES, app
from fastapi.testclient import TestClient


PRICES_KEYS = list(PRICES.keys())

client = TestClient(app)


def test_get_first_list_of_mtgjson_ids():
    """Test getting a list of all of the mtgjson ids"""
    response = client.get(f"/ids")
    assert response.status_code == 200
    assert response.json() == PRICES_KEYS