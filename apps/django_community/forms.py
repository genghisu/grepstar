import hashlib
import re

from django.conf import settings
import django.forms as forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.contrib.auth.models import User

from django_utils.form_helpers import DivForm,  DynamicRequestForm, FormValidator
import django_utils.form_widgets as widgets
from django_utils import request_helpers
import django_community.models
import django_community.utils

class LoginForm(DivForm):
    """
    Form used to authenticate users to the site.
    """
    username = forms.CharField(max_length = 30,  
                               min_length = 2,  
                               required = True,  
                               label = 'Username or email',  
                               widget = widgets.StandardCharfield(attrs={'class':'required'}))
    password = forms.CharField(min_length = 3,  
                               label = 'Password',  
                               widget = widgets.StandardPassfield(attrs={'class':'required'}))
    
    def clean(self):
        result = super(LoginForm,  self).clean()
        if django_community.utils.check_login(self.cleaned_data):
            raise forms.ValidationError("You have entered an invalid username and password combination.")
        return result
    
class SignupForm(DivForm):
    """
    Form which allows users to sign up for the site.
    """
    username = forms.CharField(max_length = 30,  min_length = 2,  required = True,  label = 'Username:',  
                               widget = widgets.StandardCharfield(attrs={'class':'required',  'minlength':'3'}))
    email = forms.EmailField(label = 'Email:',  widget = widgets.StandardCharfield(attrs={'class':'required email'}))
    firstname = forms.CharField(max_length = 30, min_length = 1, required = False, label = 'First Name:',
                                widget = widgets.StandardCharfield(attrs={'class':'required',  'minlength':'2'}))
    lastname = forms.CharField(max_length = 30, min_length = 1, required = False, label = 'Last Name:',
                                widget = widgets.StandardCharfield(attrs={'class':'required',  'minlength':'2'}))
    password = forms.CharField(min_length = 3,  label = 'Password:',  
                               widget = widgets.StandardPassfield(attrs={'class':'required'}))
    password_confirmation = forms.CharField(min_length = 3,  label = 'Password Confirmation:',  
                                            widget = widgets.StandardPassfield(attrs={'class':'required'}))
    
    def clean_username(self):
        name = self.cleaned_data['username']
        if not FormValidator.validate_username(name):
            raise forms.ValidationError("That username include invalid characters. Use letters, numbers and underscore.")
        elif len(name) > 30 or len(name) <= 3:
            raise forms.ValidationERror("Usernames have to be less than 30 characters and at least 3 characters in length.")
        else:
            try:
                User.objects.get(username = name)
                raise forms.ValidationError("That username has already been taken.")
            except ObjectDoesNotExist:
                pass
        return name
    
    def clean_password_confirmation(self):
        pw1 = self.cleaned_data['password']
        pw2 = self.cleaned_data['password_confirmation']
        if not pw1 == pw2:
            raise forms.ValidationError("Password confirmation does not match password.")
        return pw2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
            raise forms.ValidationError("There is already an user with this email address.")
        except ObjectDoesNotExist:
            pass
        return email

def build_edit_profile_form(user):
    """
    Returns an EditProfileForm which lets users edit their profiles.
    """
    profile = user.profile
    
    base_fields = {'display_name':  forms.CharField(max_length = 70,  min_length = 3,  required = False,  label = 'Display Name',  
                        initial = profile.display_name, 
                       widget = widgets.StandardCharfield(attrs={})) , 
                       'email': forms.EmailField(max_length = 200,  min_length = 5,  required = False,  label = 'Email', 
                        initial = user.email, 
                        widget = widgets.StandardCharfield(attrs={})), 
                        'first_name':  forms.CharField(max_length = 70,  required = False,  label = 'First Name',  
                            initial = user.first_name, 
                           widget = widgets.StandardCharfield(attrs={})) , 
                       'last_name':  forms.CharField(max_length = 70,  required = False,  label = 'Last Name',  
                            initial = user.last_name, 
                           widget = widgets.StandardCharfield(attrs={})) , 
                        'about_me':  forms.CharField(max_length = 500,  required = False,  label = 'About Me',  
                            initial = profile.about_me, 
                           widget = widgets.BigTextarea(attrs={})) , 
                       }
    
    def clean_display_name(self):
        display_name = self.cleaned_data['display_name']
        logged_user = self.request.user
        try:
            profile = django_community.models.UserProfile.objects.get(display_name = display_name)
            if not profile.user.pk == logged_user.pk:
                raise forms.ValidationError("That display name has already been taken.")
        except ObjectDoesNotExist:
            pass
        return display_name
         
    EditProfileForm = type('EditProfileForm',  (DynamicRequestForm, ),  base_fields)
    EditProfileForm.clean_display_name = clean_display_name
    return EditProfileForm
