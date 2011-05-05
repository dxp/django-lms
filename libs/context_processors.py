from django.conf import settings as django_settings

def settings(request):
    return {'TYPEKIT_URL':django_settings.TYPEKIT_URL}
