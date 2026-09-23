from django.test import TestCase


class HealthCheckTest(TestCase):
    def test_health_check(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")


class TasksTest(TestCase):
    def test_tasks_endpoint(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasks", response.json())