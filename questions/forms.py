from django.db import models
from django.forms import ModelForm
from django import forms
from questions.models import Question, User, Answer
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import  login, authenticate

# from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Login'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("Login or password are invalid.\nPlease try again.")
            return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return user

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


class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Username' }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder':'Email' }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Password' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Confirm password' }))

    avatar = forms.ImageField()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #         if not user or not user.is_active:
    #             raise forms.ValidationError("Login or password are invalid.\nPlease try again.")
    #         return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']