from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView
from social.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm,CommentForm
from django.contrib.auth import authenticate,login,logout
from social.models import UserProfile,Posts,Comments
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


class IndexView(CreateView,ListView):
    template_name="index.html"
     #create and list post view in the index page
    form_class=PostForm
    model=Posts
    context_object_name="data"

    def form_valid(self, form) :
        #form.instance ponits to postform user
        form.instance.user=self.request.user
        return super().form_valid(form)
  
    #after create sucessfully, the url needs to redirect to another view.so below fun implimented
    def get_success_url(self) -> str:
        return reverse("index")
    
    #to sort post in decending order()
    def get_queryset(self):
        qs=Posts.objects.order_by("-created_date")
        return qs


class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
class ProfileUpdateView(UpdateView):
    template_name="profile_add.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self) -> str:
        return reverse("index")
    
class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user) #exclude will remove the loggedin user
        return render(request,"profile_list.html",{"data":qs})
    

#follow url 
class FollowView(View):
    def post(self,request,*args,**kwargs):
        #print(request.POST)
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action == "follow":
            request.user.profile.following.add(profile_object) #add following userprofile to req .user
        elif action=="unfollow":
            request.user.profile.following.remove(profile_object)#remove following userprofile to req .user
        return redirect("index")



class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        print(action)
        if action == "like":
            post_object.liked_by.add(request.user)

        elif action == "dislike":
            post_object.liked_by.remove(request.user)
        
        return redirect("index")
    
class CommentView(CreateView): #comment is gona create so create view
    template_name="index.html"
    form_class=CommentForm #which form class is gona render

    def get_success_url(self) -> str:
        return reverse("index")
    
    def form_valid(self, form) :
        #form.instance ponits to postform user
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)

#localhost:8000/profile/<int:pk>/block

class ProfileBlockView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        #take the  profile wana block ,take pro obj
        profile_object=UserProfile.get(id=id)
        action=request.POST.get("action")
        if action == "block":
            request.user.profile.block.add(profile_object) #request.user.profile will give the logined user
        elif action=="unblock":
            request.user.profile.block.remove(profile_object)
        
        return redirect("index")
        
         

        
