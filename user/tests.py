from django.test import TestCase
from django.test.client import Client
from user.models import MyUser
from rest_framework.test import APIClient
# Create your tests here.

client = APIClient()


class ResgisterTest(TestCase):
    def test_register(self):
        response = client.post(
            '/api/user/register/', {'email': 'a@a.com', 'username': 'aaaa', 'password': 'aaaaaaaa'})
        self.assertEqual(response.status_code, 201)

    def test_username_alnumeric(self):
        response = client.post(
            '/api/user/register/', {'email': 'a@a.com', 'username': 'aaaa 123', 'password': 'aaaaaaaa'})
        self.assertEqual(response.status_code, 400)
