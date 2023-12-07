from django.contrib import admin
from .models import ImpromptuQuiz, SurveyQuiz, SurveyTopicbyUser, ImpromptuTopicbyUser

@admin.register(SurveyTopicbyUser)
class SurveyTopicAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic')
    list_filter = ( 'user', )

@admin.register(ImpromptuTopicbyUser)
class ImpromptuTopicAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic')
    list_filter = ( 'user', )

@admin.register(SurveyQuiz)
class SurveyQuizAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question')
    list_filter = ('topic',)
    search_fields = ('question', 'topic')

@admin.register(ImpromptuQuiz)
class ImpromptuQuizAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question')
    list_filter = ('topic',)
    search_fields = ('question', 'topic')