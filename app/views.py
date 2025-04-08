from django.contrib.admin.templatetags.admin_list import pagination_tag
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

questions = []
for i in range(0,29):
  questions.append({
    'title': 'title ' + str(i),
    'id': i,
    'text': 'text' + str(i),
    'img_path': "/img/concetemixer.jpg"
  })

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def base(request):
    return render(request, 'base.html')


def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')


def hot(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(questions[::-1], 5)
    page = paginator.page(page_num)
    return render(request, 'hot.html', context={'questions': page.object_list, 'page_obj': page})

def question(request, question_id):
    return render(request, 'single_question.html', context={'question': questions[question_id]})
