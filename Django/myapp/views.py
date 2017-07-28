# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime
from forms import SignUpForm
from forms import LoginForm
from forms import PostForm
from forms import LikeForm
from forms import CommentForm
from django.contrib.auth.hashers import make_password, check_password
from models import UserModel, SessionToken, Post, Like, CommentModel
from imgurpython import ImgurClient


def signup_view(request):
    if request.method == "GET":
        print ('GET REQUEST')
        today = datetime.now()
        print (today)
        signup_form = SignUpForm()
        return render(request, 'index.html', {'today': today, 'signup_form': signup_form})
    elif request.method == 'POST':
            user_data = SignUpForm(request.POST)
            # print 'success'
            if user_data.is_valid():
                username = user_data.cleaned_data['username']
                name = user_data.cleaned_data['name']
                email = user_data.cleaned_data['email']
                password = user_data.cleaned_data['password']
                print ('%s %s %s %s' % (username, name, email, password))
                # saving data to DB
                user = UserModel(name=name,
                                password=make_password(password),
                                email=email,
                                username=username)
                # print 'success'
                user.save()

                return render(request, 'success.html', {'name': name})
            else:
                return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = UserModel.objects.filter(username=username).first()

        UserModel.objects.get(id=1)
        if user:
            if check_password(password, user.password):
                print ('User is valid')
            else:
                print ('User is invalid')

    elif request.method == 'GET':
        form = LoginForm()

    return render(request, 'login.html')


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = Post.objects.all().order_by('created_on')
        return render(request, 'feed.html', {})
    else:
        return redirect('/login/')


def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == "GET":
            form = PostForm()

            return render(request, 'post.html', {'form': form})
        elif request.method == 'POST':

            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = Post(user=user, image=image, caption=caption)
                from django.settings import BASE_DIR
                post.save()
                path = str(BASE_DIR + "/" + post.image.url)
                client = ImgurClient('85071a629f86550', '3f5d8bf356698fc42dafeeae3f4a2879b71e5d5a')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                print (post.image_url)
                post.save()
                return redirect('/feed')

    else:
        return redirect('/login/')


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
        return session.user
  else:
        return None


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = Like.objects.filter(post_id=post_id, user=user).first()
            posts = Post.objects.all().order_by('-created_on', )
            for post in posts:
                existing_like = Like.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True

                    if not existing_like:
                        print ("Going to like", post_id)
                        Like.objects.create(post_id=post_id, user=user)
                    else:
                        print ("Going to Unlike", post_id)
                        existing_like.delete()

                return redirect('/feed/')

        else:
            return redirect('/login/')


def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
     post_id = form.cleaned_data.get('post').id
     comment_text = form.cleaned_data.get('comment_text')
     comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
     comment.save()
     return redirect('/feed/')
    else:
     return redirect('/feed/')
  else:
        return redirect('/login')