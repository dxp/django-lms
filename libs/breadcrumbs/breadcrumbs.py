"""
Classes to add request.breadcrumbs as one class to have a list of breadcrumbs
TODO: maybe is better to move to contrib/breadcrumbs
"""

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils.text import force_unicode 
import sys

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

class Breadcrumbs(Singleton, list):
    pass

class Breadcrumb(object):
    """
    Breadcrumb can have methods to customize breadcrumb object, Breadcrumbs
    class send to us name and url.
    """
    def __init__(self,name,url):
        # HERE
        #
        # If I don't use force_unicode, always runs ok, but have problems on
        # template with unicode text
        self.name = name
        self.url = url

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s,%s" % (self.name,self.url)

    def __repr__(self):
        return u"Breadcrumb <%s,%s>" % (self.name,self.url)
