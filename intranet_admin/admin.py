from django.utils.translation import ugettext as _
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField

class AdmissionsAdminForm(ModelForm):
    groups = ModelMultipleChoiceField(queryset = Group.objects.exclude(name = 'Admissions'))
    class Meta:
        model = User

class MyUserAdmin(UserAdmin):
    staff_fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        # No permissions
        (_('Groups'), {'fields': ('groups',)}),
    )

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if 'Admissions' in request.user.groups and not request.user.is_superuser:
            self.form = AdmissionsAdminForm
            try:
                self.fieldsets = self.staff_fieldsets
                response = UserAdmin.change_view(self, request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
            return response
        else:
            return UserAdmin.change_view(self, request, *args, **kwargs)


admin.site.unregister(User)
 
admin.site.register(User, MyUserAdmin)

