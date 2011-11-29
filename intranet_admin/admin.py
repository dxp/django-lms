from django.utils.translation import ugettext as _
from django.contrib import admin
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple

from permission_backend_nonrel.admin import NonrelPermissionCustomUserAdmin, NonrelPermissionUserForm
from permission_backend_nonrel.models import UserPermissionList, GroupPermissionList
class MyUserAdminForm(NonrelPermissionUserForm):
    def __init__(self, *args, **kwargs):
        super(NonrelPermissionUserForm, self).__init__(*args, **kwargs)
	# We pretty much need to override everything to set the widgets
	self.fields['user_permissions'] = forms.MultipleChoiceField(required=False, widget=FilteredSelectMultiple("Permission", False))
        self.fields['groups'] = forms.MultipleChoiceField(required=False, widget=FilteredSelectMultiple("Groups", False))
        
        permissions_objs = Permission.objects.all().order_by('name')
        choices = []
        for perm_obj in permissions_objs:
            choices.append([perm_obj.id, perm_obj.name])
        self.fields['user_permissions'].choices = choices
        
        group_objs = Group.objects.all()
        choices = []
        for group_obj in group_objs:
            choices.append([group_obj.id, group_obj.name])
        self.fields['groups'].choices = choices

        try:
            user_perm_list = UserPermissionList.objects.get(
                user=kwargs['instance'])
            self.fields['user_permissions'].initial = user_perm_list.permission_fk_list
            self.fields['groups'].initial = user_perm_list.group_fk_list
        except (UserPermissionList.DoesNotExist, KeyError):
            self.fields['user_permissions'].initial = list()
            self.fields['groups'].initial = list()
	    #groups = ModelMultipleChoiceField(queryset = Group.objects.exclude(name = 'Admissions'))

class AdmissionsAdminForm(MyUserAdminForm):
	pass

class MyUserAdmin(NonrelPermissionCustomUserAdmin):
    staff_fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        # No permissions
        (_('Groups'), {'fields': ('groups',)}),
    )

    def change_view(self, request, *args, **kwargs):
        try:
            group, created = Group.objects.get_or_create(name = 'Admissions')
            user_perm_list = UserPermissionList.objects.get(
                user=request.user
                )
        except UserPermissionList.DoesNotExist:
            groups = list()

	
        self.form = MyUserAdminForm

        # for non-superuser
        if not request.user.is_superuser and request.user.has_perm('auth.change_users') and group.id in user_perm_list.group_fk_list:
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

