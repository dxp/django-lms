from django_utils import render_to_response
from django.views.generic import DetailView
from courses.models import Course

class CourseOverview(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()
