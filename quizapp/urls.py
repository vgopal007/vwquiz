# quizapp\urls.py
from django.urls import path, include
from django.views.generic import TemplateView
from quizapp import views
from quizapp.views import quizapp, quiz, get_quiz, next_question, prev_question, goto_question, review
app_name = 'quizapp'
urlpatterns = [
   path('', views.quizapp , name = 'quizapp'),
#  path('quiz/', views.quiz, name= 'quiz'),
   path('quiz/', TemplateView.as_view(template_name='quiz.html')),   
   path('results/', TemplateView.as_view(template_name='results.html')),   
   path('api/get-quiz/', views.get_quiz, name='get_quiz'),
   path('next_question/', views.next_question, name= 'next_question'),
   path('prev_question/', views.prev_question, name= 'prev_question'),
   path('goto_question/', views.goto_question, name= 'goto_question'),
   path('review/', views.review, name= 'review'),
   path('get_user_response/', views.get_user_response, name='get_user_response'),
   path('storeuserresponse/', views.storeuserresponse, name='storeuserresponse'),
   path('', views.storeuserresponse, name='storeuserresponse'),
   path('login/', views.login_view, name='login'),  # URL for login page
   path('register/', views.register_view, name='register'),

  # path('login/', CustomLoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),

  ]

