from django.utils import unittest
import sys
import os

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File

from springboard.models import IntranetApplication

import test_utils

class SpringboardTest(test_utils.AuthenticatedTest):
    def test_display_code(self):
        response = self.c.get(reverse('springboard'))
        self.failUnlessEqual(response.status_code, 200)
        
    def test_display_icon(self):
        here = os.path.dirname( os.path.abspath(__file__) )
        f = open(here + '/test_files/test_icon.png')
        application = IntranetApplication(url = '/test', title='Test')
        application.save()
        application.icon.save('test_icon.png', File(f))
        
        response = self.c.get(reverse('springboard'))
        try:
            self.assertContains(response, 'Test')
        except:
            print(response)
            raise

