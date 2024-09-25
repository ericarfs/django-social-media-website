from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from user.models import Profile, User
from pages.models import Answer, Question, Post
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify

@csrf_exempt
@require_http_methods(['DELETE'])
def block_user_inbox(request, user):
    blocked_user = User.objects.get(username = user)

    profile = Profile.objects.get(user=request.user)

    profile.blocked.add(blocked_user)
    profile.following.remove(blocked_user)

    questions = Question.questions.get_queryset(user = request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


@csrf_exempt
@require_http_methods(['DELETE'])
def block_user_post(request, user):
    blocked_user = User.objects.get(username = user)
    blocked_profile = Profile.objects.get(user=blocked_user)

    profile = Profile.objects.get(user=request.user)
    
    profile.blocked.add(blocked_user)
    profile.following.remove(blocked_user)

    referer = request.headers.get('Referer').split('/')


    posts = []
    if referer[-1] == 'home':
        posts = profile.get_my_and_following_posts()
    elif referer[-1] == '':
        posts = profile.get_my_posts()
    else:
        id = int(referer[-1] )
        posts.append(Post.objects.get(id = id))


    context = {
        'profile': profile,
        'posts': posts,
        'username': user,
    }

    return render(request, 'profiles/partials/list_posts.html', context = context)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_question(request, id):
    question = Question.objects.get(id = id)
    
    question.delete()

    questions = Question.questions.get_queryset(user = request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_questions_by_user(request):
    questions = Question.questions.get_queryset(user = request.user)
    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_question_by_id(request, id):
    question =  Question.objects.get(id = id)
    return render(request, 'profiles/partials/show_question.html', {'question':question})

@csrf_exempt
def save_question(request):
    user = request.POST.get('username')
    body = request.POST.get('body')
    anon = request.POST.get('anon')
    
    is_anon = True if anon == "on" else False
    
    sent_by_user = User.objects.get(username=request.user)
    sent_by = Profile.objects.get(user=request.user)
    sent_to = Profile.profiles.get(user=user)

    if is_anon == True and sent_to.allow_anonymous_questions == False:
        message = "This user doesn't allow anonymous questions !"
        return HttpResponse(message)
    
    message = "Question sent successfully !"

    if sent_by_user not in sent_to.get_silenced() and sent_by_user not in sent_to.get_blocked():
        question = Question(
            sent_to = sent_to,
            sent_by = sent_by,
            body = body,
            is_anon = is_anon
        )   
        question.save()

    return HttpResponse(message)


def save_answer(request, id):
    body = request.POST.get('body')
    question = Question.objects.get(id = id)
    profile = Profile.objects.get(user = request.user)

    question.is_answered = True

    answer = Answer(
        question = question,
        body = body
    )
    
    question.save()
    answer.save()

    if request.user != question.sent_by.user:
        notify.send(sender = profile, recipient = question.sent_by.user, verb = "answered your question.", description=answer.id)

    questions = Question.questions.get_queryset(user = request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


@csrf_exempt
def like_post(request, id):
    post = Post.objects.get(id = id)
    user = User.objects.get(username=request.user)

    if user not in post.get_likes():
        post.liked.add(user)
    else:
        post.liked.remove(user)

    post.save()

    return render(request, 'profiles/partials/like_button.html', {'post':post})


@csrf_exempt
def share_post(request, id):  
    post = Post.objects.get(id = id)
    user = User.objects.get(username=request.user)

    if user not in post.get_shares():
        post.shared.add(user)
    else:
        post.shared.remove(user)

    post.save()

    return render(request, 'profiles/partials/share_button.html', {'post':post})


def get_post(request, id):
    post = Post.objects.get(id = id)
    user = User.objects.get(username=post.author)
    profile = Profile.objects.get(user=user)

    context = {
        'profile': profile,
        'username': user,
        'post': post,
    }

    return render(request, 'profiles/partials/show_post.html', context= context)


@csrf_exempt
def get_posts(request, user):
    profile = Profile.profiles.get(user=user)

    referer = request.headers.get('Referer').split('/')

    posts = []
    if referer[-1] == 'home':
        posts = profile.get_my_and_following_posts()
    elif referer[-1] == '':
        posts = profile.get_my_posts()
    else:
        id = int(referer[-1] )
        posts.append(Post.objects.get(id = id))


    context = {
        'profile': profile,
        'posts': posts,
        'username': user,
    }

    return render(request, 'profiles/partials/list_posts.html', context = context)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_post(request, id):
    post = Post.objects.get(id = id)
    
    post.delete()

    profile = Profile.objects.get(user=request.user)

    referer = request.headers.get('Referer').split('/')

    posts = []
    target = 'profile'
    print(referer)
    if referer[-1].isnumeric():
        target = 'profile_post'
    elif referer[-2] == 'home':
        posts = profile.get_my_and_following_posts()
        target = 'home'
    else:
        posts = profile.get_my_posts()
        target = 'profile'


    context = {
        'profile': profile,
        'posts': posts,
        'username': request.user,
    }

    print(target)
    return render(request, f'profiles/{target}.html', context = context)


def edit_post(request, user, id):
    if request.method == "POST":
        post = Post.objects.get(id = id)
        new_answer = request.POST.get('body')

        post.answer.body = new_answer

        post.answer.save()
        post.save()

        profile = Profile.objects.get(user=request.user)

        referer = request.headers.get('Referer').split('/')
        posts = []
        if referer[-1] == 'home':
            posts = profile.get_my_and_following_posts()
        elif referer[-1] == '':
            posts = profile.get_my_posts()
        else:
            id = int(referer[-1] )
            posts.append(Post.objects.get(id = id))

        context = {
            'profile': profile,
            'posts': posts,
            'username': request.user,
        }

        return render(request, 'profiles/partials/list_posts.html', context = context)
        
    post = Post.objects.get(id = id)
    return render(request, 'profiles/partials/edit_post.html', {'post': post})


@csrf_exempt
def follow_unfollow_user(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    profile = Profile.objects.get(user=request.user)

    if target_user in profile.get_following():
        profile.following.remove(target_user)
    else:
        profile.following.add(target_user)
        notify.send(sender = profile, recipient = target_user, verb = "followed you.")

    profile.save()

    context = {
        'profile': target_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def mute_unmute_user(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    profile = Profile.objects.get(user=request.user)

    if target_user in profile.get_silenced():
        profile.silenced.remove(target_user)
    else:
        profile.silenced.add(target_user)

    profile.save()

    context = {
        'profile': target_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def block_unblock_profile(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    profile = Profile.objects.get(user=request.user)

    posts = []
    if target_user in profile.get_blocked():
        profile.blocked.remove(target_user)
        posts = target_profile.get_my_posts()
    else:
        profile.blocked.add(target_user)
        profile.following.remove(target_user)

    
    profile.save()

    context = {
        'profile': target_profile,
        'username': user,
        'posts': posts,
    }
    return render(request, 'profiles/profile.html', context = context)
