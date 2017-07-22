# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from postmanager import PostManager
from models import Post
from resources import generate_resource

# Create your views here.

### HTML PAGES ###
def home_page(request):
    """ Home page
        -- just render links
    """
    context = {}
    return render(request, 'socialapp/home.html', context)

def register_page(request):
    """ Register page
        -- render links & registration form
    """
    context = {}
    return render(request, 'socialapp/register.html', context)

def login_page(request):
    """ Login page
        -- render links & login form
    """
    context = {}
    return render(request, 'socialapp/login.html', context)

### REGISTER ###
class RegisterForm(forms.Form):
    """ User registration form
    """
    email = forms.EmailField()
    name = forms.CharField()
    surname = forms.CharField()
    password = forms.CharField()
    confirmpassword = forms.CharField()

    def clean(self):
        """ Test that passwords are the same
        """
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirmpassword = cleaned_data.get("confirmpassword")

        if password and confirmpassword: # were the passwords provided
            if password != confirmpassword: # do they match
                raise forms.ValidationError("Password do not match!")

def register_user(request):
    """ Try register a new user
        -- from register form post
    """
    form = RegisterForm(request.POST)
    if form.is_valid():
        try: # Try register user
            user = User.objects.create_user(form.cleaned_data["email"], form.cleaned_data["email"], form.cleaned_data["password"])
            user.first_name = form.cleaned_data["name"]
            user.last_name = form.cleaned_data["surname"]
            user.save()
            return render(request, 'socialapp/login.html', {"register_message": "{} registered".format(form.cleaned_data["email"])})
        except: # Something went wrong
            return render(request, 'socialapp/register.html', {"error_message": "User exists!" })
    else: # Information is not correct
        return render(request, 'socialapp/register.html',
            { 'user_email' : request.POST["email"],  'user_name': request.POST["name"], 'user_surname' : request.POST["surname"],
             'user_password' : request.POST["password"], 'user_confirmpassword' : request.POST["repassword"], 'error_message' : "{}".format(form.errors)})

### LOGIN ###
class LoginForm(forms.Form):
    """ Login form
    """
    email = forms.EmailField()
    password = forms.CharField()

def verify_credentials(request):
    """ Verify user login
    """
    form = LoginForm(request.POST)
    if form.is_valid(): # Form information is valid 
        user = authenticate(request, username=form.cleaned_data["email"], password=form.cleaned_data["password"])
        if user is not None: # User has been registered
            login(request, user)
            return HttpResponseRedirect(reverse('socialapp:wall', args=()))
        else: # Not a valid user
            return render(request, 'socialapp/login.html', {"error_message": "User not registered!" })
    else: # Provided information is not correct
        return render(request, 'socialapp/login.html',
            { 'user_email' : request.POST["email"],  'user_password' : request.POST["password"], 
             'error_message' : "{}".format(form.errors)})

### LOGOUT ###
def logout_user(request):
    """ Logout user and remove authenticated status
    """
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('socialapp:home_page', args=()))
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

### POSTS ###
def wall(request):
    """ A message wall showing existing messages
    """
    context = {}
    return render(request, 'socialapp/wall.html', context)

def create_post(request, type_id):
    """ Create a new post
    """
    context = {}
    return render(request, 'socialapp/create_post.html', context)

def save_post(request, type_id):
    """ Save a post
    """
    new_post = PostManager(timezone.now(), request.user.username, generate_resource(), type_id)    
    form = new_post.validate(request)
    if form.is_valid():
        new_post.create(form)
        post = Post(post_date=new_post.post_date, user=new_post.user, resource_link=new_post.resource_link, post_type=type_id)
        post.save()

        context = {}
        return render(request, 'socialapp/wall.html', context)
    else:
        return render(request, 'socialapp/create_post.html',
            { 'error_message' : "{}".format(form.errors)})

