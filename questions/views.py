from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    question_title = "How to cook spicy chicken using python3?"
    question_text = "but note that this is not really a good way of doing things. If you just want a link that looks like a button, then have a normal a href and use CSS to style it like a button. In Bootstrap, for example, you can use the classes on any element to make it look like a button."
    question_list = []
    for i in range(1, 30):
        question_list.append({
            'question_title': question_title + str(i),
            'question_text': question_text + str(i),
            'question_id': i,
            'rating': 25 + i,
            'answer_count': 4 + i,
        })
    tag_list = []
    for i in range(1, 5):
        tag_list.append({
            'tag_name': "python3." + str(i),
    })
    context = {
        "question_list": question_list,
        "tag_list": tag_list,
    }
    return render(request, 'questions/index.html', context)

def hot(request):
    return render(request, 'questions/index.html')

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