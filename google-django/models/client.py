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

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.db.models import signals
import uuid
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

GOOGLE_AUTH_LINK = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_CALENDAR_SCOPE = "https://www.googleapis.com/auth/admin.directory.resource.calendar"
# GOOGLE_AUTH="https://accounts.google.com/signin/oauth/oauthchooseaccount?client_id=''&destination=https%3A%2F%2Fadmin.controlpointsw.com&approval_state=!ChQ4NkdiZHdWcEgxOS1sRE1BdVJlehIfSTNhRy1fUFM5QW9SWUlreWNoTjIyM1Q4RnEwVi1oWQ%E2%88%99AJDr988AAAAAXh5WUS-7iTCenpjKAU8VwbnMKhLCSdCa&oauthgdpr=1&xsrfsig=ChkAeAh8T2qp-1zOUTTOXXK2CfjE4X9ql2CYEg5hcHByb3ZhbF9zdGF0ZRILZGVzdGluYXRpb24SBXNvYWN1Eg9vYXV0aHJpc2t5c2NvcGU&flowName=GeneralOAuthFlow"

class GoogleClientManager(models.Manager):
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class GoogleClientType(models.Model):
    id = models.UUIDField(verbose_name=_("ID"), primary_key=True,
                          default=uuid.uuid4, editable=False)
    google_access_token = models.CharField(
        verbose_name=_("Google Access Token"), max_length=100, default="")
    google_refresh_token = models.CharField(
        verbose_name=_("Google Refresh Token"), max_length=100, default="")
    google_client_id = models.CharField(
        verbose_name=_("Google Client ID"), max_length=100, default="")
    google_client_secret = models.CharField(
        verbose_name=_("Google Client Secret"), max_length=100, default="")
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, null=True, verbose_name=_('Site'), blank=True)

    class Meta:
        abstract = True


class GoogleClientOption(GoogleClientType):
    objects = GoogleClientManager()

    class Meta:
        db_table = 'cpss_google_settings'
        verbose_name = _('CPSS Google Client Setting')
        verbose_name_plural = _('CPSS Google Client Settings')

    def __str__(self):
        return str(self.site.domain) + ": " + str(self.google_client_id)

    def _calendar_client(self):
        credentials = self._get_credentials()
        return build(
            "calendar", "v3",
            credentials=credentials,
            cache_discovery=False
        )

    def _get_credentials(self):

        return Credentials(
            token=self.google_access_token,
            refresh_token=self.google_refresh_token,
            token_uri="https://accounts.google.com/o/oauth2/token",
            client_id=self.google_client_id,
            client_secret=self.google_client_secret,
        )

    def get_calendar_events(self, calendar_id):
        return (
            self._calendar_client().events()
            .list(
                calendarId=calendar_id,
                maxResults=100,
            )
            .execute()
        )

        
    def authorize(self, token):
        from google.oauth2 import id_token
        from google.auth.transport import requests
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.google_client_id)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
        except ValueError:
            # Invalid token
            pass
        
        return Credentials(
            token=self.google_access_token,
            refresh_token=self.google_refresh_token,
            token_uri="https://accounts.google.com/o/oauth2/token",
            client_id=self.google_client_id,
            client_secret=self.google_client_secret,
        )

class GoogleCalendarManager(models.Manager):
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class GoogleCalendar(models.Model):
    google_calendar_id = models.CharField(max_length=255, primary_key=True)
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    google_calendar_integration = models.ForeignKey(GoogleClientOption,
                                                    models.CASCADE,
                                                    related_name='calendar'
                                                    )
    updated_at = models.DateTimeField(auto_now=True)

    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, null=True, verbose_name=_('Site'), blank=True)

    objects = GoogleCalendarManager()

    def __str__(self):
        return self.summary


class GoogleEventManager(models.Manager):
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class GoogleEvent(models.Model):
    iCalUID = models.CharField(verbose_name=_("ID"), primary_key=True, max_length=100,
                               default=uuid.uuid4, editable=False)
    summary = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    location = models.CharField(max_length=255, blank=True)
    timeZone = models.CharField(max_length=255, blank=True)

    google_calendar_id = models.ForeignKey(
        GoogleCalendar, on_delete=models.CASCADE, null=True, verbose_name=_('GoogleCalendar'), blank=True)

    google_calendar_event_id = models.CharField(max_length=255, blank=True)
    google_calendar_event_etag = models.CharField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GoogleEventManager()

    def __str__(self):
        return self.summary
