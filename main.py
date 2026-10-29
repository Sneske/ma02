import requests
import sqlite3

API_BASE = "http://164.92.167.24"
EMAIL = "laki1000@stud.ek.dk"

def get_token():
    response = requests.post(f"{API_BASE}/api/auth/token", json={"email": EMAIL})
    return response.json()["token"]

def get_incidents(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/api/incidents?$skip=0&$top=205", headers=headers)
    return response.json()

token = get_token()
incidents = get_incidents(token)
# print(incidents["value"])

SQLog = sqlite3.connect("Incidents.db")
cursor = SQLog.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Incidents 
(alertId TEXT NOT NULL, incidentId TEXT NOT NULL, category TEXT NOT NULL, machineId TEXT NOT NULL, 
firstSeen TEXT NOT NULL, timestamp TEXT NOT NULL, detectionSource TEXT NOT NULL)""")
cursor.execute("""DELETE FROM Incidents""")

x = 0
y = 0

while True:
    try:
        i = incidents["value"][x]
        incidentId = i["incidentId"]
        try:
            alertId = i["alerts"][y]["alertId"]
            category = i["alerts"][y]["category"]
            machineId = i["alerts"][y]["machineId"]
            firstSeen = i["alerts"][y]["firstSeen"]
            timestamp = i["alerts"][y]["lastSeen"]
            detectionSource = i["alerts"][y]["detectionSource"]
            y += 1
        except IndexError:
            y = 0
            x += 1
            continue
        try:
            cursor.execute("INSERT INTO incidents (alertId, incidentId, category, machineId, firstSeen, timestamp, detectionSource) values (?, ?, ?, ?, ?, ?, ?)", 
                (alertId, incidentId, category, machineId, firstSeen, timestamp, detectionSource))
        except sqlite3.IntegrityError:
            raise sqlite3.IntegrityError("An error occured with importing")
    except IndexError:
        print("Finished")
        break

SQLog.commit()
SQLog.close()