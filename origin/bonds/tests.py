from rest_framework.test import APISimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Bond
from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class AccountTests(APITestCase):

    def setUp(self):
        self.username = 'user1'
        self.password = 'pass1'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_unauthenticated_user_read(self):
        """
        Ensure we get 401 response when unauthenticated
        """
        resp = self.client.get("/bonds/")
        self.assertEqual(resp.status_code, 401)

    def test_unauthenticated_add(self):
        """
        Ensure we get 401 response when unauthenticated
        """
        data = {
                "isin": "FR0000131104",
                "size": 100000000,
                "currency": "EUR",
                "maturity": "2025-02-28",
                "lei": "R0MUWSFPU8MPRO8K5P83"
                }
        response = self.client.post("/bonds/", data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Bond.objects.count(), 0)

    def test_authenticated_add(self):
        """
        Ensure we can add a new bond when authenticated
        """
        self.client.login(username=self.username, password=self.password)
        before_count = Bond.objects.count()
        data = {
                "isin": "FR0000131104",
                "size": 100000000,
                "currency": "EUR",
                "maturity": "2025-02-28",
                "lei": "R0MUWSFPU8MPRO8K5P83"
                }
        response = self.client.post("/bonds/", data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bond.objects.count(), before_count + 1)
        self.assertEqual(Bond.objects.get().isin, 'FR0000131104')
        self.client.logout()

    def test_authenticated_read(self):
        """
        Ensure we can read bonds for a user when authenticated
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/bonds/")
        self.assertEqual(response.status_code, 200)
        self.client.logout()

