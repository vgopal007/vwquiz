"""
URL configuration for vwquiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# vwquiz/urls.py
from django.contrib import admin
from django.urls import path, include
from quizapp import views
from django.contrib.auth.views import LoginView

urlpatterns = [
   path('admin/', admin.site.urls, name = 'Admin'),
#  path('quizapp/', include('quizapp.urls')),  # Include app-specific URLs
#  app-level URL patterns follow ...
   path('', views.quizapp , name = 'quizapp'),
   path('', views.quiz, name= 'quiz'),
   path('quiz/', views.quiz, name='quiz'),  # Add this line for the 'quiz/' URL
   path('api/get-quiz/', views.get_quiz, name='get_quiz'),
 # path('quizapp/', views.quiz_view, name= 'quiz_view'),
   path('', views.next_question, name= 'next_question'),
   path('', views.prev_question, name= 'prev_question'),
   path('', views.goto_question, name= 'goto_question'),
   path('', views.review, name= 'review'),
   path('storeuserresponse/', views.storeuserresponse, name='storeuserresponse'),
   path('', views.storeuserresponse, name='storeuserresponse'),
   path('', views.storeuserresponse, name='storeuserresponse'),
   path('session_report/<str:session_id>/', views.session_report, name='session_report'),
   path('update_quiz_session/<str:session_id>/', views.update_quiz_session, name='update_quiz_session'),
   #path('create-quizsession/', views.create_quizsession, name='create_quizsession'),
   path('login/', LoginView.as_view(template_name='login.html'), name='login'),
   path('register/', views.register, name='register'),
]

