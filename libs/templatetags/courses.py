from django import template
from django.template import resolve_variable
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag(takes_context=True)
def course_menu_active(context, url):
    print reverse(url, kwargs={'pk': context['course'].id})
    if context['request'].path in reverse(url, kwargs={'pk': context['course'].id}):
        return "selected"
    return ""

@register.simple_tag(takes_context=True)
def course_menu_active(context, url):
    print reverse(url, kwargs={'pk': context['course'].id})
    if context['request'].path in reverse(url, kwargs={'pk': context['course'].id}):
        return "selected"
    return ""

@register.tag()
def iffaculty(parser, token):
    """ Check to see if the currently logged in user is faculty

    """
    nodelist = parser.parse(('endiffaculty',))
    parser.delete_first_token()
    return GroupCheckNode(nodelist)


class GroupCheckNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        user = resolve_variable('user', context)
        if not user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name='Faculty')
        except Group.DoesNotExist:
            return ''
        if group in user.groups.all():
            return self.nodelist.render(context)
        return ''
