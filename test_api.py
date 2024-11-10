import random

import requests
from faker import Faker


def create_user():
    fake = Faker()
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone_number": '+380' + str(random.randint(100000000, 999999999)),
        "email": fake.email(),
    }

    response = requests.post("http://localhost:8000/v2/users", json=data)

    print(response.status_code)
    print(response.json())

    return response.json()


def get_users():
    response = requests.get("http://localhost:8000/v2/users")

    print(response.status_code)
    print(response.json())


def update_user(json):
    data = {
        **json,
        "email": "updated_email@gmail.com"
    }

    id = json["id"]

    response = requests.put(f"http://localhost:8000/v2/users/{id}", json=data)

    print(response.status_code)
    print(response.json())


def partially_update_user(json):
    data = {
        "email": "partially_updated_email@gmail.com"
    }

    id = json["id"]

    response = requests.patch(f"http://localhost:8000/v2/users/{id}", json=data)

    print(response.status_code)
    print(response.json())


def delete_user(json):
    id = json["id"]

    response = requests.delete(f"http://localhost:8000/v2/users/{id}")

    print(response.status_code)


def get_user(json):

    id = json["id"]
    response = requests.get(f"http://localhost:8000/v2/users/{id}")

    print(response.status_code)
    print(response.json())


def get_latest_user():
    response = requests.get("http://localhost:8000/v2/users/latest")
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    return response.json()


if __name__ == "__main__":
    get_user({"id": 10})
    get_latest_user()
    