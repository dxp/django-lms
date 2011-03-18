from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.views',
                       url('$', 'dashboard', name = 'dashboard'),
                       )
