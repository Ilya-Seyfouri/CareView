def test_health_endpoint(client):
    """Test health check works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_status_endpoint(client):
    """Test status endpoint works"""
    response = client.get("/status")
    assert response.status_code == 200
    assert "service" in response.json()


def test_login_endpoint_exists(client):
    """Test login endpoint exists (even with invalid credentials)"""
    response = client.post("/login", json={
        "email": "fake@test.com",
        "password": "fakepassword"
    })
    # Should be 401 (unauthorized) not 404 (not found)
    assert response.status_code == 401
    # Just check that we get an error response, don't check specific format
    response_data = response.json()
    assert "error" in response_data or "detail" in response_data


def test_docs_endpoint(client):
    """Test API docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_invalid_endpoint_returns_404(client):
    """Test invalid endpoints return 404"""
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404