from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Answer
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, AnswerForm, QuestionForm, LoginForm, UserForm
from django.contrib.auth import authenticate, login, logout


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
    question_obj = get_object_or_404(Question, pk=question_id)
    answers = question_obj.answer_set.all()
    paginator = Paginator(answers, 2)
    page = request.GET.get('page')

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question_obj
            answer.save()
            return redirect('/question/<question_id>', pk=answer.pk)
    else:
        form = AnswerForm()

    content = {
        'question': question_obj,
        'answers': paginator.get_page(page),
        'form': form
    }
    return render(request, 'questions/questions.html', content)


def login_page(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/', pk=user.pk)
        # else:
        #     form = LoginForm()
    else:
        form = LoginForm()

    return render(request, 'questions/login.html', {'form': form})


def logout_page(request):
    logout(request)

    return new(request)


def register(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        user_form = UserForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('/', pk=user.pk)
    else:
        profile_form = ProfileForm()
        user_form = UserForm()

    return render(request, 'questions/register.html', {'user_form': user_form, 'profile_form': profile_form})


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
