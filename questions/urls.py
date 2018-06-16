from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from questions import views
# from questions.views import QuestionList

urlpatterns = [
    path('', views.new, name='new'),
    path('hot/', views.hot, name='hot'),
    path('tag/<tag>/', views.by_tag, name='by_tag'),
    path('question/<int:question_id>/', views.question, name='question_page'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('ask/', views.ask, name='ask')
]

urlpatterns += staticfiles_urlpatterns()
