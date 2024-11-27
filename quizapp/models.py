from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.contrib.auth.decorators import login_required

from ckeditor.fields import RichTextField

import uuid
import random
from math import floor
from enum import Enum

class TestMode(Enum):
    TEST = 'T'
    PRACTICE = 'P'
    
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True

class Types(BaseModel):
    """
    Represents quiz subject

    Attributes:
        subject_name : Question subject such as SAT Math.
        Domain : Educational, Professional..
        test_duration_minutes - remember to multiple this by 60 in the timer which is in seconds
    """

    class Meta:
        verbose_name_plural = "Types"  # Set the plural name explicitly
    subject_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    test_duration_minutes=models.IntegerField(default=30)
    test_numberofquestions=models.IntegerField(default=30)
    apply_fuzzylogic=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.subject_name

 
    def get_topics(self):
        topic_objs = sorted(list(Topics.objects.filter(subject=self)), key=lambda x: x.topic)
        data = []
        for topic_obj in topic_objs:
            data.append({
                'topic': topic_obj.topic,
                })
 
        return data
   
    def get_topic_objs(self):
        topic_objs = sorted(list(Topics.objects.filter(subject=self)), key=lambda x: x.topic)
        total_weight_perc = sum(topic_obj.weight_perc for topic_obj in topic_objs)

        if total_weight_perc == 0:
            if len(topic_objs) == 0:
                raise Exception("No topics found")

            # Allocate percentage equally
            weight_perc = 100 // len(topic_objs)
            for topic_obj in topic_objs:
                topic_obj.weight_perc = weight_perc
                #topic_obj.save()
                
        
        # Validate total weight percentage
        if round(total_weight_perc,0) != 100:
            print(f"Warning: Total weight percentage ({total_weight_perc}) is not 100.")

        return topic_objs
        

    @login_required
    def get_user_sessions(request, subject_name):
        user = request.user
    
        try:
            subject = Types.objects.get(subject_name=subject_name)
            sessions = QuizSession.objects.filter(user_id=user, subject=subject)
        except Types.DoesNotExist:
            sessions = None

        context = {
            'sessions': sessions,
            'subject_name': subject_name,
        }

        return render(request, 'quizapp/user_sessions.html', context)

class UserSubscription(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    subject = models.ForeignKey(Types, related_name='user_subjects', on_delete=models.CASCADE, db_index=True)
    Active=models.BooleanField(default=False, blank=False)
    created_at = models.DateField(auto_now_add=True)
    expire_at = models.DateField()


class Topics(BaseModel):
    """
    Represents topics within a given subject.

    Attributes:
        subject (Types): Question subject such as SAT Math.
        topic (str): Question topic such as Trigonometry.
        weight_perc (int): Weightage to be given to each Topic. The total should not exceed 100 for a given subject
    """
    class Meta:
        verbose_name_plural = "Topics"  # Set the plural name explicitly
    topic = models.CharField(max_length=100,unique=True)
    subject = models.ForeignKey(Types, related_name='types_topic', on_delete=models.CASCADE)
    weight_perc = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    delete_flag=models.BooleanField(default=False, blank=False) # soft delete 
    def __str__(self) -> str:
        return self.topic
        
    def clean(self):
        # Validate total weightage for subject
        total_weightage = sum(t.weight_perc for t in Topics.objects.filter(subject=self.subject))
        if total_weightage > 100:
            raise ValidationError("Total weightage exceeds 100%")
            
    def get_topic_questions(self):
        try:
            question_objs = self.topics_question.all()
            random.shuffle(question_objs)
            data = []
            for question_obj in question_objs:
                data.append({
                    'question': question_obj.question,
            })
            return data
        except Exception as e:
            return []
            
    def get_related_lessons(self): 
        return self.topic_lessons.filter(delete_flag=False).order_by('display_order')
 
class TopicLesson(BaseModel): 
    """ Represents lessons within a given topic. 
    Attributes: topic (Topics): The topic to which the lesson belongs. 
    title (str): The title of the lesson. 
    text_content (str): 
    The text content of the lesson. 
    audio_content (FileField): The audio content of the lesson. 
    video_content (FileField): The video content of the lesson. 
    display_order (int): The order in which the lesson should be displayed. 
    delete_flag (bool): Soft delete flag. """ 
    class Meta: verbose_name_plural = "Topic Lessons" # Set the plural name explicitly 
    topic = models.ForeignKey(Topics, related_name='topic_lessons', on_delete=models.CASCADE) 
    title = models.CharField(max_length=100) 
    #text_content = models.TextField(blank=True, null=True) 
    text_content = RichTextField(blank=True, null=True)
    audio_content = models.FileField(upload_to='audio/', blank=True, null=True) 
    video_content = models.FileField(upload_to='video/', blank=True, null=True) 
    display_order = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    delete_flag = models.BooleanField(default=False, blank=False) # soft delete def __str__(self): return self.title
 

class Question(BaseModel):
    """
    Represents a quiz question.

    Attributes:
        subject (Types): Question subject.
        topic (str): Question topic.
        question_type (str): Question type (RB, CB, IN).
        question (str): Question text.
        marks (int): Question marks.
    """
    QUESTION_TYPES = [
        ('RB', 'Radio Button'),
        ('CB', 'Checkbox'),
        ('IN', 'Input'),
    ]
    
    subject = models.ForeignKey(Types, related_name='types_question', on_delete=models.CASCADE)
    #topic = models.CharField(max_length=100, null=True, blank=True)
    topic = models.ForeignKey(Topics, related_name='topics_question', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='RB')
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    answer_explanation = models.CharField(max_length=255, null=True, blank=True)
    difficulty_level= models.CharField(max_length=20, null=True, blank=True)
    reference = models.CharField(max_length=100)
    source = models.CharField(max_length=10)
    delete_flag=models.BooleanField(default=False, blank=False) # soft delete 
    qc_passed=models.BooleanField(default=False, blank=False)   # Question that has been checked manually by Quiz Admin
    
    def __str__(self) -> str:
        return self.question
    
    def get_answers(self):
        related_answers = self.question_answer.all()
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        random.shuffle(answer_objs)
        
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data
        
    def get_correct_answer(self):
        if self.question_type == 'IN':
           return self.get_answers()[0]['answer'] if self.get_answers() else None
        
        if self.question_type == 'RB':
           return next((answer['answer'] for answer in self.get_answers() if answer['is_correct']), None)
          
        return None

    def get_correct_answers(self):
        if self.question_type == 'CB':
            return [answer['answer'] for answer in self.get_answers() if answer['is_correct']]
        return []

    def get_answer_explanation(self):
        return self.answer_explanation    

class Answer(BaseModel):
    """
    Represents 1 or more answers for a given question 

    Attributes:
      question (str): Question text.
      answer (str) : Represents the answer for IN question type and possible options for RB and CB with the correct option(s) having is_correct=true.
    """

    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.answer


from django.db import models
from django.contrib.auth.models import User


class QuizSession(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    test_mode = models.CharField(max_length=1, choices=[(tag.value, tag.name) for tag in TestMode], default="P",   null=False, blank=False)
    subject = models.ForeignKey(Types, related_name='types_session', on_delete=models.CASCADE, db_index=True)
    total_questions = models.IntegerField(null=True, blank=True)
    correct_answers = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    completed = models.BooleanField(default=False)
    timed_out = models.BooleanField(default=False)
    test_duration_minutes=models.IntegerField(default=30)


    def get_results(self):
        try:
            responses = UserResponse.objects.filter(session=self)
        except UserResponse.DoesNotExist:
            return {
                'total_questions': 0,
                'correct_answers': 0,
                'incorrect_answers': 0,
                'score': 0,
            }
        total_questions = responses.count()
        correct_answers = responses.filter(is_correct=True).count()
        unattempted_answers = responses.filter(selected_answer__isnull=True, selected_answers__isnull=True).count()
        incorrect_answers = total_questions - correct_answers - unattempted_answers
        if total_questions > 0:
            score = round((correct_answers / total_questions) * 100,0)
        else:
            score=0

        # Return overall results 
        return {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'unattempted_answers':unattempted_answers,
            'score': score,
    }


    def get_questionreport(self):
        responses = UserResponse.objects.filter(session=self)
  
        # Initialize question-wise report
        question_report = []

        # Iterate over responses
        for response in responses:
            question = response.question
            selected_answers = response.selected_answers if question.question_type == "CB" else response.selected_answer
            is_correct = response.is_correct
            expected_answer = question.get_correct_answers() if question.question_type == "CB" else question.get_correct_answer()
            explanation = question.answer_explanation
            # Append question-wise report
            question_report.append({
                'question_text': question.question,
                'selected_answers': selected_answers,
                'is_correct': is_correct,
                'correct_answers': expected_answer,
                'explanation': explanation,
        })

        # Return overall results and question-wise report
        return {
             'question_report': question_report,
    }

    def __str__(self):
        duration = (self.updated_at - self.created_at).total_seconds()
        minutes = floor(duration / 60)
        seconds = floor(duration % 60)
        return (
            f"{self.user_id} - {self.subject} - Score: {self.score} - "
            f"Started: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Ended: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Duration: {minutes} minutes, {seconds} seconds"
        )

class UserResponse(BaseModel):
    session = models.ForeignKey(
        QuizSession, related_name="session_responses", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        "Question", related_name="question_responses", on_delete=models.CASCADE
    )
    selected_answers = models.JSONField(blank=True, default=list)
    selected_answer = models.CharField(max_length=200, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session.user_id} - {self.question} - {self.selected_answer}"


