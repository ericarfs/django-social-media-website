from django.http import HttpResponse
from django.shortcuts import render
from .models import Profile, User
from pages.models import Answer, Question, Post
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(['DELETE'])
def block_user(request, user):
    blocked_user = User.objects.get(username = user)
    blocked_profile = Profile.objects.get(user=blocked_user)

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_by = blocked_profile)
    
    questions.delete()
    
    questions = Question.objects.filter(sent_to = profile)
    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_question(request, id):
    question = Question.objects.get(id = id)
    
    question.delete()

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_to = profile, is_answered=False)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_questions_by_user(request):
    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_to = profile, is_answered=False)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})


def get_question_by_id(request, id):
    question = question = Question.objects.get(id = id)
    return render(request, 'profiles/partials/show_question.html', {'question':question})


def saveQuestion(request, user):
    body = request.POST.get('body')
   # is_anon = request.POST.get('anon')
    sent_to = user
    sent_by = request.user

    print(body)
    print(is_anon)
    print(sent_to)
    print(sent_by)

    '''product = Product(
        name = name,
        price = price
    )
    product.save()

    products = Product.objects.all()'''

    return HttpResponse("555")

def save_question(request, user):
    body = request.POST.get('body')
    anon = request.POST.get('anon')
    
    is_anon = True if anon == "on" else False

    requestedUser = User.objects.get(username = request.user)
    sent_by = Profile.objects.get(user=requestedUser)

    requestedUser = User.objects.get(username = user)
    sent_to = Profile.objects.get(user=requestedUser)

    question = Question(
        sent_to = sent_to,
        sent_by = sent_by,
        body = body,
        is_anon = is_anon
    )
       
    question.save()

    return HttpResponse("555")


def save_answer(request, id):
    body = request.POST.get('body')
    question = Question.objects.get(id = id)
    
    print(body)
    question.is_answered = True

    answer = Answer(
        question = question,
        body = body
    )
    
    question.save()
    answer.save()

    requestedUser =  User.objects.get(username = request.user)
    profile = Profile.objects.get(user=requestedUser)

    questions = Question.objects.filter(sent_to = profile, is_answered=False)

    return render(request, 'profiles/partials/list_all_questions.html', {'questions':questions})

