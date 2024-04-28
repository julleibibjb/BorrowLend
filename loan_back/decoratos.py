from django.http import HttpResponse
from django.shortcuts import redirect


def staff_member_required(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_staff:
            return view_func(request,*args,**kwargs)
        return redirect("/")
    return wrapper_func