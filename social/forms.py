from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from social.models import UserProfile


class RegistrationForm(UserCreationForm):#reg form have to create a us nd pass
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class LoginForm(forms.Form):   #inherit from forms

    username=forms.CharField()
    password=forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following","block")