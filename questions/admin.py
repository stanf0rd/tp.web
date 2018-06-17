from django.contrib import admin
from questions.models import Question, Answer, Profile, Tag

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Tag)
