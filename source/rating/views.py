# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.
def rating (request):
    return HttpResponse ('This is rating')