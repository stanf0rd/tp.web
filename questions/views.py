from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'questions/index.html')

def hot(request):
    return HttpResponse("You're looking at hot questions.")

def tag(request, tag):
    return HttpResponse("You're looking at tag \"%s\" questions." % tag)

def question(request, question_id):
    return HttpResponse("You're looking at question number %s." % question_id)

def login(request):
    return HttpResponse("You're looking at login page.")

def signup(request):
    return HttpResponse("You're looking at signup page.")

def ask(request):
    return HttpResponse("You're looking at ask page.")