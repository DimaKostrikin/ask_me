from django.shortcuts import render

from django.core.paginator import Paginator

from app.models import Question
from app.models import Answer
from app.models import Profile

answers = [
    {
        'id': idx,
        'text': f'text-answer {idx}',
        'likes': idx,
    } for idx in range(10)
]

def new_questions(request):
    questions = Question.objects.all()
    page = paginate(questions, request, 3)
    return render(request, 'new_questions.html', {
        'questions': page,
    })

def hot_questions(request):
    questions = Question.objects.best()
    page = paginate(questions, request, 3)
    return render(request, 'hot_questions.html', {
        'questions': page
    })

def login_page(request):
    return render(request, 'login.html', {})

def settings_page(request):
    return render(request, 'settings.html', {})

def ask_question(request):
    return render(request, 'ask.html', {})

def question(request, pk):
    questions = Question.objects.one(pk)
    answers = Answer.objects.all()
    return render(request, 'question.html', {
        'questions': questions,
        'answers': answers,
    })

def signup_page(request):
    return render(request, 'signup.html', {})


def tagged_questions(request, pk):
    questions = Question.objects.tag(pk)
    page = paginate(questions, request, 3)
    return render(request, 'tagged_questions.html', {
        'questions': page,
        'tag': pk,
    })

def paginate(object_list, request, per_page=10):
    page = object_list
    paginator = Paginator(page, per_page)
    page = request.GET.get('page')
    page = paginator.get_page(page)

    return page
