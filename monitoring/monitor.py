import time
import urllib.request
import urllib.error
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

MONITORS_FILE = "/monitor/data/monitors.json"
DATA_FILE = "/monitor/data/health_history.json"

CHECK_INTERVAL = 10


def load_json(file_path, default):
    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception:
        return default


def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def check_monitor(monitor):

    url = monitor["url"]

    timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

    try:

        start_time = time.time()

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "ReliabilityPlatform/1.0"
            }
        )

        response = urllib.request.urlopen(
            request,
            timeout=5
        )

        response_time = (time.time() - start_time) * 1000

        status_code = response.status

        if 200 <= status_code < 400:

            status = "healthy"

        else:

            status = "unhealthy"

        result = {
            "monitor_id": monitor["id"],
            "timestamp": timestamp,
            "status": status,
            "response_time": round(response_time, 2),
            "http_status": status_code,
            "error": None
        }

        print(
            f"[{status.upper()}] {monitor['name']} | "
            f"Status: {status_code} | "
            f"Response time: {response_time:.2f} ms",
            flush=True
        )

        return result

    except urllib.error.HTTPError as e:

        response_time = (time.time() - start_time) * 1000

        result = {
            "monitor_id": monitor["id"],
            "timestamp": timestamp,
            "status": "unhealthy",
            "response_time": round(response_time, 2),
            "http_status": e.code,
            "error": f"HTTP {e.code}: {e.reason}"
        }

        print(
            f"[UNHEALTHY] {monitor['name']} | "
            f"HTTP {e.code}: {e.reason}",
            flush=True
        )

        return result

    except Exception as e:

        result = {
            "monitor_id": monitor["id"],
            "timestamp": timestamp,
            "status": "unhealthy",
            "response_time": None,
            "http_status": None,
            "error": str(e)
        }

        print(
            f"[UNHEALTHY] {monitor['name']} | "
            f"Application not reachable | {e}",
            flush=True
        )

        return result


def check_all_monitors():

    monitors = load_json(MONITORS_FILE, [])
    history = load_json(DATA_FILE, [])

    for monitor in monitors:

        if not monitor.get("active", True):
            continue

        result = check_monitor(monitor)

        history.append(result)

    # Keep latest 200 checks
    history = history[-200:]

    save_json(DATA_FILE, history)


print("Health monitor started...", flush=True)


while True:

    check_all_monitors()

    time.sleep(CHECK_INTERVAL)