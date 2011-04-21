from django.conf.urls.defaults import *
from courses.views import CourseOverview, BySemesterList
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('courses.views',
                       url('(?P<pk>\d+)/overview/', login_required(CourseOverview.as_view()), name = 'overview'),
                       url('semester/(?P<pk>\d+)/', login_required(BySemesterList.as_view()), name = 'by_semester'),
                       )
