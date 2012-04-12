from django import http
from django.utils import simplejson as json

from breadcrumbs import Breadcrumb, Breadcrumbs

class BreadCrumbMixin(object):
    def __init__(self, *args, **kwargs):
        self.breadcrumbs = getattr(self, 'breadcrumbs', False)

        if not self.breadcrumbs:
            self.breadcrumbs = Breadcrumbs()

        return super(BreadCrumbMixin, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Give the breadcrumbs the current page
        """
        self.breadcrumbs.append(Breadcrumb(self.name, '#'))
        return super(BreadCrumbMixin, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Adds the breadcrumbs to the render
        """
        context.update({'breadcrumbs':self.breadcrumbs})
        return super(BreadCrumbMixin, self).render_to_response(context, **response_kwargs)

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)
