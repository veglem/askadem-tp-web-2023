from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

IsLogedIn = True
QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Content of question {i}.',
        'likes': 10,
        'answers_count': 5
    } for i in range(50)
]


def paginate(objects_list, page_num, per_page=10):
    p = Paginator(objects_list, per_page)

    if page_num < 1 or page_num > p.num_pages:
        return None

    page = p.get_page(page_num)

    return page


def index(request, page=1):
    page_questions = paginate(QUESTIONS, page)
    if page_questions is None:
        return HttpResponseNotFound(f"404 Not Found: No such page")

    return render(request, 'main.html', {
        'IsLogedIn': IsLogedIn,
        'questions': page_questions,
        'page': page,
        'max_pages': int(len(QUESTIONS) / 10)})


def question(request, question_id, page=1):
    question_item = QUESTIONS[question_id]
    answers = [
        {
            'content': f'Question {question_id} is complex. This is answer {i}',
            'likes': 10
        } for i in range(15)
    ]

    page_answers = paginate(answers, page, 5)

    return render(request, 'question.html', {
        'IsLogedIn': IsLogedIn,
        'question': question_item,
        'answers': page_answers,
        'page': page,
        'max_pages': int(len(answers) / 5)})


def tag(request, tag_name, page=1):
    page_questions = paginate(QUESTIONS, page)
    if page_questions is None:
        return HttpResponseNotFound(f"404 Not Found: No such page")

    return render(request, 'tag.html', {
        'IsLogedIn': IsLogedIn,
        'questions': page_questions,
        'tag': tag_name,
        'page': page,
        'max_pages': int(len(QUESTIONS) / 10)})


def ask(request):
    return render(request, 'ask.html', {
        'IsLogedIn': IsLogedIn
    })


def login(request):
    global IsLogedIn
    IsLogedIn = False
    return render(request, 'login.html', {
        'IsLogedIn': IsLogedIn
    })


def logout(request):
    global IsLogedIn
    IsLogedIn = True
    return index(request)


def register(request):
    return render(request, 'register.html', {
        'IsLogedIn': IsLogedIn
    })


def settings(request):
    return render(request, 'settings.html', {
        'IsLogedIn': IsLogedIn
    })