#
# @license
# Copyright (c) 2020 XGDFalcon®. All Rights Reserved.
#
#
# XGDFalcon LLC retains all intellectual property rights to the code
# distributed as part of the Control Point System Software (CPSS) package.
#

"""
This python module provides...

Written by Larry Latouf (xgdfalcon@gmail.com)
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect 

def manage(request):
    return render(request, 'google-django/manage.html')


def authorize_google(request):
    print("-----------------AUTHORZE------------------")
    token = request.GET
    print(token)
    print("-----------------AUTHORZE------------------")
    return HttpResponseRedirect('/admin/google-django/googleclientoption')

