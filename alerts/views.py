from django.views.generic import ListView

from alerts.models import Alert

class AlertList(ListView):
    context_object_name = "alerts"
    template_name = "alerts/list.html"

    def get_queryset(self):
        return Alert.objects.filter(sent_to = self.request.user)


