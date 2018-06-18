from django.db import models
from django.forms import ModelForm
from django import forms
from questions.models import Question, User, Answer, Tag
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
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Title of your question'
    }))

    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Type your question here'
    }))

    tags_list = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'tags separated by commas (only first 5 will be read!)'
    }))

    def clean_title(self):
        if len(self.cleaned_data['title']) < 10:
            raise forms.ValidationError(
                "Title is too short. Minimum 10 symbols."
            )
        if len(self.cleaned_data['title']) > 100:
            raise forms.ValidationError("Title is too long... Describe the question below, please.")
        else:
            return self.cleaned_data['title']

    def clean_text(self):
        if len(self.cleaned_data['text']) < 100:
            raise forms.ValidationError(
                "Question is too short. Try to describe it issue in more detail."
            )
        if len(self.cleaned_data['text']) > 2000:
            raise forms.ValidationError("Question is too long... Maximum 2000 symbols")
        else:
            return self.cleaned_data['text']

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags_list']

    def save_question(self, request):
        question = self.save(commit=False)
        question.author = request.user
        question.save()
        taglist = self.cleaned_data['tags_list'].split(',', maxsplit=5)
        for tag in taglist:
            if not Tag.objects.filter(name=tag).exists():
                question.tags.create(name=tag)
            else:
                question.tags.add(Tag.objects.get(name=tag))
        return question


class AnswerForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Type your answer here'
    }))

    def save_answer(self, user, question):
        answer = self.save(commit=False)
        answer.author = user
        answer.question = question
        answer.save()

    def clean_text(self):
        if len(self.cleaned_data['text']) < 100:
            raise forms.ValidationError(
                "Question is too short. Try to describe it issue in more detail."
            )
        if len(self.cleaned_data['text']) > 2000:
            raise forms.ValidationError("Question is too long... Maximum 2000 symbols")
        else:
            return self.cleaned_data['text']

    class Meta:
        model = Answer
        fields = ['text']


class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder':'Confirm password'}))

    avatar = forms.ImageField()

    def clean_username(self):
        if len(self.cleaned_data['username']) > 20:
            raise forms.ValidationError("Username can not be longer than 20 characters.")
        else:
            return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']
