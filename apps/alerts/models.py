from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

ALERT_LEVELS = (
    ('info','Information'),
    ('','Warning'),
    ('success','Success'),
    ('error','Error'),
    ('danger','Danger'),
    )

class Alert(models.Model):
    # This is char because there are a wide variety that can send
    sent_by = models.CharField(max_length = 200)
    sent_to = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    title = models.CharField(max_length = 200)
    details = tinymce_models.HTMLField(blank = True)
    level = models.CharField(max_length = 200, choices = ALERT_LEVELS, blank = True)

