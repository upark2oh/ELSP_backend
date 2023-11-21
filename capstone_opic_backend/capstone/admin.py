from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ImpromptuQuiz, SurveyQuiz, Profile
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile" # 복수형으로 이름 표기하지 않도록 직접 지정
    
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


admin.site.register(ImpromptuQuiz)
admin.site.register(SurveyQuiz)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)