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
