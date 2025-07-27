
from rest_framework.test import APIClient
from django.test import TestCase
from .auth_utils import create_access_token

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.token = create_access_token({"sub": "john", "role": "patient"})
        self.invalid_token = "invalid.token.here"

    def test_dashboard_access_with_valid_token(self):
        response = self.client.get("/backend/patient-dashboard/", HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access_with_invalid_token(self):
        response = self.client.get("/backend/patient-dashboard/", HTTP_AUTHORIZATION=f"Bearer {self.invalid_token}")
        self.assertEqual(response.status_code, 403)
