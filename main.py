import requests
import sqlite3
import json

db = sqlite3.connect("database.db")
c = db.cursor()

ip = "http://164.92.167.24"
email = "siso1007@stud.ek.dk"


def get_token():
    response = requests.post(f"{ip}/api/auth/token", json={"email": email})
    open("token.txt", "a").write(f"{response.json()["token"]}\n")
    return response.json()["token"]

def get_incidents(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{ip}/api/incidents", headers=headers)
    return response.json()

token = get_token()
incidents = get_incidents(token)
print(incidents["value"])
