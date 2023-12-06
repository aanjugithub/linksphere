from django.shortcuts import render,redirect
from django.urls import reverse

from django.views.generic import FormView,CreateView,TemplateView,View
from social.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self) -> str:
        return reverse("signin")

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("logged in successfully..........")
                return redirect("index")
            
        print("error in login")
        return render(request,"login.html",{"form":form}) 


class IndexView(TemplateView):
    template_name="index.html"

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    


