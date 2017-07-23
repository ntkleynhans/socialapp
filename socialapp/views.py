# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from postmanager import PostManager
from models import Post
from resources import generate_resource

# Create your views here.

### HTML PAGES ###
def home_page(request):
    """ Home page with login and register
    """
    context = {}
    return render(request, 'socialapp/home.html', context)

def register_page(request):
    """ Register page
        -- user registration form; email, name, surname, password, confirm password
    """
    context = {}
    return render(request, 'socialapp/register.html', context)

def login_page(request):
    """ Login page
        -- user login form; email & password
    """
    context = {}
    return render(request, 'socialapp/login.html', context)

### REGISTER ###
class RegisterForm(forms.Form):
    """ User registration form; data type and validation
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
        -- capture data using register form post
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
        -- use Django type validation
    """
    email = forms.EmailField()
    password = forms.CharField()

def verify_credentials(request):
    """ Verify user login
        -- capture data using login form
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
        logout(request) # remove user authentication
        return HttpResponseRedirect(reverse('socialapp:home_page', args=()))
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

### POSTS ###
def wall(request):
    """ A message wall showing existing messages
        -- paginate 5 entries per page
        -- user can click on the post to see more details
    """
    if request.user.is_authenticated:
        posts_list = Post.objects.all()
        for post in posts_list:
            old_post = PostManager(post.post_date, post.user, post.resource_link, post.post_type)
            old_post = old_post.create(None)
            post.title = old_post.post_title()

        paginator = Paginator(posts_list, 5) # Show 5 posts per page

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        return render(request, 'socialapp/wall.html', {'posts': posts})
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

def create_post(request, type_id):
    """ Create a new post
        -- type_id: post type i.e. MessagePost
        -- TODO: use typeid to create a specific Post type
    """
    if request.user.is_authenticated:
        # For now just render the create post template
        return render(request, 'socialapp/create_post.html', {})
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

def save_post(request, type_id):
    """ Save a post of a particular post type
        -- TODO: for now just message type
    """
    if request.user.is_authenticated:
        # Create a new post and validate the form data
        new_post = PostManager(timezone.now(), request.user.username, generate_resource(), type_id)    
        form = new_post.validate(request)
        if form.is_valid(): # Check if provided data is okay
            new_post.create(form)
            post = Post(post_date=new_post.post_date, user=new_post.user, resource_link=new_post.resource_link, post_type=type_id)
            post.save()
            return HttpResponseRedirect(reverse('socialapp:wall', args=()))
        else:
            return render(request, 'socialapp/create_post.html',
                { 'error_message' : "{}".format(form.errors)})
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

def post_detail(request, pk):
    """ Display the post (identified by pk number) details
    """
    if request.user.is_authenticated:
        # Find, create and load the posts' data
        post = get_object_or_404(Post, pk=pk)
        old_post = PostManager(post.post_date, post.user, post.resource_link, post.post_type)
        old_post = old_post.create(None)

        # For the user's name else just use the email address
        users = User.objects.all()
        qset = users.filter(email=post.user)
        full_name = post.user
        if len(qset) != 0:
            full_name = "{} {}".format(qset[0].first_name, qset[0].last_name)

        # See if the user owns this post and enable/disable deleting thereof
        delete_disabled = ""
        if request.user.username != post.user:
            delete_disabled = "disabled"

        message = {"message_id" : post.id, "message_date" : post.post_date, "message_user" : full_name,
            "message_title" : old_post.post_title, "message_body" : old_post.post_body, "delete_disabled" : delete_disabled}

        return render(request, 'socialapp/post_detail.html', message)
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

def delete_post(request, pk):
    """ Delete an existing post given the post id (database pk number)
    """
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        old_post = PostManager(post.post_date, post.user, post.resource_link, post.post_type)
        old_post = old_post.create(None)
        old_post.delete() # Remove the data from the filesystem
        post.delete() # remove the db entry

        return HttpResponseRedirect(reverse('socialapp:wall', args=()))
    else:
        return HttpResponseRedirect(reverse('socialapp:login_page', args=()))

