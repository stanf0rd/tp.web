from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from questions import views
# from questions.views import QuestionList

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<tag>/', views.tag, name='tag_page'),
    path('question/<int:question_id>/', views.question, name='question_page'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask')
]

urlpatterns += staticfiles_urlpatterns()
