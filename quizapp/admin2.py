from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from .loadjson_orm import load_json_data

# Register your models here.

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    list_display = ('question', 'subject', 'topic', 'question_type', 'marks')
    search_fields = ('question', 'subject__name', 'topic__name')
    list_filter = ('subject', 'topic', 'question_type', 'difficulty_level')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_correct')
    #list_select_related = ('question',)

    list_filter = ('question', 'is_correct')
    search_fields = ('answer',)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'test_mode', 'subject', 'total_questions', 'correct_answers', 'score', 'completed', 'timed_out')
    search_fields = ('user_id__username', 'subject__name')
    list_filter = ('test_mode', 'subject', 'completed', 'timed_out')


class TopicLessonAdmin(admin.StackedInline):
    model = TopicLesson

class TopicLessonAdminForm(forms.ModelForm): 
    text_content = forms.CharField(widget=CKEditorWidget()) 
    class Meta: 
        model = TopicLesson 
        fields = '__all__' 
        
class TopicLessonAdmin(admin.ModelAdmin): 
    form = TopicLessonAdminForm 


class TopicsAdmin(admin.ModelAdmin):
    inlines = [TopicLessonAdmin]
    list_display = ('topic', 'subject', 'weight_perc', 'delete_flag')
    search_fields = ('topic', 'subject__name')
    list_filter = ('subject', 'delete_flag')
    # readonly_fields = ('delete_flag',)
    
admin.site.register(Types)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
#admin.site.register(TopicLesson,TopicLessonAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(TopicLesson, TopicLessonAdmin)
admin.site.register(QuizSession, SessionAdmin)
admin.site.register(UserResponse)


"""
@admin.action(description='Load JSON file')
def load_json(modeladmin, request, queryset):
    if request.method == 'POST':
        file = request.FILES['json_file']
        data = json.load(file)
        load_json_data(data)
        return HttpResponse('JSON file loaded successfully')
    return HttpResponseNotAllowed(['POST'])

class QuestionAdmin(admin.ModelAdmin):
    actions = [load_json]

admin.site.register(Question, QuestionAdmin)
"""
