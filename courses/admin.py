from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from permission_backend_nonrel.models import UserPermissionList

from courses.models import Course, Semester, Assignment, AssignmentSubmission, Resource


class CourseAdminForm(ModelForm):
    faculty = ModelMultipleChoiceField(queryset = User.objects.none(),
                                       required = False,
                                       widget = FilteredSelectMultiple("Faculty", False) )
    members = ModelMultipleChoiceField(queryset = User.objects.none(),
                                       required = False,
                                       widget = FilteredSelectMultiple("Faculty", False) )

    def __init__(self,*args,**kwargs):
        super (CourseAdminForm,self ).__init__(*args,**kwargs)
        faculty_group = Group.objects.get_or_create(name = 'Faculty')[0]
        faculty_list = UserPermissionList.objects.filter(group_fk_list = faculty_group.pk)
        #print User.objects.filter(pk__in = [faculty.user.pk for faculty in faculty_list]).filter(pk__in = [u'4eaef5d7bb6933592e000010'])
        self.fields['faculty'].queryset = User.objects.filter(pk__in = [faculty.user.pk for faculty in faculty_list])
        #self.fields['client'].queryset = Client.objects.filter(company=company)

    class Meta:
        model = Course
        exclude = ('faculty', 'members')

class CourseAdmin(admin.ModelAdmin):
     list_filter = ('semester',)
     #filter_horizontal = ('faculty',)
     form = CourseAdminForm

admin.site.register(Course, CourseAdmin)
#admin.site.register(Semester)
#admin.site.register(Assignment)
#admin.site.register(AssignmentSubmission)
#admin.site.register(Resource)
