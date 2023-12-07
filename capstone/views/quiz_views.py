from rest_framework.response import Response
from rest_framework.decorators import api_view
from capstone.models import ImpromptuQuiz, SurveyQuiz, SurveyTopicbyUser, ImpromptuTopicbyUser
from capstone.serializers import ImpromptuQuizSerializer, SurveyQuizSerializer, SurveyTopicbyUserSerializer, ImpromptuTopicbyUserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
import random

#사용자가 선택한 주제 중에서 랜덤하게 퀴즈를 하나 뽑아서 반환합니다. (돌발질문)
class ImpromtumQuizAPI(generics.ListAPIView):
    serializer_class = ImpromptuQuizSerializer
    def get_queryset(self):
        user = self.request.user
        return  list(ImpromptuTopicbyUser.objects.filter(user=user).values_list('topic', flat=True))
    
    def list(self, request, *args, **kwargs):
        quiz = ImpromptuQuiz.objects.filter(topic__in=self.get_queryset())
        selected_quiz = random.choice(quiz)
        serializer = self.serializer_class(selected_quiz)  # Correct serializer
        return Response(serializer.data, content_type='application/json; charset=utf-8')

#사용자가 선택한 주제 중에서 랜덤하게 퀴즈를 하나 뽑아서 반환합니다. (선택질문)
class SurveyQuizAPI(generics.ListAPIView):
    serializer_class = SurveyQuizSerializer

    def get_queryset(self):
        user = self.request.user
        return  list(SurveyTopicbyUser.objects.filter(user=user).values_list('topic', flat=True))

    def list(self, request, *args, **kwargs):
        quiz = SurveyQuiz.objects.filter(topic__in=self.get_queryset())
        selected_quiz = random.choice(quiz)
        serializer = self.serializer_class(selected_quiz)  # Correct serializer
        print(serializer.data)
        return Response(serializer.data, content_type='application/json; charset=utf-8')

#선택주제의 모든 주제를 반환합니다. 
class SurveyTopicListView(APIView):
    def get(self, request, format=None):
        survey_topics = SurveyQuiz.objects.all()
        topics_set = set([survey.topic for survey in survey_topics])
        unique_topics = list(topics_set)
        return Response(unique_topics, content_type='application/json; charset=utf-8')

#돌발주제의 모든 주제를 반환합니다. 
class ImpromtuTopicListView(APIView):
    def get(self, request, format=None):
        impromptu_topics = ImpromptuQuiz.objects.all()
        topics_set = set([impromptu.topic for impromptu in impromptu_topics])
        unique_topics = list(topics_set)
        #print(unique_topics)
        return Response(unique_topics, content_type='application/json; charset=utf-8', status=200)

#사용자가 선택한 선택 주제의 주제를 조회합니다.
class SurveyTopicByUserListView(generics.ListAPIView):
    serializer_class = SurveyTopicbyUserSerializer

    def get_queryset(self):
        user = self.request.user  # 현재 요청을 보낸 사용자
        return SurveyTopicbyUser.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

#사용자가 선택한 돌발 주제의 주제를 조회합니다.
class ImpromptuTopicByUserListView(generics.ListAPIView):
    serializer_class = ImpromptuTopicbyUserSerializer

    def get_queryset(self):
        user = self.request.user  # 현재 요청을 보낸 사용자
        print(user)
        return ImpromptuTopicbyUser.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
#사용자가 선택 질문에서 주제를 선택할 수 있도록 하는 API를 제공합니다.
class SurveyTopicCreateView(generics.CreateAPIView):
    serializer_class =  SurveyTopicbyUserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        topic = serializer.validated_data['topic']

        # 중복 체크
        if (SurveyTopicbyUser.objects.filter(user=user, topic=topic).exists()==True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 중복이 아닌 경우 저장
        serializer.save(user=user)
        return Response(status=status.HTTP_201_CREATED)
    
#사용자가 선택 질문에서 정 토픽을 삭제 하는 API를 제공합니다.
class SurveyTopicDeleteView(APIView):
    def post(self, request, format=None):
        # 클라이언트에서 전송한 선택된 토픽
        selected_topic = request.data.get('topic', None)

        # 현재 사용자의 모든 토픽 가져오기
        all_user_topics = SurveyTopicbyUser.objects.filter(user=request.user)
        
        # 선택된 토픽 삭제
        deleted = False  # 토픽이 삭제되었는지 여부를 나타내는 플래그

        for user_topic in all_user_topics:
            if user_topic.topic == selected_topic:
                # 선택된 토픽과 일치하는 경우 삭제
                user_topic.delete()
                deleted = True

        if deleted:
            # 토픽이 삭제된 경우 성공적인 응답
            return Response(status=status.HTTP_200_OK)
        else:
            # 선택된 토픽이 없는 경우 에러 응답
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

#사용자가 돌발 질문에서 주제를 선택할 수 있도록 하는 API를 제공합니다.
class ImpromptuTopicCreateView(generics.CreateAPIView):
    serializer_class =  ImpromptuTopicbyUserSerializer

    def perform_create(self, serializer):
        user = self.request.user
        topic = serializer.validated_data['topic']

        # 중복 체크
        if (ImpromptuTopicbyUser.objects.filter(user=user, topic=topic).exists()==True):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 중복이 아닌 경우 저장
        serializer.save(user=user)
        return Response(status=status.HTTP_201_CREATED)
    
#사용자가 돌발 질문에서 정 토픽을 삭제 하는 API를 제공합니다.
class ImpromptuTopicDeleteView(APIView):
    def post(self, request, format=None):
        # 클라이언트에서 전송한 선택된 토픽
        selected_topic = request.data.get('topic', None)

        # 현재 사용자의 모든 토픽 가져오기
        all_user_topics = ImpromptuTopicbyUser.objects.filter(user=request.user)
        
        # 선택된 토픽 삭제
        deleted = False  # 토픽이 삭제되었는지 여부를 나타내는 플래그

        for user_topic in all_user_topics:
            if user_topic.topic == selected_topic:
                # 선택된 토픽과 일치하는 경우 삭제
                user_topic.delete()
                deleted = True

        if deleted:
            # 토픽이 삭제된 경우 성공적인 응답
            return Response(status=status.HTTP_200_OK)
        else:
            # 선택된 토픽이 없는 경우 에러 응답
            return Response(status=status.HTTP_400_BAD_REQUEST)