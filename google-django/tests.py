#
# @license
# Copyright (c) 2020 XGDFalcon®. All Rights Reserved.
#
#
# XGDFalcon LLC retains all intellectual property rights to the code
# distributed as part of the Control Point System Software (CPSS) package.
# 

"""
This python module provides the models for the video vault application.

Written by Larry Latouf (xgdfalcon@gmail.com)
"""

from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import RequestFactory
from .models.client import GoogleClientOption
from datetime import datetime
import os

GOOGLE_ACCESS_TOKEN = os.environ['GOOGLE_ACCESS_TOKEN'] 
GOOGLE_REFRESH_TOKEN = os.environ['GOOGLE_REFRESH_TOKEN'] 
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID'] 
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET'] 

GOOGLE_CALENDAR_ID = os.environ['GOOGLE_CALENDAR_ID'] 
TEST_DOMAIN = os.environ['TEST_DOMAIN'] 

class GoogleDjangoTestCase(TestCase):
    def setUp(self):
        Site.objects.create(
            domain=TEST_DOMAIN,
            name="Test Domain")

        site = Site.objects.get(domain=TEST_DOMAIN)
        GoogleClientOption.objects.create(
            google_access_token=GOOGLE_ACCESS_TOKEN,
            google_refresh_token=GOOGLE_REFRESH_TOKEN,
            google_client_id=GOOGLE_CLIENT_ID,
            google_client_secret=GOOGLE_CLIENT_SECRET,
            site=site)



    def test_calendar_events(self):
        site = Site.objects.get(domain=TEST_DOMAIN)
        collection = GoogleClientOption.objects.get(site=site)
        result = collection.get_calendar_events(GOOGLE_CALENDAR_ID)
        print(result)

