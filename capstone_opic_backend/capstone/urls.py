from django.urls import path, include
from .views import ImpromtumQuizAPI,  SurveyQuizAPI, RegisterView, LoginView, ProfileView

urlpatterns = [
    path('impromptu/<int:id>/', ImpromtumQuizAPI),
    path('survey/<int:id>', SurveyQuizAPI),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
]