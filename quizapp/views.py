# home/quizapp Function: Displays a list of quiz categories. Redirects to the quiz page for a selected category.
# quiz Function: Displays a quiz page for a specific category.
# get_quiz Function: Retrieves random quiz questions, optionally filtered by category. 
# Returns them as JSON. Handles exceptions with a “Something went wrong” response.
# Create your views here.

from django.shortcuts import render,  redirect
from django.http import JsonResponse  
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .crud import create_quizsession
from .crud import create_userresponse

from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404

import json
import random

from django.views.decorators.csrf import csrf_exempt


"""
@login_required
def user_dashboard(request):
    # Fetch all quiz attempts by the logged-in user
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')

    # Pass data to the template
    return render(request, 'dashboard.html', {
        'quiz_attempts': quiz_attempts
    })
"""
    
@login_required
def quizapp(request):
    #print("Request passed to quizapp view is ",request)
    context = {'categories': Types.objects.all()}
    #print (context)
    if request.GET.get('subject'):
     
       #return redirect(f"/quizapp/?subject={request.GET.get('subject')}")
       return redirect(f"/quiz/?subject={request.GET.get('subject')}")
    
    return render(request, 'quizapp.html', context)
    


def quiz(request):
    context = {'subject': request.GET.get('subject')}
    #print ("context from quiz function in view.py - ", context)
    return render(request, 'quiz.html', context)


def get_quiz(request):
    
    try:
        #print ("Request passed to view.get_quiz  : ", request)
        question_objs = Question.objects.all()
        subject_value = request.GET.get('subject')
        #print("subject_value from views.get_quiz : ", subject_value)
        #if subject_value is None or subject_value not in valid_subjects:
        if subject_value is None:
           return JsonResponse({'error': "Key 'subject' not found in request.GET"}, status=400)


        # create session
        user = request.user  # Assuming this is a Django view
        print("user=",user)
       
        #user='pbkdf2_sha256$870000$HiLLj02UXghftdV9xb2cXj$0IHjBkZmDjUhBBcWVKnYh0lSCTNDsBG+Xee5VCFgYrs='
        session=create_quizsession(user,subject_value)
        print ("Session : ",session)
        # end create session
    
   
        question_objs = question_objs.filter(subject__subject_name__icontains = subject_value)
        #print (type(question_objs)) # this returns <class 'django.db.models.query.QuerySet'>

        num_samples_per_category = 1 # replace this with weightage based values 
        sampled_records = []
        # Get unique values of the topic field from the collection of questions
        unique_topics = question_objs.values_list('topic', flat=True).distinct()
        # Convert the result to a list
        if unique_topics.count()==0 :
           print("Quiz not setup yet.  Please contact the administrator")
           return JsonResponse({'error': "Quiz not setup yet. Please contact the administrator"}, status=404)
           # display a message to user and exit gracefully
           
        unique_topics_list = list(unique_topics)
        print ("Unique Topics ",unique_topics_list)
        for unique_topic in unique_topics_list:
            category_records = question_objs.filter(topic=unique_topic)
            category_records = list(category_records)  # convert to a list
            sampled_records.extend(random.sample(category_records, num_samples_per_category))
        
        #print("sampled_records : ", sampled_records)  # returns a list of questions, 5 from each topic
        
        question_objs=sampled_records
  
        data = []
        random.shuffle(question_objs)  # shuffle to rearrange randomly
        
        
        for question_obj in question_objs:
            
            data.append({
                "uid" : question_obj.uid,
                "subject": question_obj.subject.subject_name,
                "question_type": question_obj.question_type,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answer" : question_obj.get_answers(),
                "answer_explanation" : question_obj.answer_explanation,
                "reference" : question_obj.reference,
                "difficulty_level" : question_obj.difficulty_level,
                "marks" : question_obj.marks,
                "source" : question_obj.source,
                #"iscorrect" : False,


               
            })

            # create user_response holder with all questions in the session
            user_response=create_userresponse(session,question_obj)
           
   


        payload = {'status': True, 'data': data,'session_id': session.uid}
        # print ("Data : ", data)
        return JsonResponse(payload)  # Return JsonResponse
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)
        
def next_question(request):
    current_question_id = int(request.GET.get('current_question_id'))
    next_question = Question.objects.filter(id__gt=current_question_id).first()
    return JsonResponse({'question_text': next_question.question})

def prev_question(request):
    current_question_id = int(request.GET.get('current_question_id'))
    prev_question = Question.objects.filter(id__lt=current_question_id).last()
    return JsonResponse({'question_text': prev_question.question})

def goto_question(request):
    question_id = int(request.GET.get('question_id'))
    question = Question.objects.get(id=question_id)
    return JsonResponse({'question_text': question.question})

def review(request):
    questions = Question.objects.all()
    return render(request, 'review.html', {'questions': questions})
    
def addsession_view(request):
    # Your logic here
    # print ("Request passed to addsession_view : ", request)
   
    return JsonResponse({'message': 'Hello from Django!'})

@require_GET
def get_user_response(request):
    session_id = request.GET.get('session_id')
    question_id = request.GET.get('question_id')

    # Fetch the UserResponse if it exists
    response = UserResponse.objects.filter(session_id=session_id, question_id=question_id).first()
    selected_answers = response.selected_answers if response else []

    return JsonResponse({'selected_answers': selected_answers})


#@csrf_exempt  
# Use this if you are not including CSRF token in your AJAX request
@require_POST
def storeuserresponse(request):
    try:
        data = json.loads(request.body)
        print ("Data passed to view.storeuserresponse : ", data)
        session_id = data.get('session_id')
        question_id = data.get('question_id')
        selected_answers = data.get('selected_answers', [])
        is_correct = data.get('is_correct')

        if not session_id or not question_id or not selected_answers:
            return JsonResponse({'message': 'Invalid data'}, status=400)

        #session = get_object_or_404(QuizSession, pk=session_id)
        #question = get_object_or_404(Question, pk=question_id)
        # Fetch the QuizSession instance
        session = get_object_or_404(QuizSession, pk=session_id)
        question = get_object_or_404(Question, pk=question_id)
        
        # Update or create the UserResponse (assume selected_answers is a list)
        UserResponse.objects.update_or_create(
            session=session,
            question=question,
            #defaults={'selected_answers': selected_answers, 'is_correct': is_correct},
            selected_answer=selected_answers,
            is_correct=is_correct,
        )

        return JsonResponse({'message': 'User responses saved successfully!'})
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

"""
@require_POST
def save_user_response(request):
    data = json.loads(request.body)

    session_id = data.get('session_id')
    question_id = data.get('question_id')
    selected_answers = data.get('selected_answers', [])

    session = get_object_or_404(QuizSession, pk=session_id)
    question = get_object_or_404(Question, pk=question_id)

    # Update or create the UserResponse (assume selected_answers is a list)
    UserResponse.objects.update_or_create(
        session=session,
        question=question,
        defaults={'selected_answers': selected_answers}
    )

    return JsonResponse({'message': 'User responses saved successfully!'})
"""