from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ask_me import models

# Create your views here.

IsLogedIn = True


def sidebar_info():

    return {'tags': models.Tag.objects.get_top_tags(),
            'profiles': models.Profile.objects.get_top_users()}


def paginate(objects_list, page_num, per_page=10):
    p = Paginator(objects_list, per_page)

    if page_num < 1 or page_num > p.num_pages:
        return None

    page = p.get_page(page_num)

    return page


def index(request, page=1):
    page_questions = paginate(models.Question.objects.get_hot(), page)
    count = models.Question.objects.get_hot().count()
    if page_questions is None:
        return HttpResponseNotFound(f"404 Not Found: No such page")

    return render(request, 'main.html', {
        'IsLogedIn': IsLogedIn,
        'questions': page_questions,
        'page': page,
        'max_pages': int(count / 10 + (1 if count % 10 != 0 else 0)),
        'sidebar': sidebar_info()})


def last(request, page=1):
    page_questions = paginate(models.Question.objects.get_new(), page)
    count = models.Question.objects.get_new().count()
    if page_questions is None:
        return HttpResponseNotFound(f"404 Not Found: No such page")

    return render(request, 'new.html', {
        'IsLogedIn': IsLogedIn,
        'questions': page_questions,
        'page': page,
        'max_pages': int(count / 10 + (1 if count % 10 != 0 else 0)),
        'sidebar': sidebar_info()})


def question(request, question_id, page=1):
    question_item = get_object_or_404(models.Question, id=question_id)
    page_answers = paginate(models.Answer.objects.get_top_answers(question_item), page, 5)
    count = models.Answer.objects.get_top_answers(question_item).count()
    return render(request, 'question.html', {
        'IsLogedIn': IsLogedIn,
        'question': question_item,
        'answers': page_answers,
        'page': page,
        'max_pages': int(count / 5 + (1 if count % 5 != 0 else 0)),
        'sidebar': sidebar_info()})


def tag(request, tag_name, page=1):
    tag_item = get_object_or_404(models.Tag, name=tag_name)
    page_questions = paginate(models.Question.objects.get_questions_with_tag(tag_item), page)
    count = models.Question.objects.get_questions_with_tag(tag_item).count()
    if page_questions is None:
        return HttpResponseNotFound(f"404 Not Found: No such page")

    return render(request, 'tag.html', {
        'IsLogedIn': IsLogedIn,
        'questions': page_questions,
        'tag': tag_name,
        'page': page,
        'max_pages': int(count / 10 + (1 if count % 5 != 0 else 0)),
        'sidebar': sidebar_info()})


def ask(request):
    return render(request, 'ask.html', {
        'IsLogedIn': IsLogedIn,
        'sidebar': sidebar_info()
    })


def login(request):
    global IsLogedIn
    IsLogedIn = False
    return render(request, 'login.html', {
        'IsLogedIn': IsLogedIn,
        'sidebar': sidebar_info()
    })


def logout(request):
    global IsLogedIn
    IsLogedIn = True
    return index(request)


def register(request):
    return render(request, 'register.html', {
        'IsLogedIn': IsLogedIn,
        'sidebar': sidebar_info()
    })


def settings(request):
    return render(request, 'settings.html', {
        'IsLogedIn': IsLogedIn,
        'sidebar': sidebar_info()
    })