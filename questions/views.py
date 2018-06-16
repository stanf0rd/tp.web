from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Answer, Tag
from .forms import UserForm


def new(request):
    question_list = Question.objects.order_by('creation_date')
    paginator = Paginator(question_list, 2)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions})


def hot(request):
    question_list = Question.objects.order_by('rating')
    paginator = Paginator(question_list, 2)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/hot.html', {'questions': questions})


def by_tag(request, tag):
    question_list = Question.objects.filter(tags__name=tag)
    paginator = Paginator(question_list, 2)
    page_number = request.GET.get('page')
    content = {
        'tag': tag,
        'questions': paginator.get_page(page_number)
    }
    return render(request, 'questions/tag.html', content)


def question(request, question_id):
    paginator = Paginator(Answer.objects.all(), 2)
    page = request.GET.get('page')
    content = {
        'question': get_object_or_404(Question, pk=question_id),
        'answers': paginator.get_page(page)
    }
    return render(request, 'questions/questions.html', content)


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
