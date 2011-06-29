from django import forms
from courses.models import Course, Assignment, AssignmentSubmission, Resource
from django.contrib.auth.models import User

class CourseAdminForm(forms.ModelForm):
    private = forms.ChoiceField(label = "Visibility",
                                choices = ((False, "public"),
                                           (True, "private")),
                                widget = forms.RadioSelect,
                                )

    class Meta:
        model = Course
        fields = ('private',)

class NewAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ('course',)

class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        exclude = ('assignment','users')

class TeamSubmitAssignmentForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset = User.objects.all(),
                                           required = False,
                                           label = 'Team members')
    class Meta:
        model = AssignmentSubmission
        fields = ('users', 'link', 'file', 'notes')

class NewResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = ('course',)
