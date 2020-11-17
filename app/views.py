from django.shortcuts import render

from django.core.paginator import Paginator

questions = [
    {
        'id': idx,
        'tag': ['black-jack', 'bender'],
        'title': f'title {idx}',
        'text': 'text text',
        'likes': idx,
        'answers': idx,
    } for idx in range(10)
]

answers = [
    {
        'id': idx,
        'text': f'text-answer {idx}',
        'likes': idx,
    } for idx in range(10)
]

def new_questions(request):
    page = paginate(questions, request, 3)
    return render(request, 'new_questions.html', {
        'questions': page,
    })

def hot_questions(request):
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
    question = questions[pk]
    page = paginate(answers, request, 3)
    return render(request, 'question.html', {
        'question': question,
        'answers': page,
    })

def signup_page(request):
    return render(request, 'signup.html', {})


def tagged_questions(request, pk):
    tag1 = pk
    page = paginate(questions, request, 3)
    return render(request, 'tagged_questions.html', {
        'questions': page,
        'tag': tag1,
    })

def paginate(object_list, request, per_page=10):
    page = object_list
    paginator = Paginator(page, per_page)
    page = request.GET.get('page')
    page = paginator.get_page(page)

    return page
