def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_status_endpoint(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert "service" in response.json()


def test_login_endpoint_exists(client):
    response = client.post("/login", json={
        "email": "fake@test.com",
        "password": "fakepassword"
    })
    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data or "detail" in response_data


def test_docs_endpoint(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_invalid_endpoint_returns_404(client):
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404