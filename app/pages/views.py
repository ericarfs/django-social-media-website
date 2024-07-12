from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
############
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
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
        profile = Profile.profiles.get(user=user)

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
    questions_list = Question.questions.get_queryset(user = request.user)
    
    return render(request, 'profiles/inbox.html', {'questions':questions_list})

@login_required(login_url='/account/login')
def postDetailView(request, user, id):
    profile = Profile.profiles.get(user=user)

    posts = []
    if Post.objects.filter(id = id).exists(): 
        posts.append(Post.objects.get(id=id))

    context = {
        'profile': profile,
        'username': user,
        'posts': posts,
    }
    
    return render(request, 'profiles/profile_post.html', context = context)


@login_required(login_url='/account/login')
@csrf_exempt
def editProfileView(request, user):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'username': user,
    }
    
    return render(request, 'profiles/edit_profile.html', context = context)