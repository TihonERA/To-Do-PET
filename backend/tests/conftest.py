import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
from backend.main import app
from backend.models.base import Base
from backend.models import user, task
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_user_data():
    return {
        "email": "test_user@example.com",
        "login": "test_user",
        "password": "TestPassword123!"
    }

# Создаем один клиент на все тесты
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

# Фикстура для получения токена авторизации
@pytest.fixture(scope="function")
def auth_token(client):
    """
    Регистрирует пользователя и возвращает токен.
    Этот токен можно использовать в любых других тестах.
    """
    # 1. Регистрация
    register_data = {
        "email": "pytest_user@gmail.com",
        "login": "pytest_user",
        "password": "pytestpassword15"
    }
    response = client.post("/register", json=register_data)
    
    # Если пользователь уже есть (от предыдущих запусков), может быть ошибка 409.
    # Для простоты теста считаем, что регистрация успешна или пользователь уже существует.
    if response.status_code not in [200, 201, 409]:
        raise Exception(f"Failed to register user: {response.json()}")

    # 2. Логин для получения токена
    login_data = {
        "login_or_email": "pytest_user",
        "password": "pytestpassword15"
    }
    response = client.post("/login", json=login_data)
    
    assert response.status_code == 200
    return response.json()["access_token"]

# Фикстура для заголовков с токеном
@pytest.fixture(scope="function")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
