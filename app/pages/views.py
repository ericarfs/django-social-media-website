from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
############
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from .models import Question, Answer, Post
from user.models import User, Profile

def redirectPNF(request, exception): return redirect('home')

# Create your views here.
@user_passes_test(lambda user: not user.username, login_url='/home', redirect_field_name=None)
def IndexView(request):
    return render(request, 'pages/index.html')

class AboutView(TemplateView):
    template_name=('pages/about.html') 


@login_required(login_url='/account/login')
def homeView(request):
    profile = Profile.objects.get(user=request.user)
    posts = profile.get_my_and_following_posts()
    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'profiles/home.html', context = context)

@login_required(login_url='/account/login')
def profileDetailView(request, user):
   
    if (user=="login" or user == "home"):
        return redirect('/home')

    if User.objects.filter(username = user).exists(): 
        requestedUser = User.objects.get(username = user)
        profile = Profile.objects.get(user=requestedUser)
        posts = profile.get_my_posts()

        context = {
            'profile': profile,
            'username': user,
            'posts': posts,
            'userFound':"true",
        }
        return render(request, 'profiles/profile.html', context = context)
    else:
        context = {
            'username': user,
            'userFound': "false",
        }
        return render(request, 'profiles/profile.html', context = context)


@login_required(login_url='/account/login')
def profileInboxView(request):
    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_to = profile, is_answered=False).order_by('-created_at')
    
    return render(request, 'profiles/inbox.html', {'questions':questions})

@login_required(login_url='/account/login')
def postDetailView(request, user, id):
    requestedUser =  User.objects.get(username = user)
    profile = Profile.objects.get(user=requestedUser)

    posts = []
    if Post.objects.filter(id = id).exists(): 
        posts.append(Post.objects.get(id=id))

    context = {
        'profile': profile,
        'username': user,
        'posts': posts,
    }
    
    return render(request, 'profiles/profile.html', context = context)
