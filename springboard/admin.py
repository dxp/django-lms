from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from springboard.models import IntranetApplication

class IntranetApplicationAdminForm(forms.ModelForm):
    groups = forms.MultipleChoiceField(required = False, widget = FilteredSelectMultiple("Groups", False))

    def __init__(self, *args, **kwargs):
        super(IntranetApplicationAdminForm, self).__init__(*args, **kwargs)

        group_objs = Group.objects.all()
        choices = []
        for group_obj in group_objs:
            choices.append([group_obj.id, group_obj.name])
        self.fields['groups'].choices = choices

        try:
            self.fields['groups'].initial = kwargs['instance'].groups
        except KeyError:
            self.fields['groups'].initial = list()


    class Meta:
        model = IntranetApplication
        exclude = ('groups',)

class IntranetApplicationAdmin(admin.ModelAdmin):
    form = IntranetApplicationAdminForm

    def save_model(self, request, obj, form, change):
        super(IntranetApplicationAdmin, self).save_model(request, obj, form, change)
        try:
            if len(form.cleaned_data["groups"]) > 0:
                obj.groups = form.cleaned_data["groups"]
                obj.save()
        except KeyError:
            pass

    

admin.site.register(IntranetApplication, IntranetApplicationAdmin)
