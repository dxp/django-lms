from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

class Alert(models.Model):
    # This is char because there are a wide variety that can send
    sent_by = models.CharField(max_length = 200)
    sent_to = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    title = models.CharField(max_length = 200)
    details = tinymce_models.HTMLField()
    level = models.CharField(max_length = 200)

