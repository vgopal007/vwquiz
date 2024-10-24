from django.db import models
from django.contrib.auth.models import User
import uuid
import random

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True

class Types(BaseModel):
    class Meta:
        verbose_name_plural = "Types"  # Set the plural name explicitly
    subject_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.subject_name

class Topics(BaseModel):
    class Meta:
        verbose_name_plural = "Topics"  # Set the plural name explicitly
    topic = models.CharField(max_length=100)
    subject = models.ForeignKey(Types, related_name='types_topic', on_delete=models.CASCADE)
    weight_perc = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.topic

class Question(BaseModel):
    QUESTION_TYPES = [
        ('RB', 'Radio Button'),
        ('CB', 'Checkbox'),
        ('IN', 'Input'),
    ]
    
    subject = models.ForeignKey(Types, related_name='types_question', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, null=True, blank=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='RB')
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=1)
    answer_explanation = models.CharField(max_length=255, null=True, blank=True)
    difficulty_level= models.CharField(max_length=20, null=True, blank=True)
    reference = models.CharField(max_length=100)
    source = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return self.question
    
    def get_answers(self):
        # print ("Value passed to get_answers : ", self)
        related_answers = self.question_answer.all()
        #print ("Related Answers : ", related_answers)
        answer_objs = list(Answer.objects.filter(question=self))
        data = []
        random.shuffle(answer_objs)
        
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        print ("Output of get_answers : ",data)
        return data

class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.answer
        

class QuizSession(BaseModel):
    #user = models.ForeignKey(User, related_name='quiz_user', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    #quiz = models.ForeignKey(Types, related_name='quiz_subject', on_delete=models.CASCADE)
    quiz = models.CharField(max_length=100)

    score = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    timed_out = models.BooleanField(default=False)


class UserResponse(BaseModel):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question_user', on_delete=models.CASCADE)
    # For checkboxes, store multiple answers as a list
    # selected_answers = models.JSONField(blank=True, default=list)
    
    # For radio buttons or single text input, store a single answer
    selected_answer = models.CharField(max_length=200, blank=True)  
  
    is_correct = models.BooleanField(default=False)
    

