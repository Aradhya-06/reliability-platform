# Reliability Platform

A lightweight application monitoring and health-check platform built using Django, Docker, and Terraform.

The platform allows users to add websites or applications that they want to monitor. A separate monitoring service periodically sends HTTP requests to the configured URLs and records their health status, HTTP status code, response time, timestamp, and errors.

The collected monitoring data is displayed through a web dashboard.

---

## Features

- Add websites or applications for monitoring
- Automatic health checks at regular intervals
- Monitor multiple applications
- HTTP status monitoring
- Response-time measurement
- Healthy / Unhealthy status detection
- Detection of unreachable applications
- Error reporting for failed requests
- Pause and resume monitoring
- Delete monitors
- Monitoring history
- Response-time visualization
- Dashboard with application statistics
- Docker-based development environment
- Terraform infrastructure configuration
- GitHub Actions CI pipeline

---

## Project Architecture

```text
                    User
                     |
                     v
            +------------------+
            | Django Dashboard |
            |                  |
            | Add Monitor      |
            | View Status      |
            | View History     |
            +--------+---------+
                     |
                     |
                     v
            +------------------+
            | Monitoring       |
            | Service          |
            |                  |
            | HTTP Health      |
            | Checks           |
            | Response Time     |
            +--------+---------+
                     |
                     v
          +----------------------+
          | Monitored Applications|
          |                      |
          | Websites / APIs      |
          +----------------------+

                     |
                     v
            monitoring data
                     |
                     v
             JSON data files
````

---

## Technology Stack

### Backend

* Python
* Django

### Monitoring

* Python
* HTTP requests
* Periodic health checks
* Response-time measurement

### Frontend

* HTML
* CSS
* Django Templates
* JavaScript where required

### Containerization

* Docker
* Docker Compose

### Infrastructure

* Terraform
* AWS infrastructure configuration

### CI/CD

* GitHub Actions

---

## How Monitoring Works

When a user adds an application, the platform stores its name and URL.

The monitoring service periodically checks the configured URL.

For every check, the following information is recorded:

```text
Monitor ID
Timestamp
Health status
Response time
HTTP status code
Error message
```

For example:

```json
{
    "monitor_id": 1,
    "timestamp": "2026-09-25 16:33:46",
    "status": "healthy",
    "response_time": 98.77,
    "http_status": 200,
    "error": null
}
```

A successful HTTP response is reported as healthy.

Errors such as HTTP failures, connection errors, or timeouts are reported as unhealthy.

---

## Project Structure

```text
reliability-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── monitor/
│   ├── templates/
│   │   └── monitor/
│   │       ├── dashboard.html
│   │       ├── add_monitor.html
│   │       └── monitor_detail.html
│   │
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── monitoring/
│   ├── data/
│   │   ├── health_history.json
│   │   └── monitors.json
│   │
│   └── monitor.py
│
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   └── .terraform.lock.hcl
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Aradhya-06/reliability-platform.git
cd reliability-platform
```

### 2. Build the Docker containers

```bash
docker compose build
```

### 3. Start the application

```bash
docker compose up
```

The Django application can then be accessed through the configured localhost port.

---

## Docker Services

The project separates the Django application and monitoring process.

### Web Service

Runs the Django application and provides:

* Dashboard
* Add Monitor interface
* Health endpoint
* Monitor details

### Monitor Service

Runs the monitoring process independently.

It periodically checks the configured applications and records monitoring information.

This separation allows the monitoring service to continue checking applications independently of the dashboard logic.

---

## Example Monitoring Results

### Healthy Application

```text
Status: HEALTHY
HTTP Status: 200
Response Time: 18.88 ms
```

### Unhealthy Application

```text
Status: UNHEALTHY
HTTP Status: 403
Response Time: 879.46 ms
Error: HTTP 403: Forbidden
```

The dashboard displays these results for each monitored application.

---

## CI Pipeline

The project uses GitHub Actions for continuous integration.

The CI pipeline is intended to automatically verify the project whenever changes are pushed to GitHub.

The pipeline includes checks such as:

```text
Git Push
   |
   v
GitHub Actions
   |
   +--> Install dependencies
   |
   +--> Django checks
   |
   +--> Run tests
   |
   +--> Build Docker image
   |
   v
Build verified
```

---

## Terraform

Terraform configuration is included in the project to define infrastructure as code.

Terraform files are stored in:

```text
terraform/
```

The `.terraform/` directory is intentionally excluded from Git because it contains downloaded provider binaries.

Typical Terraform commands are:

```bash
terraform init
terraform validate
terraform plan
```

Infrastructure can then be provisioned after reviewing the generated plan.

---

## Future Improvements

Possible future improvements include:

* AWS deployment
* Automated deployment through GitHub Actions
* Persistent database instead of JSON storage
* User authentication
* Email or notification alerts
* Uptime percentage calculation
* More detailed monitoring analytics
* Historical response-time graphs
* Scalable monitoring workers
* Production deployment architecture

---

## Project Goal

The goal of the Reliability Platform is to provide a simple monitoring system that allows users to track the availability and response performance of their own applications.

The project demonstrates concepts including:

* Web application development
* Application monitoring
* HTTP health checks
* Docker containerization
* Infrastructure as Code
* Continuous Integration
* Cloud deployment

```

