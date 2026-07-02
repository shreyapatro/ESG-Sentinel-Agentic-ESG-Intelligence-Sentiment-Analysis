from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["service"] == "ESG Sentinel API"
    assert data["status"] == "running"
    assert data["docs"] == "/docs"


def test_companies_endpoint_returns_infosys():
    response = client.get("/companies")

    assert response.status_code == 200
    data = response.json()

    companies = data["companies"]
    tickers = [company["ticker"] for company in companies]

    assert "INFY" in tickers