from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

def unautenticate_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('management:index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('point_of_sale:index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
