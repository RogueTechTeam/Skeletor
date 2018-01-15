from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden
import requests

from home.models import *
import os
from user.views import my_login_required

