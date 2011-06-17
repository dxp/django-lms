from django.conf.urls.defaults import *
from profiles.views import (ProfileEdit)
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('profiles.views',
                       url('^(?P<username>[-\w]+)/edit/$', login_required(ProfileEdit.as_view()), name = 'edit'),
                       )
