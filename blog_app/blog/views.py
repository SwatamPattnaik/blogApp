from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

import datetime

import sys

# Create your views here.

def redirect_url(request):
    return HttpResponseRedirect(reverse('blog:index'))

def user_registration(request):
    try:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username = cd.get('username')
                email = cd.get('email')
                password = cd.get('password2')
                user = User.objects.create_user(username,email,password)
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return render(request, 'blog/user_registration_form.html', {'form': form})
        else:
            form = RegistrationForm()
            return render(request, 'blog/user_registration_form.html', {'form': form})
    except:
        return HttpResponseRedirect(reverse('blog:index'))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def index(request):
    try:
        my_blogs = []
        if request.user.is_authenticated:
            user_id = request.user.id
            my_blogs = Blog.objects.filter(user_id=user_id)
            
        all_blogs = Blog.objects.all()
        return render(request, 'blog/index.html', {'all_blogs':all_blogs,'my_blogs':my_blogs})
    except:
        return HttpResponseNotFound()

def blog_form(request):
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user_id = request.user.id
                title = cd.get('title')
                subtitle = cd.get('subtitle')
                body = cd.get('body')
                Blog.objects.create(user_id=user_id,title=title,subtitle=subtitle,body=body)
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return render(request, 'blog/blog_form.html', {'form':form,'edit':False})
        else:
            if request.user.is_authenticated:
                form = BlogForm()
                return render(request, 'blog/blog_form.html', {'form':form,'edit':False})
            else:
                return HttpResponseRedirect(reverse('blog:index'))
    except:
        return HttpResponseRedirect(reverse('blog:index'))

def edit_blog(request,blog_id):
    try:
        if Blog.objects.filter(id=blog_id).exists():
            blog = Blog.objects.get(id=blog_id)
            if request.user.id != blog.user.id:
                return HttpResponseRedirect(reverse('blog:index'))
            if request.method == 'POST':
                
                form = BlogForm(request.POST,instance=blog)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('blog:index'))
                else:
                    return render(request, 'blog/blog_form.html', {'form':form,'edit':True,'blog_id':blog_id})
            else:
                form = BlogForm(instance=blog)
                return render(request, 'blog/blog_form.html', {'form':form,'edit':True,'blog_id':blog_id})
        else:
            return HttpResponseRedirect(reverse('blog:index'))
    except:
        return HttpResponseRedirect(reverse('blog:index'))

def blog_page(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        if request.user.id == blog.user.id:
            author = True
            comments = Comment.objects.filter(blog_id=blog_id)
        else:
            author = False
            comments = Comment.objects.filter(blog_id=blog_id,approved=1)
        return render(request, 'blog/blog_page.html', {'blog':blog,'author':author,'comments':comments})
    except:
        return HttpResponseRedirect(reverse('blog:index'))

def add_comment(request):
    try:
        blog_id = request.POST.get('blog_id')
        comment = request.POST.get('comment')
        user_id = request.user.id
        blog = Blog.objects.get(id=blog_id)
        if blog.user.id == user_id:
            approved=1
        else:
            approved=0
        ct = datetime.datetime.now()
        timestamp = ct.timestamp()
        Comment.objects.create(blog_id=blog_id,user_id=user_id,body=comment,timestamp=timestamp,approved=approved)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)

def approve_comment(request):
    try:
        comment_id = request.POST.get('comment_id')
        Comment.objects.filter(id=comment_id).update(approved=1)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)

def reject_comment(request):
    try:
        comment_id = request.POST.get('comment_id')
        Comment.objects.get(id=comment_id).delete()
        return HttpResponse(comment_id,content_type='text/plain')
    except:
        return HttpResponse(status=500)
