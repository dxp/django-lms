import sys
import os
import datetime

from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files import File

from courses.models import Course, Semester

import test_utils

class SemesterTest(test_utils.AuthenticatedTest):
    def test_create(self):
        semester = Semester(name='Spring', year = '2012', start = datetime.date(2012, 1, 1), end = datetime.date(2012, 5, 15))
        semester.save()
        self.assertEquals(semester.name, 'Spring')
        self.assertEquals(semester.year, '2012')
        self.assertEquals(semester.start, datetime.date(2012, 1, 1))
        self.assertEquals(semester.end, datetime.date(2012, 5, 15))
        semester.delete()

        # Try invalid start and end date
        semester = Semester(name='Spring', year = '2012', start = datetime.date(2012, 5, 15), end = datetime.date(2012, 1, 1))
        self.assertRaises(ValueError, semester.save, ())
        
    def test_listing(self):
        semester = Semester(name='Spring', year = '2012', start = datetime.date(2012, 1, 1), end = datetime.date(2012, 5, 15))
        semester.save()

        course = Course(title='Test Course', number = '101', section = '001', description = 'Test description of a course', semester = semester)
        course.save()
        course = Course(title='Test Course2', number = '101', section = '002', description = 'Test description of a course', semester = semester)
        course.save()
        course = Course(title='Test Course3', number = '102', section = '001', description = 'Test description of a course', semester = semester)
        course.save()

        response = self.c.get(reverse('courses:by_semester', args = [semester.id]))
        courses = Course.objects.filter(semester = semester)
        self.assertEquals([course.id for course in response.context['courses']], [course.id for course in courses])


class CoursesTest(test_utils.AuthenticatedTest):
    def test_create(self):
        semester = Semester(name='Spring', year = '2012', start = datetime.date(2012, 1, 1), end = datetime.date(2012, 5, 1))
        semester.save()

        course = Course(title='Test Course', number = '101', section = '001', description = 'Test description of a course', semester = semester)
        course.save()
        self.assertEquals(course.title, 'Test Course')
        self.assertEquals(course.number, '101')
        self.assertEquals(course.section, '001')
        self.assertEquals(course.description, 'Test description of a course')

    def test_view(self):
        semester = Semester(name='Spring', year = '2012', start = datetime.date(2012, 1, 1), end = datetime.date(2012, 5, 1))
        semester.save()

        course = Course(title='Test Course', number = '101', section = '001', description = 'Test description of a course', semester = semester)
        course.save()

        response = self.c.get(reverse('courses:overview', args = [course.id]))

        self.assertEquals(response.context['course'].title, 'Test Course')
        self.assertEquals(response.context['course'].number, '101')
        self.assertEquals(response.context['course'].section, '001')
        self.assertEquals(response.context['course'].description, 'Test description of a course')

