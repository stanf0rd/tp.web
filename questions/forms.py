from django.db import models
from django.forms import ModelForm
from django import forms
from questions.models import Question, Profile, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# from django.core.files.uploadedfile import SimpleUploadedFile

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Login'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

# # Creating a form to add an article.
# form = ArticleForm()

# # Creating a form to change an existing article.
# article = Article.objects.get(pk=1)
# form = ArticleForm(instance=article)


class AnswerForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Type your answer here'
    }))

    class Meta:
        model = Answer
        fields = ['text']


class ProfileForm(ModelForm):

    avatar = forms.ImageField()
        # 'class':'custom-file-input custom-file',
        # 'placeholder':'Choose avatar'
        # avatar = forms.ImageField(
        # label='Company Logo',required=False,
        # error_messages = {'invalid':"Image files only"},
        # widget=forms.FileInput
    # )

    class Meta:
        model = Profile
        fields = ['avatar']

class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Username'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']