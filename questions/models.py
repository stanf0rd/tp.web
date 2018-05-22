from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name="User's avatar")

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tag name")

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Question title")
    text = models.TextField(verbose_name="Full question text")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=datetime.now, verbose_name="Publication time")
    is_active = models.BooleanField(default=True, verbose_name="If question is active")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-creation_date']
