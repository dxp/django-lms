from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple

from courses.models import Course, Semester, Assignment, AssignmentSubmission, Resource

class CourseAdminForm(ModelForm):
    faculty = ModelMultipleChoiceField(queryset = Group.objects.get_or_create(name = 'Faculty')[0].user_set.all(),
                                       required = False,
                                       widget = FilteredSelectMultiple("Faculty", False) )
    class Meta:
        model = Course

class CourseAdmin(admin.ModelAdmin):
     list_filter = ('semester',)
     filter_horizontal = ('faculty',)
     form = CourseAdminForm

admin.site.register(Course, CourseAdmin)
admin.site.register(Semester)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Resource)
