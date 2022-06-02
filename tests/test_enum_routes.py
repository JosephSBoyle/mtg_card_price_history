from app.main import PRICES, FORMATS, PRINTINGS, VENDORS, QUOTE_TYPES, app
from fastapi.testclient import TestClient


PRICES_KEYS = list(PRICES.keys())

client = TestClient(app)


def test_get_ids():
    """Test getting a list of all of the mtgjson ids"""
    response = client.get(f"/ids")
    assert response.status_code == 200
    assert response.json() == PRICES_KEYS

def test_get_formats():
    """Test getting a list of the formats"""
    response = client.get(f"/formats")
    assert response.status_code == 200
    assert response.json() == FORMATS
    
def test_get_vendors():
    """Test getting a list of the vendors"""
    response = client.get(f"/vendors")
    assert response.status_code == 200
    assert response.json() == VENDORS

def test_get_quote_types():
    """Test getting a list of the quotes types"""
    response = client.get(f"/quote_types")
    assert response.status_code == 200
    assert response.json() == QUOTE_TYPES


def test_get_printings():
    """Test getting a list of the printing types"""
    response = client.get(f"/printings")
    assert response.status_code == 200
    assert response.json() == PRINTINGS