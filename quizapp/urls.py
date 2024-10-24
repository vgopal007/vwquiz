# quizapp\urls.py
from django.urls import path, include
from quizapp import views
from quizapp.views import quizapp, quiz, get_quiz, quiz_view, next_question, prev_question, goto_question, review

urlpatterns = [
   path('', views.quizapp , name = 'quizapp'),
#  path('quiz/', views.quiz, name= 'quiz'),
   path('quiz/', TemplateView.as_view(template_name='quiz.html')),   
   path('api/get-quiz/', views.get_quiz, name='get_quiz'),
   path('quiz_view/', views.quiz_view, name= 'quiz_view'),
   path('next_question/', views.next_question, name= 'next_question'),
   path('prev_question/', views.prev_question, name= 'prev_question'),
   path('goto_question/', views.goto_question, name= 'goto_question'),
   path('review/', views.review, name= 'review'),
   path('get_user_response/', views.get_user_response, name='get_user_response'),
   path('storeuserresponse/', views.storeuserresponse, name='storeuserresponse'),
   path('', views.storeuserresponse, name='storeuserresponse'),
   path('save_user_response/', views.save_user_response, name='save_user_response'),
   
 ]
