from django.shortcuts import render, redirect, reverse

from django.core.paginator import Paginator

from app.models import Question, Answer, Profile
from django.views.decorators.http import require_POST
from django.contrib import auth
from app.forms import *

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
        'page_obj': page,
    })

def hot_questions(request):
    questions = Question.objects.best()
    page = paginate(questions, request, 3)
    return render(request, 'hot_questions.html', {
        'questions': page,
        'page_obj': page,
    })

def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect("/")  # правильный редирект

    ctx = {'form': form}
    return render(request, 'login.html', ctx)


def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required
def settings_page(request):
    form_class = AvatarForm
    if request.method == 'GET':
        form = form_class()
    else:
        form = form_class(data=request.POST, files=request.FILES, instance=request.user)
        form.save()
        if form.is_valid():
            return redirect(reverse('settings-view'))
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)

def question(request, pk):
    questions = Question.objects.one(pk)
    answers = Answer.objects.get_by_q(pk)
    page = paginate(answers, request, 3)
    
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST, qid=Question.objects.get_by_id(pk), profile=request.user.profile)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('one-question-view', kwargs={'pk': pk}))
    return render(request, 'question.html', {
        'questions': questions,
        'answers': page,
        'page_obj': page,
        'form': form,
    })

@login_required
def ask_question(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            return redirect(reverse('one-question-view', kwargs={'pk': question.pk}))
    ctx = {'form': form}
    return render(request, 'ask.html', ctx)


def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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

@require_POST
@login_required
def vote(request):
    data = request.POST
    from pprint import pformat
    print('\n\n', '=' * 100)
    print(f'HERE: {pformat(data)}')
    print('=' * 100, '\n\n')
    # обработка лайков
    return JsonResponse({'question_likes': 42})
    pass