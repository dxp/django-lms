from django.utils import unittest
import django
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

class AuthenticatedTest(django.test.TestCase):
    def setUp(self):
        self.c = Client()

        # create login
        user = User(username = 'test', first_name = 'Test', last_name = 'McTesterson', email = 'test@test.com')
        user.save()
        user.set_password('test123')
        user.save()

        # login
        response = self.c.post('/accounts/login/', {'username': 'test', 'password': 'test123', 'next': '/'})

        self.assertRedirects(response, '/')
