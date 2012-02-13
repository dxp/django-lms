from django import forms
from django.forms import fields, models, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.formtools.wizard import FormWizard
from django.utils.encoding import force_unicode
from alerts.models import Alert

ALERT_CHOICES = (
    ('all', 'All'),
    ('user', 'User'),
    ('group', 'Group')
    )

class AlertForm1(forms.ModelForm):
    class Meta:
        exclude = ('sent_to',)
        model = Alert

class AlertForm2(forms.Form):
    send_to = forms.ChoiceField(widget = forms.RadioSelect, choices = ALERT_CHOICES)


class AlertCreationWizard(FormWizard):
    """
    FormWizard
    """
    @property
    def __name__(self):
        # Python instances don't define __name__ (though functions and classes do).
        # We need to define this, otherwise the call to "update_wrapper" fails:
        return self.__class__.__name__

    def get_template(self, step):
        # Optional: return the template used in rendering this wizard:
        return 'admin/alert_form.html'

    def parse_params(self, request, admin=None, *args, **kwargs):
        # Save the ModelAdmin instance so it's available to other methods:
        self._model_admin = admin
        # The following context variables are expected by the admin
        # "change_form.html" template; Setting them enables stuff like
        # the breadcrumbs to "just work":
        opts = admin.model._meta
        self.extra_context.update({
            'title': 'Add %s' % force_unicode(opts.verbose_name),
            # See http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adding-views-to-admin-sites
            # for why we define this variable.
            'current_app': admin.admin_site.name,
            'has_change_permission': admin.has_change_permission(request),
            'add': True,
            'opts': opts,
            'root_path': admin.admin_site.root_path,
            'app_label': opts.app_label,
        })

    def render_template(self, request, form, previous_fields, step, context=None):
        from django.contrib.admin.helpers import AdminForm
        # Wrap this form in an AdminForm so we get the fieldset stuff:
        form = AdminForm(form, [(
            'Step %d of %d' % (step + 1, self.num_steps()),
            {'fields': form.base_fields.keys()}
            )], {})
        context = context or {}
        context.update({
            'media': self._model_admin.media + form.media
        })
        return super(AlertCreationWizard, self).render_template(request, form, previous_fields, step, context)

    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        # Send alert

        # Display success message and redirect to changelist:
        return self._model_admin.response_add(request, employer)

alert_form = AlertCreationWizard([AlertForm1, AlertForm2])
