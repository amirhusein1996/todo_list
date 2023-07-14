from django.shortcuts import redirect
from django.conf import settings


def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper