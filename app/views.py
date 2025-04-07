from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def base(request):
    return render(request, 'base.html')


def ask(request):
    return render(request, 'ask.html')
