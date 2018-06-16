from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Answer
from .forms import UserForm

def new(request):
    paginator = Paginator(Question.objects.all(), 2)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions})

def hot(request):
    paginator = Paginator(Question.objects.all(), 2)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/hot.html', {'questions': questions})

def by_tag(request, tag):
    paginator = Paginator(Question.objects.all(), 2)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/tag.html', {'tag': tag, 'questions': questions})

def question(request, question_id):
    question_obj = Question.objects.get(pk=question_id)
    paginator = Paginator(Answer.objects.all(), 2)
    page = request.GET.get('page')
    answers = paginator.get_page(page)
    return render(request, 'questions/questions.html', {'question': question_obj, 'answers': answers})

def login(request):
    return render(request, 'questions/login.html')

def register(request):

    # form = ProfileForm(request.POST, request.FILES)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('/', pk=user.pk)
    else:
        form = UserForm(request.POST, request.FILES)

    context = {
        'form': form
    }
    return render(request, 'questions/register.html', context)

def ask(request):
    return render(request, 'questions/ask.html')
