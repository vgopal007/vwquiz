from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .loadjson_orm import load_json_data

# Register your models here.

# Inline admin for Answer model
class AnswerAdmin(admin.StackedInline):
    model = Answer

# Admin for Question model with inline AnswerAdmin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_display = ('question', 'subject', 'topic', 'question_type', 'marks')
    search_fields = ('question', 'subject__name', 'topic__name')
    list_filter = ('subject', 'topic', 'question_type', 'difficulty_level')

# Admin for Answer model
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('answer',)

# Admin for QuizSession model
class SessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'test_mode', 'subject', 'total_questions', 'correct_answers', 'score', 'completed', 'timed_out')
    search_fields = ('user_id__username', 'subject__name')
    list_filter = ('test_mode', 'subject', 'completed', 'timed_out')

# Form for TopicLesson model using CKEditorUploadingWidget for text_content
class TopicLessonAdminForm(forms.ModelForm): 
    text_content = forms.CharField(widget=CKEditorUploadingWidget()) 
    class Meta: 
        model = TopicLesson 
        fields = '__all__' 

# Inline admin for TopicLesson model using TopicLessonAdminForm
class TopicLessonInline(admin.StackedInline): 
    model = TopicLesson 
    form = TopicLessonAdminForm 

# Admin for Topics model with inline TopicLessonInline
class TopicsAdmin(admin.ModelAdmin):
    inlines = [TopicLessonInline]
    list_display = ('topic', 'subject', 'weight_perc', 'delete_flag')
    search_fields = ('topic', 'subject__name')
    list_filter = ('subject', 'delete_flag')
    # readonly_fields = ('delete_flag',)

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'subject', 'Active', 'created_at', 'expire_at')
    list_filter = ('Active', 'created_at', 'expire_at')
    search_fields = ('user_id__username', 'subject__subject_name')

# Registering models with the admin site
admin.site.register(Types)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(TopicLesson)
admin.site.register(QuizSession, SessionAdmin)
admin.site.register(UserResponse)
admin.site.register(UserSubscription)
