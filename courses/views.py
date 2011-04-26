import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.core import exceptions

from courses.models import Course, Semester
from courses.forms import CourseAdminForm

class CourseOverview(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CourseOverview, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    # Overriding the dispatch to check visibility
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        course = self.get_object()

        if course.private:
            if not request.user in course.faculty.all() or not request.user in course.members.all():
                raise exceptions.PermissionDenied

        return super(CourseOverview, self).dispatch(request, *args, **kwargs)

# TODO: Check if user is faculty
class CourseAdmin(UpdateView):
    form_class = CourseAdminForm
    template_name = "courses/admin.html"

    queryset = Course.objects.all()

    def get_success_url(self):
        course = self.get_object()
        return reverse('courses:admin', kwargs={'pk':course.id})

    def get_context_data(self, **kwargs):
        context = super(CourseAdmin, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class BySemesterList(ListView):
    context_object_name = "courses"
    template_name = "courses/by_semester.html"

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['pk'])
        return self.semester.course_set.all()

    
    def get_context_data(self, **kwargs):
        context = super(BySemesterList, self).get_context_data(**kwargs)
        context['semester'] = self.semester
        return context

class CourseDropPage(RedirectView):
    '''
    Gets the current semester and redirects to its page
    '''
    url = None
    permanent = False

    def get_redirect_url(self, **kwargs):
        semesters = Semester.objects.filter(start__lt = datetime.date.today(), end__gt = datetime.date.today())
        if not semesters:
            raise ValueError, "No current semester"
        semester = semesters[0]
        url = reverse('courses:by_semester', kwargs={'pk':semester.id})
        return url
