from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

import test_utils

class SpringboardTest(test_utils.AuthenticatedTest):
    def test_display_code(self):
        response = self.c.get(reverse('springboard'))
        self.failUnlessEqual(response.status_code, 200)


