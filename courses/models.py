from django.db import models

class Course(models.Model):
    title = models.CharField(max_length = 200)
    section = models.CharField(max_length = 10)
    number = models.CharField(max_length = 10)
    description = models.TextField()
