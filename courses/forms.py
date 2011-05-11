from django import forms
from courses.models import Course, Assignment, AssignmentSubmission

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
        exclude = ('assignment','user')
