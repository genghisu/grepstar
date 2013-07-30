"""
Various utilities functions used by django_community and
other apps to perform authentication related tasks.
"""
import json
import hashlib, re
import logging

import django.forms as forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
import django.http as http
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.validators import email_re
     
from django_utils.form_helpers import FormValidator

logger = logging.getLogger('django')

def handle_edit_profile(user, data):
    pass

def get_client_setting_named(name):
    return ClientSetting.objects.get_client_settings()[name]

def get_client_setting_named_length(name):
    return map(int, re.findall(r'\w+', get_client_setting_named(name)))

def is_length_valid(text, client_setting_name):
    setting_length = get_client_setting_named_length(client_setting_name)
    min_length = setting_length[0]
    max_length = setting_length[1]
    length = len(text)
    if length > max_length or length < min_length:
        return False
    else:
        return True

def check_comment(comment):
    errors = []
    if not is_length_valid(comment, 'comment_length'):
        errors.append('INVALID_COMMENT_LENGTH')
    return errors

def check_caption(caption):
    errors = []
    if not is_length_valid(caption, 'caption_length'):
        errors.append('INVALID_CAPTION_LENGTH')
    return errors

def check_username(username):
    errors = []
    if not is_length_valid(username, 'username_length'):
        errors.append('INVALID_USERNAME_LENGTH')
    elif not FormValidator.validate_username(username):
        errors.append('INVALID_USERNAME')
    else:
        try:
            user = User.objects.get(username__iexact = username)
            errors.append('USERNAME_UNAVAILABLE')
        except ObjectDoesNotExist:
            pass
    
    return errors

def check_password(password):
    errors = []
    if not is_length_valid(password, 'password_length'):
        errors.append('INVALID_PASSWORD_LENGTH')
    return errors

def check_email(email):
    errors = []
    if not email_re.match(email):
        errors.append('INVALID_EMAIL')
    else:
        try:
            User.objects.get(email__iexact = email)
            errors.append('EMAIL_UNAVAILABLE')
        except ObjectDoesNotExist:
            pass
        
    return errors

def check_firstname(firstname):
    errors = []
    if not is_length_valid(firstname, 'first_name_length'):
        errors.append('INVALID_FIRSTNAME_LENGTH')
    return errors

def check_lastname(lastname):
    errors = []
    if not is_length_valid(lastname, 'last_name_length'):
        errors.append('INVALID_LASTNAME_LENGTH')
    return errors

def check_aboutme(aboutme):
    errors = []
    if not is_length_valid(aboutme, 'about_me_length'):
        errors.append('INVALID_ABOUTME_LENGTH')
    return errors

def check_website(website):
    errors = []
    if not is_length_valid(website, 'website_length'):
        errors.append('INVALID_WEBSITE_LENGTH')
    return errors

def check_age_verified(age_verified):
    errors = []
    if not age_verified:
        print 'age_verified %s' % (age_verified)
        errors.append('AGE_UNVERIFIED')
    return errors

def check_login(data):
    errors = []
    
    try:
        name = data['username'].replace(' ', '')
        password = data['password']
        user = None
        try:
            user = User.objects.get(username__iexact = name)
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(email__iexact = name)
            except ObjectDoesNotExist:
                errors.append('INVALID_LOGIN_CREDENTIALS')
        if user and not user.check_password(password):
            errors.append('INVALID_LOGIN_CREDENTIALS')
    except KeyError:
        errors.append('INCOMPLETE_DATA')
    
    return errors

def handle_login(request, data):
    """
    Login for user
    """
    user_id = data.get('username', None)
    if user_id:
        user_id = user_id.replace(' ', '')

    if email_re.match(user_id):
        try:
            target_user = User.objects.get(email__iexact = user_id)
        except ObjectDoesNotExist:
            target_user = None
    else:
        try:
            target_user = User.objects.get(username__iexact = user_id)
        except ObjectDoesNotExist:
            target_user = None
    
    if target_user:
        user = authenticate(username = target_user.username,
                                password = data.get('password', None))
        user_object = target_user
    else:
        user = None
        
    if user is not None:
        login(request, user)
    return user

def check_registration(data):
    errors = []
    
    try:
        username = data['username'].strip()
        firstname = data.get('firstname', '').strip()
        lastname = data.get('lastname', '').strip()
        pw1 = data['password']
        email = data['email'].strip()
    except KeyError:
        errors.append('INCOMPLETE_DATA')
    
    if not errors:
        errors.extend(check_username(username))
        errors.extend(check_password(pw1))
        errors.extend(check_email(email))
        errors.extend(check_firstname(firstname))
        errors.extend(check_lastname(lastname))
            
    return errors
    
def handle_registration(request,  data):
    """
    Signs a user up based on form data from django_community.SignupForm.
    """
    
    username = data.get('username', None).strip()
    email = data.get('email', None).strip()
    password = data.get('password', None)
    firstname = data.get('firstname', '').strip()
    lastname = data.get('lastname', '').strip()
    try:
        age_verified = bool(int(data.get('age_verified', '0').strip()))
    except Exception, e:
        age_verified = False
    
    try:
        user = User.objects.get(username = username,  email = email)
    except ObjectDoesNotExist:
        user = User(username = username,  
                    email = email,
                    first_name = firstname,
                    last_name = lastname)
        user.save()
        user.set_password(password)
        user.save()

        from core.models import UserProfile
        user_profile = UserProfile.objects.get_user_profile(user)
        user_profile.is_age_verified = age_verified
        user_profile.save()
    
    user = authenticate(username = username, password = password)
    login(request, user)
    return user

def handle_signout(request):
    """
    Log out.
    """
    auth_logout(request)
