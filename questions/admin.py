from django.contrib import admin
from questions.models import Question, User, Tag

# Register your models here.

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
