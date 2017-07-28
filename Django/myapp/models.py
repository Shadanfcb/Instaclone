# -*- coding: utf-8 -*-
from django.db import models
import uuid


# Create your models here.


class UserModel(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    has_verified_mobile = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4


class Post(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return len(Like.objects.filter(post_id=self.id))


class Like(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(Post)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)