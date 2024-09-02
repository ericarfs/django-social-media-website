from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer, Post
from user.models import User, Profile
from .notifications import get_notifications_user, notifications_count
from notifications.models import Notification

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
def inboxView(request):
    questions_list = Question.questions.get_queryset(user = request.user)
    return render(request, 'profiles/inbox.html', {'questions':questions_list})


@login_required(login_url='/account/login')
def notificationsView(request):
    notifications = get_notifications_user(request.user)
    
    notifications_list = []
    for notification in notifications:
        values = {}
        values["notification"] = notification
        values["link"] = {"page":'pages:profile-detail', "elem1":notification.actor}
        values["description"]  = None
        
        if notification.description is not None:
            answer = Answer.objects.get(id = int(notification.description))
            post = Post.objects.get(answer=answer)

            values["description"] = {"question": answer.question.body}
            values["link"] = {"page":'pages:post-detail', "elem1":post.author.user, "elem2":post.id}
        
        notifications_list.append(values)
    
    Notification.objects.mark_all_as_read(recipient=request.user)

    return render(request, 'profiles/notifications.html', {'data':notifications_list})


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
    if request.method == "POST":
        username = request.POST.get('username')
        body = request.POST.get('body')
        anon = request.POST.get('anon')

        profile = Profile.objects.get(user=request.user)

        if username != request.user.username and User.objects.filter(username = username).exists(): 
            error = "Username already taken !"
            context = {
                "res":"error",
                "message":error
            }
            return JsonResponse(context)


        allow_anon = True if anon == "on" else False

        profile.user.username = username
        profile.question_helper = body
        profile.allow_anonymous_questions = allow_anon

        profile.user.save()
        profile.save()

        posts = profile.get_my_posts()

        return JsonResponse({'username':username})
    
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'username': request.user,
    }
        
    return render(request, 'profiles/edit_profile.html', context = context)