from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views.quiz_views import(
    ImpromtumQuizAPI, 
    SurveyQuizAPI,
    SurveyTopicCreateView,
    SurveyTopicByUserListView,
    SurveyTopicDeleteView,
    SurveyTopicByUserListView,
    ImpromtuTopicListView,
    SurveyTopicListView,
    ImpromtuTopicListView,
    ImpromptuTopicByUserListView,
    ImpromptuTopicCreateView,
    ImpromptuTopicDeleteView,
)
from .views.auth_views import RegisterView, UserProfileView, LogoutView, UserDeleteAPIView
from .views.corrected_response_views import CorrectionView, AudioUploadView, SimilarityView
from .views.result_views import ResponseListCreateView, UserListView, UserFeedbackView, DeleteItemView

urlpatterns = [
    #특정 질문 조회
    path('impromptu/', ImpromtumQuizAPI.as_view(), name='impromptu-quiz-list'),
    path('survey/', SurveyQuizAPI.as_view(), name='survey-quiz-list'),

    #계정 관련 URL
    path('register/', RegisterView.as_view(), name='register'), 
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #토큰 유효성 확인 

    #jwt
    path('api-jwt-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-jwt-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-jwt-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    #사용자가 선택한 선택 질문 주제 조회/생성/삭제
    path('user-survey-topics-select/', SurveyTopicByUserListView.as_view(), name='user-survey-topics-select'),
    path('user-survey-topic-create/', SurveyTopicCreateView.as_view(), name='user-topic-create'),
    path('user-survey-topic-delete/', SurveyTopicDeleteView.as_view(), name='user-topic-delete'),

    #사용자가 선택한 돌발 질문 주제 조회/생성/삭제
    path('user-impromptu-topics-select/', ImpromptuTopicByUserListView.as_view(), name='user-impromptu-topics-select'),
    path('user-impromptu-topic-create/', ImpromptuTopicCreateView.as_view(), name='user-topic-create'),
    path('user-impromptu-topic-delete/', ImpromptuTopicDeleteView.as_view(), name='user-topic-delete'),

    #모든 선택 질문 조회
    path('all-survey-topics/', SurveyTopicListView.as_view(), name='survey-topic-list'),
    path('all-impromptu-topics/', ImpromtuTopicListView.as_view(), name='impromptu-topic-list'),

    #수정된 질문 반환
    path('get-corrected-response/', CorrectionView.as_view(), name='get-corrected-response'),
    path('get-similarity/', SimilarityView.as_view(), name='get-similarity'),
    path('upload-audio/', AudioUploadView.as_view(), name='audio-upload'),

    #답변 저장
    path('responses/', ResponseListCreateView.as_view(), name='response-list-create'),
    path('list-page/', UserListView.as_view(), name='list-page'),
    path('delete-item/', DeleteItemView.as_view(), name='delete-page'),
    path('feedback/', UserFeedbackView.as_view(), name='get-user-feedback'),
]