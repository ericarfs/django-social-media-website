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

        return render(request, 'profiles/partials/htmx/list_all_questions.html', {'questions':questions})
    
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

    return render(request, 'profiles/partials/htmx/list_posts.html', context = context)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_question(request, id):
    question = Question.objects.get(id = id)
    
    question.delete()

    questions = questions = get_questions(request.user)

    return render(request, 'profiles/partials/htmx/list_all_questions.html', {'questions':questions})



def get_questions_by_user(request):
    questions = get_questions(request.user)
    return render(request, 'profiles/partials/htmx/list_all_questions.html', {'questions':questions})


def get_question_by_id(request, id):
    question = question = Question.objects.get(id = id)
    return render(request, 'profiles/partials/htmx/show_question.html', {'question':question})

def check_question(request):
    body = request.GET.get('body')
    return render(request, 'profiles/partials/htmx/check_question.html', {'body': body})


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
        return render(request, 'profiles/partials/htmx/question_response.html', {'message': message})

    if len(body) > 1024:
        message = 'Question must contain up to 1024 characters !'
        return render(request, 'profiles/partials/htmx/question_response.html', {'message': message})

    question.save()

    return render(request, 'profiles/partials/htmx/question_response.html', {'message': message})



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

    return render(request, 'profiles/partials/htmx/list_all_questions.html', {'questions':questions})


def get_post(request, id):
    post = Post.objects.get(id = id)
    user = User.objects.get(username=post.author)
    profile = Profile.objects.get(user=user)

    context = {
        'profile': profile,
        'username': user,
        'post': post,
    }

    return render(request, 'profiles/partials/htmx/show_post.html', context= context)


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

    return render(request, 'profiles/partials/htmx/list_posts.html', context = context)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_post(request, id):
    post = Post.objects.get(id = id)
    
    post.delete()

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

    return render(request, 'profiles/partials/htmx/list_posts.html', context = context)


def edit_post(request, user, id):
    post = Post.objects.get(id = id)
    return render(request, 'profiles/partials/htmx/edit_post.html', {'post': post})

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

    return render(request, 'profiles/partials/htmx/list_posts.html', context = context)