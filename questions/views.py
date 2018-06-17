from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from .models import Question, Answer
from .forms import AnswerForm, QuestionForm, LoginForm, UserForm


def new(request):
    question_list = Question.objects.get_new_questions()
    paginator = Paginator(question_list, 2)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions})


def hot(request):
    question_list = Question.objects.get_hot_questions()
    paginator = Paginator(question_list, 2)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/hot.html', {'questions': questions})


def by_tag(request, tag):
    question_list = Question.objects.get_tag_questions(tag)
    paginator = Paginator(question_list, 2)
    page_number = request.GET.get('page')
    content = {
        'tag': tag,
        'questions': paginator.get_page(page_number)
    }
    return render(request, 'questions/tag.html', content)


def question(request, question_id):
    question_obj = get_object_or_404(Question, pk=question_id)
    answers = question_obj.get_answers()
    paginator = Paginator(answers, 2)
    page = request.GET.get('page')

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save_answer(request.user, question_obj)
            return redirect('/question/<question_id>')
    else:
        form = AnswerForm()

    content = {
        'question': question_obj,
        'answers': paginator.get_page(page),
        'form': form
    }
    return render(request, 'questions/questions.html', content)


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/', pk=user.pk)
    else:
        form = UserForm()
    return render(request, 'questions/register.html', {'form': form})


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'questions/login.html', {'form': form})


def logout_page(request):
    logout(request)
    return new(request)


def ask(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.save()
            return redirect('/', pk=new_question.pk)
    else:
        form = QuestionForm()

    return render(request, 'questions/ask.html', {'form': form})
