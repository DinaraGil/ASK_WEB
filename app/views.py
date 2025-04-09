from django.contrib.admin.templatetags.admin_list import pagination_tag
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from app.models import Question

# Create your views here.
from django.http import HttpResponse

questions = Question.objects.all()
#
# for i in range(0,29):
#   questions.append({
#     'title': 'title ' + str(i),
#     'id': i,
#     'text': 'text' + str(i),
#     'img_path': "/img/concetemixer.jpg"
#   })

def paginate(objects, request, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page_number)

def index(request):
    questions = Question.objects.get_new()
    page = paginate(questions, request)
    return render(request, "index.html", context={'questions': page.object_list, "page_obj": page})

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
    questions = Question.objects.get_hot()
    page = paginate(questions, request)
    return render(request, "hot.html", context={'questions': page.object_list, "page_obj": page})



def question(request, question_id):
    question_obj = get_object_or_404(Question, id=question_id)
    like_count = question_obj.count_likes()
    return render(request, 'single_question.html', context={'question': question_obj, 'like_count': question_obj.count_likes()})
