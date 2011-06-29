import datetime
from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from libs.class_views import JSONResponseMixin
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView, View, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core import exceptions
from django.http import HttpResponse

from courses.models import Course, Semester, Assignment, AssignmentSubmission, Resource
from courses.forms import CourseAdminForm, NewAssignmentForm, SubmitAssignmentForm, TeamSubmitAssignmentForm, NewResourceForm

class CourseOverview(DetailView):
    context_object_name = "course"
    template_name = "courses/overview.html"

    queryset = Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CourseOverview, self).get_context_data(**kwargs)
    
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


class CourseMembers(CourseOverview):
    template_name = "courses/members.html"

# TODO: Check if user is faculty
class CourseAdmin(UpdateView):
    form_class = CourseAdminForm
    template_name = "courses/admin.html"

    queryset = Course.objects.all()

    def get_success_url(self):
        course = self.get_object()
        return reverse('courses:admin', kwargs={'pk':course.id})


class BySemesterList(ListView):
    context_object_name = "courses"
    template_name = "courses/by_semester.html"

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['pk'])
        return self.semester.course_set.all()

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
        return reverse('courses:assignments', kwargs={'pk':course.id})

    def get_context_data(self, **kwargs):
        context = super(NewCourseAssignment, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk = self.kwargs['pk'])
        
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.course = Course.objects.get(pk = self.kwargs['pk'])
        self.object.save()
        return super(NewCourseAssignment, self).form_valid(form)

    # Overriding the dispatch to check permissions
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        course = Course.objects.get(pk = self.kwargs['pk'])

        if request.user not in course.faculty.all():
                raise exceptions.PermissionDenied

        return super(NewCourseAssignment, self).dispatch(request, *args, **kwargs)

class AssignmentList(ListView):
    context_object_name = "assignments"
    template_name = "courses/assignement_list.html"

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return self.course.assignment_set.all()

    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['course'] = self.course
        return context

class AssignmentOverview(DetailView):
    context_object_name = "assignment"
    template_name = "courses/assignment_overview.html"

    queryset = Assignment.objects.all()

    def get_template_names(self):
        return self.template_name
    

    def get_context_data(self, **kwargs):
        context = super(AssignmentOverview, self).get_context_data(**kwargs)
        context['course'] = self.get_object().course

        # Get any submissions the member has submitted
        context['submissions'] = AssignmentSubmission.objects.filter(users = self.request.user, assignment = self.get_object())
    
        return context

    # Overriding the dispatch to check visibility
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        course = self.get_object().course

        if course.private:
            if request.user not in course.faculty.all() and request.user not in course.members.all():
                raise exceptions.PermissionDenied

        return super(AssignmentOverview, self).dispatch(request, *args, **kwargs)

class SubmitAssignment(CreateView):
    model = AssignmentSubmission
    form_class = SubmitAssignmentForm
    template_name = "courses/submit_assignment.html"

    def get_initial(self):
        '''
        Overriding this method to set the assignment id for the form
        '''
        return {'course': self.kwargs['pk']}

    def get_success_url(self):
        assignment = Assignment.objects.get(pk = self.kwargs['pk'])
        return reverse('courses:assignment_overview', kwargs={'pk':assignment.id})

    def get_context_data(self, **kwargs):
        context = super(SubmitAssignment, self).get_context_data(**kwargs)
        context['assignment'] = Assignment.objects.get(pk = self.kwargs['pk'])
        context['course'] = context['assignment'].course

        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.assignment = Assignment.objects.get(pk = self.kwargs['pk'])
        self.object.save()
        self.object.users.add(self.request.user)
        return super(SubmitAssignment, self).form_valid(form)

    # Overriding the dispatch to check permissions
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        self.assignment = Assignment.objects.get(pk = self.kwargs['pk'])

        if request.user not in self.assignment.course.members.all():
                raise exceptions.PermissionDenied

        return super(SubmitAssignment, self).dispatch(request, *args, **kwargs)

class DeleteSubmission(DeleteView):
    template_name = "courses/delete_submission.html"

    queryset = AssignmentSubmission.objects.all()

    def get_success_url(self):
        return reverse('courses:assignment_overview', kwargs={'pk':self.assignment.id})

    def get_context_data(self, **kwargs):
        context = super(DeleteSubmission, self).get_context_data(**kwargs)
        return context

    # Here we set the pk into the kwargs because we're calling this by ajax. We can't reverse the url on the client side because we don't have the id until it's clicked
    def get_object(self, queryset=None):
        self.kwargs['pk'] = self.request.POST.get('id', None)

        # Set the old assignment here so I know where to redirect to
        return super(DeleteSubmission, self).get_object(queryset)

    # Override delete so we save the old object. Return the url to redirect to
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.assignment = self.object.assignment
        self.object.delete()

        return HttpResponse(self.get_success_url())

class TeamSubmitAssignment(SubmitAssignment):
    form_class = TeamSubmitAssignmentForm

    def get_form(self, form_class):
        form = super(TeamSubmitAssignment, self).get_form(form_class)

        form.fields['users'].queryset =  self.assignment.course.members

        return form

class NewCourseResource(CreateView):
    model = Resource
    form_class = NewResourceForm
    template_name = "courses/new_resource.html"

    def get_initial(self):
        '''
        Overriding this method to set the course id for the form
        '''
        return {'course': self.kwargs['pk']}

    def get_success_url(self):
        course = Course.objects.get(pk = self.kwargs['pk'])
        return reverse('courses:resources', kwargs={'pk':course.id})

    def get_context_data(self, **kwargs):
        context = super(NewCourseResource, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk = self.kwargs['pk'])
        
        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.course = Course.objects.get(pk = self.kwargs['pk'])
        self.object.save()
        return super(NewCourseResource, self).form_valid(form)

    # Overriding the dispatch to check permissions
    def dispatch(self, request, *args, **kwargs):
        # set the kwargs so we can get the object
        self.kwargs = kwargs
        course = Course.objects.get(pk = self.kwargs['pk'])

        if request.user not in course.faculty.all():
                raise exceptions.PermissionDenied

        return super(NewCourseResource, self).dispatch(request, *args, **kwargs)

class ResourceList(ListView):
    context_object_name = "resources"
    template_name = "courses/resource_list.html"

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return self.course.resource_set.all()

    def get_context_data(self, **kwargs):
        context = super(ResourceList, self).get_context_data(**kwargs)
        context['course'] = self.course
        return context
