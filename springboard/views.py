from django_utils import render_to_response
from django.views.generic import TemplateView

class SpringBoard(TemplateView):
    template_name = "springboard/springboard.html"
