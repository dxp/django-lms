import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from libs.class_views import JSONResponseMixin
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView, View
from django.views.generic.detail import SingleObjectMixin
from django.core import exceptions

from courses.models import Course, Semester, Assignment
from courses.forms import CourseAdminForm, NewAssignmentForm

class CourseOverview(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CourseOverview, self).get_context_data(**kwargs)
        context['request'] = self.request
    
        # Check if user is a member
        context['is_member'] = self.request.user in context['course'].members.all()
        
        return context

    # Overriding the dispatch to check visibility
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        course = self.get_object()

        if course.private:
            if request.user not in course.faculty.all() and request.user not in course.members.all():
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

class ToggleMembership(View, SingleObjectMixin, JSONResponseMixin):
    queryset = Course.objects.all()
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user in self.object.members.all():
            self.object.members.remove(request.user)
            status = "removed"
        else:
            self.object.members.add(request.user)
            status = "added"
        context = {'status':status}
        return self.render_to_response(context)

class NewCourseAssignment(CreateView):
    model = Assignment
    form_class = NewAssignmentForm
    template_name = "courses/new_assignment.html"

    def get_initial(self):
        '''
        Overriding this method to set the course id for the form
        '''
        return {'course': self.kwargs['pk']}

    def get_success_url(self):
        course = Course.objects.get(pk = self.kwargs['pk'])
        return reverse('courses:overview', kwargs={'pk':course.id})

    def get_context_data(self, **kwargs):
        context = super(NewCourseAssignment, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['course'] = Course.objects.get(pk = self.kwargs['pk'])
        
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.course = Course.objects.get(pk = self.kwargs['pk'])
        self.object.save()
        return super(NewCourseAssignment, self).form_valid(form)
