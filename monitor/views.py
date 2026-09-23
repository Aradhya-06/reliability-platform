from django.shortcuts import render
from django.http import JsonResponse
import json
import os

tasks=[
    {
        "id":1,
        "title": "Complete project",
        "completed": False
    },
    {
        "id":2,
        "title": "Test deployment",
        "completed": True
    }
]

def home(request):
    return render(request,"monitor/home.html")

def health_check(request):
    return JsonResponse({"status":"healthy"})

def get_tasks(request):
    return JsonResponse({"tasks": tasks})

def dashboard(request):

    data_file = "/monitor/data/health_history.json"

    if os.path.exists(data_file):

        with open(data_file, "r") as file:
            history = json.load(file)

    else:
        history = []

    total_checks = len(history)

    successful_checks = len([
        check for check in history
        if check["status"] == "healthy"
    ])

    if history:
        current_status = history[-1]["status"]
        latest_response = history[-1]["response_time"]

    else:
        current_status = "unknown"
        latest_response = "—"

    context = {
        "history": reversed(history[-20:]),
        "total_checks": total_checks,
        "successful_checks": successful_checks,
        "latest_response": latest_response,
        "current_status": current_status
    }

    return render(request, "monitor/dashboard.html", context)