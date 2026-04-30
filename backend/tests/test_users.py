import pytest

def test_get_current_user(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    data = response.json()
    assert response.status_code == 200
    assert data["login"] == "pytest_user"
    assert data["email"] == "pytest_user@gmail.com"


def test_update_profile_invalid(client, auth_headers):
    form_data = {
        "new_login": "pytest_user",
        "new_email": "pytest_user@gmail.com"
    }
    response = client.patch("/users/update_profile", data=form_data, headers=auth_headers)
    assert response.status_code == 404

def test_update_profile(client, auth_headers):
    # Сохраняем старые данные
    old_data = client.get("/users/me", headers=auth_headers).json()
    old_login = old_data["login"]
    old_email = old_data["email"]
    
    # Обновляем профиль
    form_data = {
        "new_login": "pytestik",
        "new_email": "pytest_bot@gmail.com"
    }
    response = client.patch("/users/update_profile", data=form_data, headers=auth_headers)
    data = response.json()
    
    assert response.status_code == 200
    assert data["login"] == "pytestik"
    assert data["email"] == "pytest_bot@gmail.com"
    
    # ВОССТАНАВЛИВАЕМ старые данные
    revert_data = {
        "new_login": old_login,
        "new_email": old_email
    }
    client.patch("/users/update_profile", data=revert_data, headers=auth_headers)

def test_update_password(client, auth_headers):
    form_data = {
        "old_password": "pytestpassword15",
        "new_password": "pytestpassword16"
    }
    revert_data = {
        "old_password": "pytestpassword16",
        "new_password": "pytestpassword15"
    }
    response = client.patch("/users/update_password", data=form_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Password successfully changed"
    client.patch("/users/update_password", data=revert_data, headers=auth_headers)

def test_bad_password(client, auth_headers):
    form_data = {
        "old_password": "wrongpasswordssssssss",
        "new_password": "pytestpassword16"
    }
    response = client.patch("/users/update_password", data=form_data, headers=auth_headers)
    assert response.status_code == 400