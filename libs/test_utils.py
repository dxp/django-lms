from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

class AuthenticatedTest(unittest.TestCase):
    def setUp(self):
        self.c = Client()

        # create login
        user = User(username = 'test', password = 'test123', first_name = 'Test', last_name = 'McTesterson', email = 'test@test.com')
        user.save()

        # login
        response = self.c.post('/accounts/login/', {'username': 'test', 'password': 'test123'})
        self.failUnlessEqual(response.status_code, 200)
