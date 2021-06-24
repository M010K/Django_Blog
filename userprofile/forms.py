from django import forms

from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    """
    form for user login
    """
    username = forms.CharField()
    password = forms.CharField()
