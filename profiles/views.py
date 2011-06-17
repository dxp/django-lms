from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from django.views.generic.edit import FormView
from django.core import exceptions

from profiles.models import Profile
#from courses.forms import CourseAdminForm, NewAssignmentForm, SubmitAssignmentForm, TeamSubmitAssignmentForm

class ProfileEdit(FormView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"


    def get_success_url(self):
        profile = self.get_object()
        return reverse('profiles:detail', kwargs={'username':profile.user.username})

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
