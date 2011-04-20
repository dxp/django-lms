from django.utils import unittest
import sys
import os

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File

from courses.models import Course

import test_utils

class CoursesTest(test_utils.AuthenticatedTest):
    def test_create(self):
        course = Course(title='Test Course', number = '101', section = '001', description = 'Test description of a course')
        course.save()
        self.assertEquals(course.title, 'Test Course')
        self.assertEquals(course.number, '101')
        self.assertEquals(course.section, '001')
        self.assertEquals(course.description, 'Test description of a course')

