from django import template
from django.template import resolve_variable
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag(takes_context=True)
def course_menu_active(context, url):
    if reverse(url, kwargs={'pk': context['course'].id}) in context['request'].path:
        return "selected"
    return ""

@register.tag()
def iffaculty(parser, token):
    """ Check to see if the currently logged in user is faculty

    """
    nodelist = parser.parse(('endiffaculty',))
    parser.delete_first_token()
    return FacultyCheckNode(nodelist)


class FacultyCheckNode(template.Node):
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
        if group in user.group_list:
            return self.nodelist.render(context)
        return ''

@register.tag()
def ifcoursefaculty(parser, token):
    """
    Check to see if the currently logged in user is faculty for this course
    """

    # Default nodelist_false so we don't get and error
    nodelist_false = None
    nodelist_true = parser.parse(['else', 'endifcoursefaculty'])

    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(['endifcoursefaculty'])
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return FacultyCourseCheckNode(nodelist_true, nodelist_false)


class FacultyCourseCheckNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        
    def render(self, context):
        user = resolve_variable('user', context)
        course = resolve_variable('course', context)
        group, created = Group.objects.get_or_create(name='Faculty')

        if user.is_authenticated:
            # Not sure if we should be checking for group. Hmmm
            if group in user.group_list:
                if user in course.faculty:
                    return self.nodelist_true.render(context)

        if self.nodelist_false:
            return self.nodelist_false.render(context)
        else:
            return ''

@register.tag()
def ifcoursemember(parser, token):
    """
    Simple check if user is a member of the course

    """
    nodelist = parser.parse(('endifcoursemember',))
    parser.delete_first_token()
    return MemberCheckNode(nodelist)




@register.tag()
def ifpossiblemember(parser, token):
    """
    Check to see if the current user can be a member of the course.
    This is seperate from just being 'is student' because there is possible expansion to TAs, research fellows, etc.

    """
    nodelist = parser.parse(('endifpossiblemember',))
    parser.delete_first_token()
    return PossibleMemberCheckNode(nodelist)


class PossibleMemberCheckNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        user = resolve_variable('user', context)
        course = resolve_variable('course', context)
        if not user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name='Student')
        except Group.DoesNotExist:
            return ''
        if group in user.group_list:
            return self.nodelist.render(context)
        return ''



class MemberCheckNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        request = resolve_variable('request', context)
        course = resolve_variable('course', context)
        if not request.user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name='Student')
        except Group.DoesNotExist:
            return ''
        if request.user in course.members:
            return self.nodelist.render(context)
        return ''
