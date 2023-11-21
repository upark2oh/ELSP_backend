from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ImpromptuQuiz(models.Model):
    section = models.CharField(max_length=100, default="돌발주제")
    topic = models.CharField(max_length=100, default="")
    question = models.TextField()

class SurveyQuiz(models.Model):
    section = models.CharField(max_length=100, default="선택주제")
    topic = models.CharField(max_length=100, default="")
    question = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # primary_key를 User의 pk로 설정하여 통합적으로 관리
    nickname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    subjects = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile/', default='default.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)