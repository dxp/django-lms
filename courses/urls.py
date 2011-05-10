from django.conf.urls.defaults import *
from courses.views import (CourseOverview,
                           BySemesterList,
                           CourseDropPage,
                           CourseAdmin,
                           ToggleMembership,
                           NewCourseAssignment,
                           AssignmentList,
                           AssignmentOverview,)
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('courses.views',
                       url('^(?P<pk>\d+)/overview/$', login_required(CourseOverview.as_view()), name = 'overview'),
                       url('^(?P<pk>\d+)/admin/$', login_required(CourseAdmin.as_view()), name = 'admin'),
                       url('^(?P<pk>\d+)/assignments/new/$', login_required(NewCourseAssignment.as_view()), name = 'new_assignment'),
                       url('^(?P<pk>\d+)/assignments/$', login_required(AssignmentList.as_view()), name = 'assignments'), 
                       url('^assignment/(?P<pk>\d+)/overview/$', login_required(AssignmentOverview.as_view()), name = 'assignment_overview'),
                       url('^(?P<pk>\d+)/toggle-membership/$', login_required(ToggleMembership.as_view()), name = 'toggle-membership'),
                       url('^semester/(?P<pk>\d+)/$', login_required(BySemesterList.as_view()), name = 'by_semester'),
                       url('^$', login_required(CourseDropPage.as_view()), name = 'drop_page'),
                       )
