from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os


MONITORS_FILE = "/monitor/data/monitors.json"
HISTORY_FILE = "/monitor/data/health_history.json"


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


def home(request):

    return redirect("/dashboard/")


def add_monitor(request):

    error = None

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        url = request.POST.get("url", "").strip()

        if not name or not url:

            error = "Both application name and URL are required."

        elif not (
            url.startswith("http://")
            or url.startswith("https://")
        ):

            error = "URL must start with http:// or https://"

        else:

            monitors = load_json(MONITORS_FILE, [])

            new_id = 1

            if monitors:
                new_id = max(
                    monitor["id"]
                    for monitor in monitors
                ) + 1

            new_monitor = {
                "id": new_id,
                "name": name,
                "url": url,
                "active": True
            }

            monitors.append(new_monitor)

            save_json(MONITORS_FILE, monitors)

            return redirect("/dashboard/")

    return render(
        request,
        "monitor/add_monitor.html",
        {"error": error}
    )


def delete_monitor(request, monitor_id):

    if request.method == "POST":

        monitors = load_json(MONITORS_FILE, [])

        monitors = [
            monitor
            for monitor in monitors
            if monitor["id"] != monitor_id
        ]

        save_json(MONITORS_FILE, monitors)

        history = load_json(HISTORY_FILE, [])

        history = [
            check
            for check in history
            if check.get("monitor_id") != monitor_id
        ]

        save_json(HISTORY_FILE, history)

    return redirect("/dashboard/")


def toggle_monitor(request, monitor_id):

    if request.method == "POST":

        monitors = load_json(MONITORS_FILE, [])

        for monitor in monitors:

            if monitor["id"] == monitor_id:

                monitor["active"] = not monitor.get(
                    "active",
                    True
                )

                break

        save_json(MONITORS_FILE, monitors)

    return redirect("/dashboard/")


def monitor_detail(request, monitor_id):

    monitors = load_json(MONITORS_FILE, [])

    monitor = next(
        (
            m for m in monitors
            if m["id"] == monitor_id
        ),
        None
    )

    if monitor is None:
        return redirect("/")


    history = load_json(HISTORY_FILE, [])

    monitor_history = [
        check
        for check in history
        if (
            check.get("monitor_id") == monitor_id
            or check.get("monitor_name") == monitor["name"]
        )
    ]

    monitor_history = monitor_history[-50:]

    latest = (
        monitor_history[-1]
        if monitor_history
        else None
    )

    context = {
        "monitor": monitor,
        "history": reversed(monitor_history),
        "latest": latest,
        "chart_data": json.dumps(monitor_history)
    }

    return render(
        request,
        "monitor/monitor_detail.html",
        context
    )


def health_check(request):

    return JsonResponse(
        {
            "status": "healthy",
            "checks": {
                "django": "ok"
            }
        },
        status=200
    )


def dashboard(request):

    monitors = load_json(MONITORS_FILE, [])
    history = load_json(HISTORY_FILE, [])

    monitor_data = []


    for monitor in monitors:

        monitor_history = [
            check
            for check in history
            if check.get("monitor_id") == monitor["id"]
        ]


        if monitor_history:

            latest = monitor_history[-1]

            # Keep only the latest 20 checks for the graph
            graph_history = monitor_history[-20:]


            # Extract timestamps
            graph_labels = [
                check.get("timestamp")
                for check in graph_history
            ]


            # Extract response times
            graph_values = [
                check.get("response_time")
                for check in graph_history
            ]


            monitor_info = {

                "id": monitor["id"],

                "name": monitor["name"],

                "url": monitor["url"],

                "active": monitor.get(
                    "active",
                    True
                ),

                "status": latest.get(
                    "status",
                    "unknown"
                ),

                "response_time": latest.get(
                    "response_time"
                ),

                "timestamp": latest.get(
                    "timestamp"
                ),

                "http_status": latest.get(
                    "http_status"
                ),

                "error": latest.get(
                    "error"
                ),

                # IMPORTANT:
                # Convert Python lists into valid JSON
                # before sending them to JavaScript.

                "graph_labels": json.dumps(
                    graph_labels
                ),

                "graph_values": json.dumps(
                    graph_values
                )
            }


        else:

            monitor_info = {

                "id": monitor["id"],

                "name": monitor["name"],

                "url": monitor["url"],

                "active": monitor.get(
                    "active",
                    True
                ),

                "status": "unknown",

                "response_time": None,

                "timestamp": None,

                "http_status": None,

                "error": None,

                "graph_labels": json.dumps([]),

                "graph_values": json.dumps([])
            }


        monitor_data.append(
            monitor_info
        )


    # -----------------------------
    # DASHBOARD STATISTICS
    # -----------------------------

    total_monitors = len(
        monitor_data
    )


    healthy_monitors = len([
        monitor
        for monitor in monitor_data
        if monitor["status"] == "healthy"
    ])


    unhealthy_monitors = len([
        monitor
        for monitor in monitor_data
        if monitor["status"] == "unhealthy"
    ])


    checked = [
        monitor
        for monitor in monitor_data
        if monitor["response_time"] is not None
    ]


    if checked:

        average_response = round(
            sum(
                monitor["response_time"]
                for monitor in checked
            )
            / len(checked),
            2
        )

    else:

        average_response = None


    context = {

        "monitors": monitor_data,

        "total_monitors":
            total_monitors,

        "healthy_monitors":
            healthy_monitors,

        "unhealthy_monitors":
            unhealthy_monitors,

        "average_response":
            average_response
    }


    return render(
        request,
        "monitor/dashboard.html",
        context
    )