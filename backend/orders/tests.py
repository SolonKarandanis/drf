from django.test import TestCase
from rest_framework import status


# Create your tests here.
class URLTests(TestCase):

    def test_get_user_orders(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
