import requests


def create_user(first_name, last_name, phone_number, email):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "email": email,
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

    print(f"Get Latest User Status: {response.status_code}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.json()}")


if __name__ == "__main__":
    json = create_user("Vasya", "Petrenko", "+380501234567", "vasya.petrenko@gmail.com")
    json2 = create_user("Petya", "Vasyliev", "+380501234568", "petya@gmail.com")

    get_user(json)

    get_latest_user()

    update_user(json)

    get_user(json)

    partially_update_user(json)

    get_user(json)

    delete_user(json)

    get_user(json)
