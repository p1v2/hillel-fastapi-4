import requests
import jwt


def get_access_token():
    request_data = {
        "username": "user",
        "password": "password"
    }

    response = requests.post("http://localhost:8000/auth/token", json=request_data)

    return response.json()["access_token"]


def decode_access_token(token):
    public_key = open("public_key.pem", "rb").read()
    ALGORITHM = "RS256"

    decoded_token = jwt.decode(token, public_key, algorithms=[ALGORITHM])

    return decoded_token


def test_me():
    access_token = get_access_token()

    response = requests.get("http://localhost:8000/auth/me", headers={"Authorization": f"Bearer {access_token}"})

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    test_me()
