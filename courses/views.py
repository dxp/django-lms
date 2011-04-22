from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from django.views.generic import DetailView, ListView
from courses.models import Course, Semester

class CourseOverview(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CourseOverview, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

# TODO: Check if user is faculty
class CourseAdmin(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()


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
