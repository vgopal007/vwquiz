# home/quizapp Function: Displays a list of quiz categories. Redirects to the quiz page for a selected category.
# quiz Function: Displays a quiz page for a specific category.
# get_quiz Function: Retrieves random quiz questions, optionally filtered by category. 
# Returns them as JSON. Handles exceptions with a “Something went wrong” response.
# Create your views here.



# Django imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count, Sum
from django.forms import Form
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods

# Local imports
from .crud import create_quizsession, create_userresponse
from .models import *

# Standard library imports
import json
import logging
import re
import random
from collections import Counter

# Third-party imports
import requests
from fuzzywuzzy import fuzz


from login.decorators import login_required_decorator


# Constants
UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

# Logging
logger = logging.getLogger(__name__)


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
class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '/'
        

class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirect URL after logout

    def dispatch(self, request, *args, **kwargs):
        # Additional logic before logout
        return super().dispatch(request, *args, **kwargs)


@login_required_decorator
def quizapp(request):
    context = {
        'categories': Types.objects.all(),
        'test_mode': "P"
    }

    subject_id = request.GET.get('subject')
    test_mode = request.GET.get('test_mode')

    if test_mode not in ['P', 'T']:
        test_mode = 'P'

    if subject_id and test_mode:
        subject_obj = Types.objects.get(subject_name=subject_id)
        subject_dict = model_to_dict(subject_obj)
        context = {
            'subject': subject_dict,
            'test_mode': test_mode
        }
        
        return render(request, 'quiz.html', {
            'subject': json.dumps(subject_dict),
            'test_mode': test_mode
            })
        # return render(request, 'quiz.html', context)


    return render(request, 'quizapp.html', context)


@login_required_decorator
def quiz(request):
    """
    Handles quiz page.

    Displays quiz questions based on selected subject.
    """

    context = {'subject': request.GET.get('subject')}
    return render(request, 'quiz.html', context)


def select_questions(subject_obj):
    try:
        topic_objs = subject_obj.get_topic_objs()  # returns a list of topic objects
        if not topic_objs:
            logging.error("No topics found for subject")
            return None

        question_objs = Question.objects.filter(subject=subject_obj)
        sampled_records = []

        for topic_obj in topic_objs:
            num_questions = int(subject_obj.test_numberofquestions * topic_obj.weight_perc / 100)
            questions = question_objs.filter(topic=topic_obj)
            sampled_records.extend(random.sample(list(questions), min(num_questions, len(questions))))

        # If the total number of sampled questions is less than required, sample additional questions
        if len(sampled_records) < subject_obj.test_numberofquestions:
            remaining_questions = subject_obj.test_numberofquestions - len(sampled_records)
            additional_questions = random.sample(
                list(question_objs.exclude(uid__in=[q.uid for q in sampled_records])),
                min(remaining_questions, len(question_objs) - len(sampled_records))
            )
            sampled_records.extend(additional_questions)

        # If there are still not enough questions, log error and return None
        if len(sampled_records) < subject_obj.test_numberofquestions:
            logging.error("Insufficient questions available to meet the required number")
            return None

        return sampled_records
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None

  
def get_quiz(request):
    """
    This function gets a list of questions with associated options for the quiz based on the Subject
    It also creates placeholders for responses by storing the questions in UserResponse table by calling create_userresponse from crud.py
    """
    
    try:
        subject_value = request.GET.get('subject')
        if subject_value is None:
            return JsonResponse({'error': "Key 'subject' not found in request.GET"}, status=400)
        
        user = request.user  
        try:
            user_obj = User.objects.get(username=user)
        except User.DoesNotExist:
            user_obj = None  # or handle the exception
        
        test_mode = request.GET.get('test_mode')
        # question_objs = Question.objects.all()
        
        try:
            types_obj = Types.objects.get(subject_name=subject_value)
            types_uid=types_obj.uid
            types_data = model_to_dict(types_obj)
        except Types.DoesNotExist:
            types_data = {}
            types_uid = None 
        
        # Access attributes of Types
        test_duration_minutes = types_data['test_duration_minutes']
        test_numberofquestions = types_data['test_numberofquestions']            
        print("Questions : ", test_numberofquestions, " Duration in Minutes : ", test_duration_minutes)
        # Create Session
        session_data = {"user_obj":user_obj, "types_obj":types_obj, "test_numberofquestions":test_numberofquestions, "test_duration_minutes":test_duration_minutes
                       }
        session = create_quizsession(session_data)       
        
        # Select questions
        sampled_records = select_questions(types_obj)
        if sampled_records:
            print("Sampled Records:", sampled_records)
        else:
            print("No sampled records found.")
            
        data = []
        random.shuffle(sampled_records)  # Shuffle questions
        
        for question_obj in sampled_records:
            data.append({
                "uid": question_obj.uid,
                "subject": question_obj.subject.subject_name,
                "question_type": question_obj.question_type,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answer": question_obj.get_answers(),
                "answer_explanation": question_obj.answer_explanation,
                "reference": question_obj.reference,
                "difficulty_level": question_obj.difficulty_level,
                "marks": question_obj.marks,
                "source": question_obj.source,
            })
            
            # Create user_response holder with all questions in the session for Test mode
            #if test_mode == 'T':
            user_response = create_userresponse(session, question_obj)
        
        payload = {'status': True, 'data': data, 'session_id': session.uid}
        print (payload)
        return JsonResponse(payload)  # Return JsonResponse
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)
        
        

 
 
@require_GET
def get_user_response(request):
    session_id = request.GET.get('session_id')
    question_id = request.GET.get('question_id')

    # Fetch the UserResponse if it exists
    response = UserResponse.objects.filter(session_id=session_id, question_id=question_id).first()

    if response:
        data = {
            "selected_answers": response.selected_answers,
            "selected_answer": response.selected_answer,
        }
        return JsonResponse({"response": data})
    else:
        return JsonResponse({"error": "Response not found"}, status=404)

def check_userresponse(question, selected_answers, selected_answer, apply_fuzzylogic):
    answeroptions = question.get_answers()
    explanation = question.answer_explanation
    is_correct = False
    correct_response = None

    if question.question_type == "CB":
        correct_answers = [answer['answer'] for answer in answeroptions if answer['is_correct']]
        correct_response = correct_answers
        if isinstance(selected_answers[0], dict):
            selected_answers = [answer['answer'] for answer in selected_answers]
        if set(selected_answers) == set(correct_answers):
            is_correct = True
    else:
        correct_answer = next((answer['answer'] for answer in answeroptions if answer['is_correct']), None)
        
        if correct_answer is None:
           Print("Quiz setup Error - No correct answer defined for ", question.question)
           
           
        correct_response = correct_answer
        if isinstance(selected_answer, dict):
            selected_answer = selected_answer['answer']

        if question.question_type == "IN":
            correct_answer = correct_answer.lower()
            selected_answer = selected_answer.lower()
            if selected_answer == correct_answer:
                is_correct = True
            else:
                print("apply_fuzzylogic: ", apply_fuzzylogic)
                if apply_fuzzylogic:          
                    similarity = fuzz.ratio(selected_answer, correct_answer)
                    print("similarity : ", similarity) 
                    if similarity > 80:  # Adjust threshold
                        is_correct = True
                        # you also need to install the fuzzy library
                        # pip install fuzzywuzzy python-Levenshtein
        else:
            if selected_answer == correct_answer:
                is_correct = True

    return {
        'is_correct': is_correct,
        'correct_response': correct_response,
        'explanation': explanation,
    }

## Updated storeuserresponse:
@require_POST
def storeuserresponse(request):
    try:
        data = json.loads(request.body)

        session_id = data.get('session_id')
        question_id = data.get('question_id')
        selected_answers = data.get('selected_answers', [])
        selected_answer = data.get('selected_answer', "")
        test_mode = data.get('test_mode',"P")
        apply_fuzzylogic=data.get('apply_fuzzylogic',False)

        if not session_id or not question_id:
            return JsonResponse({'message': 'Invalid data'}, status=400)

        session = get_object_or_404(QuizSession, uid=session_id)
        question = get_object_or_404(Question, uid=question_id)

        answer_result = check_userresponse(question, selected_answers, selected_answer,apply_fuzzylogic)

        # Save user response for Tests, but not Practice mode
        #if test_mode=="T":
        try:
                UserResponse.objects.update_or_create(
                session=session,
                question=question,
                defaults={
                    'selected_answers': selected_answers,
                    'selected_answer': selected_answer,
                    'is_correct': answer_result['is_correct'],
                }
                )
        except Exception as e:
               return JsonResponse({'message': f'Database error: {str(e)}'}, status=500)

        return JsonResponse({
            'message': 'User responses saved successfully!',
            'is_answer': answer_result['is_correct'],
            'correct_response': answer_result['correct_response'],
            'explanation': answer_result['explanation'],
        })

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Session or question not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Server error: {str(e)}'}, status=500)


@require_http_methods(["GET", "POST"])
def session_report(request, session_id):
    try:
        session = QuizSession.objects.get(uid=session_id)
    except QuizSession.DoesNotExist:
        return JsonResponse({'message': 'Session not found'}, status=404)

    summary_report=session.get_results()
    question_report=session.get_questionreport()
    report = {**summary_report, **question_report}

    return JsonResponse(report, safe=False, json_dumps_params={'indent': 4}, status=200)
    #return render(request, 'results.html', {'report': report, 'form': form}, status=200)
    

@require_http_methods(["POST"])
def update_quiz_session(request, session_id):
    if not UUID_REGEX.match(session_id):
        return JsonResponse({'message': 'Invalid session ID'}, status=400)
   
 
    try: 
        session = QuizSession.objects.get(uid=session_id)
        session.completed = True
        results = session.get_results()  or {}
        session.score = results['score']
        session.total_questions = results['total_questions']
        session.correct_answers = results['correct_answers']
        session.incorrect_answers = results['incorrect_answers']

        
           
        session.timed_out = False
        
        
        # Validate data before saving
        if session.score < 0:
            raise ValueError('Invalid score')
        
        session.full_clean()  # Validate model fields
        session.save()
        
        return JsonResponse({'message': 'Session updated successfully'})
    
    except QuizSession.DoesNotExist:
        return JsonResponse({'message': 'Session not found'}, status=404)

    except QuizSession.MultipleObjectsReturned:
        logger.error("Multiple sessions found")
        return JsonResponse({'message': 'Internal server error'}, status=500)   
        
    except ValueError as e:
        return JsonResponse({'message': str(e)}, status=400)
    
    except ValidationError as e:
        return JsonResponse({'message': 'Validation error', 'errors': e.message_dict}, status=400)
    
    except Exception as e:
        # Log unexpected errors
        logger.error(f'Unexpected error: {e}')
        return JsonResponse({'message': 'Internal server error'}, status=500)
        
        
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


