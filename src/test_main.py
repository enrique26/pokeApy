from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)

def test_all_berry_stats():
    response = cliente.get("/allBerryStats")
    print(response.headers["Content-Type"])
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    data = response.json()
    assert "berries_names" in data
    assert "min_growth_time" in data
    assert "median_growth_time" in data
    assert "max_growth_time" in data
    assert "variance_growth_time" in data
    assert "mean_growth_time" in data
    assert "frequency_growth_time" in data