from django.conf.urls.defaults import *
from profiles.views import (ProfileEdit,
                            ProfileDetail)
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('profiles.views',
                       url('^(?P<username>[-\w]+)/edit/$', login_required(ProfileEdit.as_view()), name = 'edit'),
                       url('^(?P<username>[-\w]+)/$', login_required(ProfileDetail.as_view()), name = 'detail'),
                       )
