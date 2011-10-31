from django.utils.translation import ugettext as _
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField

from permission_backend_nonrel.admin import NonrelPermissionCustomUserAdmin, NonrelPermissionUserForm

class AdmissionsAdminForm(NonrelPermissionUserForm):
	pass
	#groups = ModelMultipleChoiceField(queryset = Group.objects.exclude(name = 'Admissions'))

class MyUserAdmin(NonrelPermissionCustomUserAdmin):
    staff_fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        # No permissions
        (_('Groups'), {'fields': ('groups',)}),
    )

    def change_view(self, request, *args, **kwargs):
	content_type = ContentType.objects.get_for_model(User)
        perm, created = Permission.objects.get_or_create(name='change_users',
                                         content_type=content_type,
                                         codename='change_users')

        # for non-superuser
        if not request.user.is_superuser and request.user.has_perm('auth.change_users'):
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

