from django.conf import settings
from django.http import HttpResponseRedirect

DEFAULT_REDIRECT_PATH = getattr(settings, 'DEFAUTL_REDIRECT_URL','https://diminuative.herokuapp.com/')

def wildcard_redirect(request, path=None):
    new_url = DEFAULT_REDIRECT_PATH
    if path is not None:
        new_url += '/' + path
    return HttpResponseRedirect(new_url)

