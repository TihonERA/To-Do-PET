def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]  

def test_registration_page(client):
    response = client.get("/registration")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]  