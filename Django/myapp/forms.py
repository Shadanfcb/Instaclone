from django import forms
from models import UserModel, Post, Like, CommentModel, CategoryModel

CATEGORY = (
    ('LAP', 'laptop'),
    ('CAR', 'cars'),
    ('MOB', 'Mobile'),
    ('BIKE', 'Bike'),
)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'name', 'email', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post']


class CommentForm(forms.ModelForm):
  class Meta:
    model = CommentModel
    fields = ['comment_text', 'post']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = CategoryModel
        fields=['category']