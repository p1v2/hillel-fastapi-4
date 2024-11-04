import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"  # Адреса сервера FastAPI

def test_create_user():
    unique_email = f"user_{uuid.uuid4()}@example.com"  # Генерація унікального email
    response = requests.post(f"{BASE_URL}/users", json={
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+380123456789",
        "email": unique_email,
        "password": "strongpassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    return data["id"]  # Повертаємо user_id для подальших тестів

def test_read_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user():
    user_id = test_create_user()  # Отримуємо user_id
    response = requests.put(f"{BASE_URL}/users/{user_id}", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "phone_number": "+380987654321",
        "email": f"jane_{uuid.uuid4()}@example.com",  # Унікальний email
        "password": "newstrongpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"

def test_partial_update_user():
    user_id = test_create_user()  # Отримуємо user_id
    response = requests.patch(f"{BASE_URL}/users/{user_id}", json={
        "first_name": "Jake"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jake"

def test_delete_user():
    user_id = test_create_user()  # Отримуємо user_id
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 204
