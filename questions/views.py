from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Question
from .forms import UserForm

def index(request):
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 5)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions})

def hot(request):
    return render(request, 'questions/index.html')

def tag(request, tag):
    return HttpResponse("You're looking at tag \"%s\" questions." % tag)

def question(request, question_id):
    return HttpResponse("You're looking at question number %s." % question_id)

def login(request):
    return HttpResponse("You're looking at login page.")

def signup(request):

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
    return render(request, 'questions/signup.html', context)

def ask(request):
    return render(request, 'questions/ask.html')
