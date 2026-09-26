from django.test import TestCase, Client


class HealthCheckTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_health_check(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "healthy")


class DashboardTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


class AddMonitorTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_add_monitor_page(self):
        response = self.client.get("/add_monitor/")

        self.assertEqual(response.status_code, 200)