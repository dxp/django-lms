# Yay monkey patching
from permission_backend_nonrel.models import UserPermissionList, GroupPermissionList
from django.contrib.auth.models import Group

def get_groups(self):
    user_perm_list = UserPermissionList.objects.get(user = self)
    
    groups = Group.objects.filter(id__in = user_perm_list.group_fk_list)
    return groups

from django.contrib.auth.models import User

User.add_to_class('group_list', property(get_groups))
