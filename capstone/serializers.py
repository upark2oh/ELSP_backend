from rest_framework import serializers
from .models import ImpromptuQuiz, SurveyQuiz
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import SurveyTopicbyUser, ImpromptuTopicbyUser, ResponseModel, UserFeedbackModel
#돌발주제조회
class ImpromptuQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpromptuQuiz
        fields = ("__all__")
    
    def validate_topic(self, value):
        # 유효한 토픽인지 확인
        valid_topics = [choice[0] for choice in ImpromptuQuiz.IMRPOMPTU_TOPIC_CHOICES]
        if value not in valid_topics:
            raise serializers.ValidationError("유효하지 않은 토픽입니다.")
        return value

class SurveyQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuiz
        fields = ("__all__")

    def validate_topic(self, value):
        # 유효한 토픽인지 확인
        valid_topics = [choice[0] for choice in SurveyQuiz.SURVEY_TOPIC_CHOICES]
        if value not in valid_topics:
            raise serializers.ValidationError("유효하지 않은 토픽입니다.")
        return value

# User - 선택질문 Topic을 확인할 때 사용하는 Serializer
class SurveyTopicbyUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # 사용자 ID를 문자열로 처리
    class Meta:
        model = SurveyTopicbyUser
        fields = ['user', 'topic']

# User - 돌발 질문 Topic을 확인할 때 사용하는 Serializer
class ImpromptuTopicbyUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # 사용자 ID를 문자열로 처리
    class Meta:
        model = ImpromptuTopicbyUser
        fields = ['user', 'topic']


# 사용자 정보를 읽어올 때 사용하는 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# 회원가입을 위한 Serializer
class RegisterSerializer(serializers.ModelSerializer):
    # 비밀번호를 입력받을 때만 사용하고 출력 시에는 포함하지 않음
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
         # 사용자 생성 및 비밀번호 암호화
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # RefreshToken 클래스를 사용하여 사용자의 리프레시 토큰 및 액세스 토큰 생성
        refresh = RefreshToken.for_user(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # 사용자 ID를 문자열로 처리
    class Meta:
        model = ResponseModel
        fields = ("__all__")

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedbackModel
        fields = ("__all__")