from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import FormView,CreateView
from social.forms import RegistrationForm,LoginForm
# Create your views here.

class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self) -> str:
        return reverse("signup")


