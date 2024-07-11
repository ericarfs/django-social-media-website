from django.http import HttpResponse
from django.shortcuts import render
from user.models import Profile, User
from pages.models import Answer, Question, Post
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def get_questions(user):
    requestedUser =  User.objects.get(username = user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_to = profile, is_answered=False).order_by('-created_at')
    return questions

    
@csrf_exempt
@require_http_methods(['DELETE'])
def block_user(request, user):
    blocked_user = User.objects.get(username = user)
    blocked_profile = Profile.objects.get(user=blocked_user)

    questions_to_delete = Question.objects.filter(sent_by = blocked_profile, is_answered=False)
    
    questions_to_delete.delete()

    referer = request.headers.get('Referer').split('/')
    if "inbox" in referer:
        questions = get_questions(request.user)

        return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})
    
    profile = Profile.objects.get(user=request.user)
    
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
    }

    return render(request, 'profiles/partials/list_posts.html', context = context)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_question(request, id):
    question = Question.objects.get(id = id)
    
    question.delete()

    questions = get_questions(request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_questions_by_user(request):
    questions = get_questions(request.user)
    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_question_by_id(request, id):
    question =  Question.objects.get(id = id)
    return render(request, 'profiles/partials/show_question.html', {'question':question})


def check_question(request):
    body = request.GET.get('body')
    return render(request, 'profiles/partials/check_question.html', {'body': body})


def save_question(request):
    user = request.POST.get('username')
    body = request.POST.get('body')
    anon = request.POST.get('anon')
    
    is_anon = True if anon == "on" else False

    sent_by_user = User.objects.get(username = request.user)
    sent_by = Profile.objects.get(user=sent_by_user)

    sent_to_user = User.objects.get(username = user)
    sent_to = Profile.objects.get(user=sent_to_user)

    question = Question(
        sent_to = sent_to,
        sent_by = sent_by,
        body = body,
        is_anon = is_anon
    )
    
    message = "Question sent successfully !"
    if len(body) < 4:
        message = 'Question must contain at least 4 characters !'
        return render(request, 'profiles/partials/question_response.html', {'message': message})

    if len(body) > 1024:
        message = 'Question must contain up to 1024 characters !'
        return render(request, 'profiles/partials/question_response.html', {'message': message})

    question.save()

    return render(request, 'profiles/partials/question_response.html', {'message': message})



def save_answer(request, id):
    body = request.POST.get('body')
    question = Question.objects.get(id = id)

    question.is_answered = True

    answer = Answer(
        question = question,
        body = body
    )
    
    question.save()
    answer.save()

    questions = get_questions(request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


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


def get_posts(request):
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
    if referer[-1] == 'home':
        posts = profile.get_my_and_following_posts()
        target = 'home'
    elif referer[-1] == '':
        posts = profile.get_my_posts()
        target = 'profile'
    else:
        target = 'profile_post'

    context = {
        'profile': profile,
        'posts': posts,
        'username': request.user,
    }

    return render(request, f'profiles/{target}.html', context = context)


def edit_post(request, user, id):
    post = Post.objects.get(id = id)
    return render(request, 'profiles/partials/edit_post.html', {'post': post})

def save_post(request, id):
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

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'profiles/partials/list_posts.html', context = context)

@csrf_exempt
def follow_unfollow_user(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    if target_user in profile.get_following():
        profile.remove_following(target_user)
    else:
        profile.add_new_following(target_user)

    profile.save()

    context = {
        'profile': target_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)

@csrf_exempt
def unfollow_user(request, user):
    user_to_unfollow =  User.objects.get(username = user)
    unfollowed_profile = Profile.objects.get(user=user_to_unfollow)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.remove_following(user_to_unfollow)

    profile.save()

    context = {
        'profile': unfollowed_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def mute_user(request, user):
    user_to_mute =  User.objects.get(username = user)
    muted_profile = Profile.objects.get(user=user_to_mute)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.add_new_silenced(user_to_silence)

    profile.save()

    context = {
        'profile': muted_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def unmute_user(request, user):
    user_to_unmute =  User.objects.get(username = user)
    unmuted_profile = Profile.objects.get(user=user_to_unmute)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.add_new_silenced(user_to_silence)

    profile.save()

    context = {
        'profile': unmuted_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def block_profile(request, user):
    user_to_block =  User.objects.get(username = user)
    blocked_profile = Profile.objects.get(user=user_to_block)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.add_new_blocked(user_to_block)

    profile.save()

    context = {
        'profile': blocked_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


@csrf_exempt
def unblock_profile(request, user):
    user_to_unblock =  User.objects.get(username = user)
    unblocked_profile = Profile.objects.get(user=user_to_unblock)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.add_new_blocked(user_to_block)

    profile.save()

    context = {
        'profile': unblocked_profile,
        'username': user,
    }
    return render(request, 'profiles/partials/profile_info.html', context = context)


def save_profile_changes(request):
    print(request.POST)
    body = request.POST.get('body')

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    profile.question_helper = body

    profile.save()

    posts = profile.get_my_posts()

    context = {
        'profile': profile,
        'username': requestedUser,
        'posts': posts,
    }

    return render(request, 'profiles/profile.html', context = context)
