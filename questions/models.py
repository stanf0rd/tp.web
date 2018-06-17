from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
#  AbstractUser


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name="User's avatar")
    rating = models.IntegerField(default=0, verbose_name="Answer rating")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tag name")

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Question title")
    text = models.TextField(verbose_name="Full question text")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name="Question rating")
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Publication time")
    answer_count = models.IntegerField(default=0, verbose_name="Count of answers")
    is_active = models.BooleanField(default=True, verbose_name="If question is active")
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name="Answer text")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    creation_date = models.DateTimeField(default=timezone.now, verbose_name="Publication time")
    rating = models.IntegerField(default=0, verbose_name="Answer rating")
    is_active = models.BooleanField(default=True, verbose_name="is active")
    is_right = models.BooleanField(default=False, verbose_name="marked by autor as right")
