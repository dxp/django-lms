from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def course_menu_active(context, url):
    print reverse(url, kwargs={'pk': context['course'].id})
    if context['request'].path in reverse(url, kwargs={'pk': context['course'].id}):
        return "selected"
    return ""
