from django.http.response import HttpResponse
from django.shortcuts import redirect



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper_func