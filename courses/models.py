from django.db import models
from django.contrib.auth.models import Group, User
from tinymce import models as tinymce_models

class Semester(models.Model):
    name = models.CharField(max_length = 200)
    year = models.IntegerField()
    start = models.DateField()
    end = models.DateField()

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
    faculty = models.ManyToManyField(User, related_name = 'faculty')
    private = models.BooleanField(default=False, blank=True)
    members = models.ManyToManyField(User, related_name = 'members')

    def __unicode__(self):
        return "%s: %s %s" % (self.title, self.semester.name, self.semester.year)

    class Admin:
        js = (
            'tiny_mce/tiny_mce.js',
            '/appmedia/admin/js/textareas.js',
            ),
