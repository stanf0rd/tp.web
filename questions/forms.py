from django.db import models
from django.forms import ModelForm
from django import forms
from questions.models import Question, User
# from django.core.files.uploadedfile import SimpleUploadedFile

class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

# # Creating a form to add an article.
# form = ArticleForm()

# # Creating a form to change an existing article.
# article = Article.objects.get(pk=1)
# form = ArticleForm(instance=article)

class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Email'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

    avatar = forms.ImageField()
        # 'class':'custom-file-input custom-file',
        # 'placeholder':'Choose avatar'
    # avatar = forms.ImageField(label='Company Logo',required=False, error_messages = {'invalid':"Image files only"}, widget=forms.FileInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']
