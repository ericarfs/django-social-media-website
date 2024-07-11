from django.http import HttpResponse
from django.shortcuts import render
from user.models import Profile, User
from pages.models import Answer, Question, Post
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def get_questions(user):
    requested_user =  User.objects.get(username = user)
    profile = Profile.objects.get(user=requested_user)

    questions = Question.objects.filter(sent_to = profile, is_answered=False).order_by('-created_at')
    blocked_users = profile.get_blocked_users()
    questions_list = [question for question in questions if question.sent_by.user not in blocked_users]

    return questions_list

    
@csrf_exempt
@require_http_methods(['DELETE'])
def block_user_inbox(request, user):
    blocked_user = User.objects.get(username = user)

    user = User.objects.get(username = request.user)
    profile = Profile.objects.get(user=user)

    profile.add_new_blocked(blocked_user)
    profile.remove_following(blocked_user)

    questions = get_questions(request.user)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


@csrf_exempt
@require_http_methods(['DELETE'])
def block_user_post(request, user):
    blocked_user = User.objects.get(username = user)
    blocked_profile = Profile.objects.get(user=blocked_user)

    user = User.objects.get(username = request.user)
    profile = Profile.objects.get(user=user)

    profile.add_new_blocked(blocked_user)
    profile.remove_following(blocked_user)

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

    if sent_by_user not in sent_to.get_silenced() or sent_by_user not in sent_to.get_blocked():
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

@csrf_exempt
def get_posts(request, user):
    requested_user = User.objects.get(username=user)
    profile = Profile.objects.get(user=requested_user)

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
        'username': request.user,
    }

    return render(request, 'profiles/partials/list_posts.html', context = context)

@csrf_exempt
def follow_unfollow_user(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    requested_user =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requested_user)

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
def mute_unmute_user(request, user):
    target_user =  User.objects.get(username = user)
    target_profile = Profile.objects.get(user=target_user)

    requested_user =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requested_user)

    if target_user in profile.get_silenced():
        profile.remove_silenced(target_user)
    else:
        profile.add_new_silenced(target_user)

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

    requested_user =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requested_user)

    posts = []
    if target_user in profile.get_blocked():
        profile.remove_blocked(target_user)
        posts = target_profile.get_my_posts()
    else:
        profile.add_new_blocked(target_user)
        profile.remove_following(target_user)

    
    profile.save()

    context = {
        'profile': target_profile,
        'username': user,
        'posts': posts,
    }
    return render(request, 'profiles/profile.html', context = context)


def save_profile_changes(request):
    body = request.POST.get('body')

    requested_user =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requested_user)

    profile.question_helper = body

    profile.save()

    posts = profile.get_my_posts()

    context = {
        'profile': profile,
        'username': requested_user,
        'posts': posts,
    }

    return render(request, 'profiles/profile.html', context = context)
