from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django import forms

from django.conf import settings
from user.models import *
import json

# Create your views here.
def my_login_required(function):
    def wrapper(request, *args, **kw):
        user = request.user
        print "USER : " +str(user)

        if not (request.user and request.user.is_authenticated()):
            return JsonResponse({"redirect": settings.LOGIN_URL})

        else:
            return function(request, *args, **kw)
    return wrapper


def UserLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print "LOGGING IN : " + str(user)

        redirect = request.POST['redirect']
        if user is not None:
            if user.is_active:
                login(request, user)

                if redirect != "":
                    return HttpResponseRedirect("http://" + request.META['HTTP_HOST'] + redirect)
                else:
                    return HttpResponseRedirect("/profile")
                # Redirect to a success page.
            else:
                pass
                # Return a 'disabled account' error message
        else:
            return HttpResponseRedirect(reverse('user:login'))


def UserLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

