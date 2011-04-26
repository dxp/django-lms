from django import forms
from courses.models import Course

class CourseAdminForm(forms.ModelForm):
    private = forms.ChoiceField(label = "Visibility",
                                choices = ((False, "public"),
                                           (True, "private")),
                                widget = forms.RadioSelect,
                                )

    class Meta:
        model = Course
        fields = ('private',)
