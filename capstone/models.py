from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseQuiz(models.Model):
    section = models.CharField(max_length=100)
    topic = models.CharField(max_length=100, default="")
    question = models.TextField()

    class Meta:
        abstract = True

#돌발 주제
class ImpromptuQuiz(BaseQuiz):
    section = models.CharField(max_length=100, default="돌발주제")
    IMRPOMPTU_TOPIC_CHOICES = [
        ('가구', '가구'),
        ('명절/휴일', '명절/휴일'),
        ('재활용', '재활용'),
        ('지형과 활동', '지형과 활동'),
        ('자유시간', '자유시간'),
        ('모임', '모임'),
        ('호텔', '호텔'),
        ('기술', '기술'),
        ('휴대폰', '휴대폰'),
        ('인터넷', '인터넷'),
        ('산업', '산업'),
        ('교통수단', '교통수단'),
        ('음식/음식점', '음식/음식점'),
        ('건강', '건강'),
        ('은행', '은행'),
        ('약속', '약속'),
        ('날씨', '날씨'),
        ('의상/패션', '의상/패션'),
    ]
    topic = models.CharField(max_length=100, choices=IMRPOMPTU_TOPIC_CHOICES)

#선택 주제
class SurveyQuiz(BaseQuiz):
    section = models.CharField(max_length=100, default="선택주제")
    SURVEY_TOPIC_CHOICES = [
        ('개인주택이나 아파트에 홀로 거주', '개인주택이나 아파트에 홀로 거주'),
        ('가족과 함께 주택이나 아파트 거주', '가족과 함께 주택이나 아파트 거주'),
        ('영화보기', '영화보기'),
        ('공연보기', '공연보기'),
        ('공원가기', '공원가기'),
        ('해변가기', '해변가기'),
        ('카페/커피 전문점 가기', '카페/커피 전문점 가기'),
        ('쇼핑하기', '쇼핑하기'),
        ('TV시청하기', 'TV시청하기'),
        ('스포츠관람', '스포츠관람'),
        ('음악 감상하기', '음악 감상하기'),
        ('악기 연주하기', '악기 연주하기'),
        ('독서', '독서'),
        ('혼자 노래 부르거나 합창하기', '혼자 노래 부르거나 합창하기'),
        ('요리하기', '요리하기'),
        ('조깅', '조깅'),
        ('걷기', '걷기'),
        ('헬스', '헬스'),
        ('집에서 보내는 휴가', '집에서 보내는 휴가'),
        ('국내여행', '국내여행'),
        ('해외여행', '해외여행'),
    ]

    topic = models.CharField(max_length=100, choices=SURVEY_TOPIC_CHOICES)

# 유저와 설문주제 토픽 
class SurveyTopicbyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, choices=SurveyQuiz.SURVEY_TOPIC_CHOICES)

class ImpromptuTopicbyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, choices=ImpromptuQuiz.IMRPOMPTU_TOPIC_CHOICES)

class ResponseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, choices=ImpromptuQuiz.IMRPOMPTU_TOPIC_CHOICES)
    question = models.TextField()
    user_response = models.TextField()
    corrected_response = models.TextField()
    recording_time = models.CharField(max_length=255)
    accuracy = models.FloatField()
    similarity = models.FloatField()
    current_date = models.CharField(max_length=255)

class UserFeedbackModel(models.Model):
    user_answer = models.TextField()
    corrected_answer = models.TextField()
