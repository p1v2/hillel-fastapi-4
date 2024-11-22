import requests

resp = requests.get("http://localhost:8000/v2/products")
print(resp.json())
print(resp.status_code)

data = {
    "name": "Pepsi",
    "price": 5
}
resp = requests.post("http://localhost:8000/v2/products/", json=data)

print(resp.json())
print(resp.status_code)

id = resp.json()["_id"]

resp = requests.get(f"http://localhost:8000/v2/products/{id}")

print(resp.json())

data = {
    "name": "Pepsi",
    "price": 6
}
resp = requests.put(f"http://localhost:8000/v2/products/{id}", json=data)

print(resp.json())

resp = requests.delete(f"http://localhost:8000/v2/products/{id}")

print(resp.status_code)
print(resp.text)