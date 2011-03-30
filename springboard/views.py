from django_utils import render_to_response
from django.views.generic import ListView
from springboard.models import IntranetApplication
from django.contrib.auth.decorators import login_required

class SpringBoard(ListView):

    context_object_name = "applications"
    template_name = "springboard/springboard.html"

    def get_queryset(self):
        # Check the groups the user is allowed to see
        applications = []
        for group in self.request.user.groups.all():
            applications = applications or group.intranetapplication_set.all()

        return applications
