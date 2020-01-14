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

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models.client import GoogleClientOption
import requests
import uuid 

@receiver(post_save, sender=GoogleClientOption) 
def authorize_google(sender, instance, signal, *args, **kwargs):
    SCOPE = "https://www.googleapis.com/auth/admin.directory.resource.calendar"
    GOOGLE_AUTH_LINK="https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id="+str(instance.google_client_id)+"&flowName=GeneralOAuthFlow&redirect_uri=http://localhost:8000/google/auth&scope="+SCOPE
    # GOOGLE_AUTH_LINK = "https://accounts.google.com/signin/oauth"
    # GOOGLE_CALENDAR_SCOPE = "https://www.googleapis.com/auth/admin.directory.resource.calendar"
    # appstate = str(uuid.uuid4())
    # dest = "http://localhost:8000/google/auth"
    # reqstring = GOOGLE_AUTH_LINK+'?client_id='+ str(instance.google_client_id) + "&scope=email,calendar&destination="+dest+"&approval_state="+appstate
    print (GOOGLE_AUTH_LINK)
    LINK="https://accounts.google.com/o/oauth2/auth?redirect_uri=storagerelay%3A%2F%2Fhttps%localhost:8000%3Fgoogle%3Dauth893348&response_type=permission%20id_token&scope=email%20profile%20openid&openid.realm=&client_id=492221255156-trnduui8j31i06ovaaipjjav4340v69l.apps.googleusercontent.com&ss_domain=http%3A%2F%localhost&fetch_basic_profile=true&gsiwebsdk=2"
    r = requests.get(GOOGLE_AUTH_LINK)
    print(r)