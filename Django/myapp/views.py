from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm, CategoryForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel, CategoryModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils import timezone
from Django.settings import BASE_DIR

from imgurpython import ImgurClient


# Create your views here.
client_id = str('9bfedc15f2e6afe')
client_secret = str('704830f11469f79b0bbfa2feba976d96c095e2fe')
currentuser = None
category = None

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
            # return redirect('login/')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})


def login_view(request):
    global currentuser
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            currentuser= username
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                price = form.cleaned_data.get('price')
                category = form.cleaned_data.get('category')
                post = PostModel(user=user, image=image, caption=caption, price=price, category=category)
                post.save()
                #path = 'C:\Users\bhada\Documents\Myprojects\instaClone\instaclone\user_images'
                #path = str(BASE_DIR)
                path = str(BASE_DIR +'/'+ post.image.url)
                client = ImgurClient(client_id, client_secret)
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def feed_view(request):
    global currentuser
    global category
    user = check_validation(request)
    #form = CategoryForm(request.POST)
    if user:
        if category == 'MOB':
            category = 'LAP'
            # posts = PostModel.objects.all().order_by('created_on')
            posts = PostModel.objects.all().filter(category='LAP')
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            print currentuser
            return render(request, 'feed.html', {'posts': posts}, {'currentuser': currentuser})

        elif category == 'LAP':
            category = 'CAR'
            # posts = PostModel.objects.all().order_by('created_on')
            posts = PostModel.objects.all().filter(category='CAR')
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            print currentuser
            return render(request, 'feed.html', {'posts': posts}, {'currentuser': currentuser})

        elif category == 'CAR':
            category = 'BIKE'
            # posts = PostModel.objects.all().order_by('created_on')
            posts = PostModel.objects.all().filter(category='BIKE')
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            print currentuser
            return render(request, 'feed.html', {'posts': posts}, {'currentuser': currentuser})

        elif category == 'BIKE':
            category = 'MOB'
            # posts = PostModel.objects.all().order_by('created_on')
            posts = PostModel.objects.all().filter(category='MOB')
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            print currentuser
            return render(request, 'feed.html', {'posts': posts}, {'currentuser': currentuser})

        else:
            category = 'MOB'
            # posts = PostModel.objects.all().order_by('created_on')
            posts = PostModel.objects.all().filter(category='MOB')
            for post in posts:
                existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
                if existing_like:
                    post.has_liked = True
            print currentuser
            return render(request, 'feed.html', {'posts': posts}, {'currentuser': currentuser})



    else:

        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    print user.username
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


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None