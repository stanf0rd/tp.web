from django.contrib import admin
from questions.models import Question, Answer, User, Tag

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(User)
admin.site.register(Tag)
