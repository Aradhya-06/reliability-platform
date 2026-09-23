import time
import urllib.request
import json
import os
from datetime import datetime


URL = "http://web:8000/health/"
CHECK_INTERVAL = 10

DATA_FILE = "data/health_history.json"


def load_history():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    with open(DATA_FILE, "w") as file:
        json.dump(history, file, indent=4)


def check_health():

    history = load_history()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        start_time = time.time()

        response = urllib.request.urlopen(URL, timeout=5)

        response_time = (time.time() - start_time) * 1000

        if response.status == 200:

            result = {
                "timestamp": timestamp,
                "status": "healthy",
                "response_time": round(response_time, 2)
            }

            print(
                f"[HEALTHY] Status: {response.status} | "
                f"Response time: {response_time:.2f} ms",
                flush=True
            )

        else:

            result = {
                "timestamp": timestamp,
                "status": "unhealthy",
                "response_time": None
            }

            print(
                f"[UNHEALTHY] Status: {response.status}",
                flush=True
            )

    except Exception as e:

        result = {
            "timestamp": timestamp,
            "status": "unhealthy",
            "response_time": None
        }

        print(
            f"[UNHEALTHY] Application is not reachable | {e}",
            flush=True
        )

    history.append(result)

    # Keep only the latest 100 checks
    history = history[-100:]

    save_history(history)


def wait_for_application():
    print("Waiting for application to start...", flush=True)

    while True:
        try:
            response = urllib.request.urlopen(URL, timeout=3)

            if response.status == 200:
                print("Application is ready!", flush=True)
                return

        except Exception:
            print("Application not ready yet. Retrying...", flush=True)

        time.sleep(2)


print("Health monitor started...", flush=True)

wait_for_application()

while True:
    check_health()
    time.sleep(CHECK_INTERVAL)