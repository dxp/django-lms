import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _

from djangotoolbox import fields
from tinymce import models as tinymce_models
import recurrence.fields

from libs.utils.fields import ForeignKey

class Semester(models.Model):
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

    def active(self):
        return self.start < datetime.date.today() and self.end > datetime.date.today()

    def save(self, *args, **kwargs):
        if self.start > self.end:
            raise ValueError, "Start date must be before end date."
        return super(Semester, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s" % (self.name, self.year)


class Course(models.Model):
    title = models.CharField(max_length = 200)
    section = models.CharField(max_length = 10)
    number = models.CharField(max_length = 10)
    description = tinymce_models.HTMLField()
    semester = models.ForeignKey(Semester)
    faculty = fields.ListField(ForeignKey(User, related_name = _('Faculty')))
    teaching_assistants = fields.ListField(ForeignKey(User, related_name = _('Teaching Assistants')))
    private = models.BooleanField(default=False, blank=True)
    members = fields.ListField(ForeignKey(User, related_name = _('Members')))
    schedule = recurrence.fields.RecurrenceField()
    credits = models.DecimalField(max_digits = 3, decimal_places = 1, default = '3.0')
    campus = models.CharField(max_length = 200,
                              choices = getattr(settings, 'CAMPUSES', [('main', 'Main'),] ),
        )
    location = models.CharField(max_length = 200)

    def __unicode__(self):
        return "%s" % (self.title)

    class Admin:
        js = (
            'tiny_mce/tiny_mce.js',
            '/appmedia/admin/js/textareas.js',
            ),


class Assignment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length = 200)
    description = tinymce_models.HTMLField()
    due_date = models.DateField(null = True)

    def __unicode__(self):
        return unicode(self.title)


class AssignmentSubmission(models.Model):
    users = fields.ListField(ForeignKey(User, related_name = 'submitters'))
    assignment = models.ForeignKey(Assignment)
    link = models.URLField(blank = True)
    file = models.FileField(upload_to = 'photos/%Y/%m/%d', blank = True)
    notes = models.TextField(blank = True)

    def __unicode__(self):
        if self.link:
            return self.link
        elif self.file:
            return self.file.name

class Resource(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length = 200)
    description = tinymce_models.HTMLField()
    link = models.URLField(blank = True)
    file = models.FileField(upload_to = 'photos/%Y/%m/%d', blank = True)

    def __unicode__(self):
        return self.title

