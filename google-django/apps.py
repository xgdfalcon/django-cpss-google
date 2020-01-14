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

from django.apps import AppConfig

class CPSSGoogleConfig(AppConfig):
    name = 'google-django'
    verbose_name = "CPSS Google - Django"

    def ready(self):
    	from .signals import authorize_google
