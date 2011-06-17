import sys
import os

from django.utils import unittest
import libs.test_utils as test_utils
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from profiles.models import Profile

class ProfilesTest(test_utils.AuthenticatedTest):
    '''
    Tests for our profiles application.
    '''
    def test_create(self):
        user = User(username = 'profiletest')
        user.save()

        # Test if we have a profile created. It should be created when a user is saved.
        profile = Profile.objects.get(user = user)
        assert profile

    def test_edit(self):
        response = self.c.get(reverse('profiles:edit'))
        self.assertEquals(response.status_code, 200)

        response = self.c.post(reverse('profiles:edit'),
                               {'biography':'Some test <bold>text</bold',
                                'resume': open('test_files/test.pdf'),
                                'mugshot': open('test_file/profile.gif'),
                                })
    
    
