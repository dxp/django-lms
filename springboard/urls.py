from django.conf.urls.defaults import *
from springboard.views import SpringBoard

urlpatterns = patterns('springboard.views',
                       url('$', SpringBoard.as_view(), name = 'springboard'),
                       )
