from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from libs.django_utils import render_to_response
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.core import exceptions
from django.contrib.auth.models import User

from profiles.models import Profile
from profiles.forms import ProfileForm
#from courses.forms import CourseAdminForm, NewAssignmentForm, SubmitAssignmentForm, TeamSubmitAssignmentForm

class ProfileEdit(FormView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"

    def form_valid(self, form):
        profile = self.get_profile()
        form.save(profile)
        return super(ProfileEdit, self).form_valid(form)

    def get_success_url(self):
        profile = self.get_profile()
        return reverse('profiles:detail', kwargs={'username':profile.user.username})

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def get_profile(self):
        return Profile.objects.get(user = self.request.user)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        profile = self.get_profile()
        self.initial = {'mugshot': profile.mugshot,
                   'resume': profile.resume,
                   'biography': profile.data.get('biography', ''),}
        return self.initial


class ProfileDetail(DetailView):
    template_name = "profiles/detail.html"
    context_object_name = "profile"

    def get_object(self):
        username = self.kwargs.get('username', None)

        profile = Profile.objects.get(user = User.objects.get(username = username))
        return profile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
