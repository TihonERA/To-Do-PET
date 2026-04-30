def test_registration(client):
    form_data = {
        "email": "pytest@gmail.com",
        "login": "testuser",
        "password": "pytestpassword15"
    }

    response = client.post("/register", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_loginpage_via_login(client):
    login_data = {
        "login_or_email": "testuser",
        "password": "pytestpassword15"
    }

    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_loginpiage_via_email(client):
    login_data = {
        "login_or_email": "pytest@gmail.com",
        "password": "pytestpassword15"
    }

    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def registration_test_invalid_data(client):
    form_data = {
        "email": "pytest@gmail.co",
        "login": "tesuser",
        "password": "pytestpasswd15"
    }

    response = client.post("/register", data=form_data)
    assert response.status_code == 401

def login_test_invalid_data(client):
    form_data = {
        "login_or_email": "testur",
        "password": "pytestpasswor15"
    }

    response = client.post("/login", data=form_data)
    assert response.status_code == 401
