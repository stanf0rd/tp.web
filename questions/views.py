from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Question
from .forms import UserForm
# from django.views.generic.list import ListView

# class QuestionList(ListView):
#     model = Question
#     paginate_by = 1

def index(request):
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 5)

    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'questions/index.html', {'questions': questions})

    # question_title = "How to cook spicy chicken using python3?"
    # question_text = "but note that this is not really a good way of doing things. If you just want a link that looks like a button, then have a normal a href and use CSS to style it like a button. In Bootstrap, for example, you can use the classes on any element to make it look like a button."
    # question_list = []
    # for i in range(1, 30):
    #     question_list.append({
    #         'question_title': question_title + str(i),
    #         'question_text': question_text + str(i),
    #         'question_id': i,
    #         'rating': 25 + i,
    #         'answer_count': 4 + i,
    #     })
    # tag_list = []
    # for i in range(1, 5):
    #     tag_list.append({
    #         'tag_name': "python3." + str(i),
    # })
    # context = {
    #     "question_list": question_list,
    #     "tag_list": tag_list,
    # }
    # return render(request, 'questions/index.html', {'question': get_object_or_404(Question)})

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
