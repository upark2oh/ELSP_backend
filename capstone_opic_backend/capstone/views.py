from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .models import ImpromptuQuiz, SurveyQuiz, Profile
from .serializers import ImpromptuQuizSerializer, SurveyQuizSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer  # Corrected the typo
from .permissions import CustomReadOnly


@api_view(['GET'])
def ImpromtumQuizAPI(request, id):
    quiz = ImpromptuQuiz.objects.get(id=id)
    serializer = ImpromptuQuizSerializer(quiz)  # Correct serializer
    return Response(serializer.data, content_type='application/json; charset=utf-8')

    
@api_view(['GET'])
def SurveyQuizAPI(request, id):
    quiz = SurveyQuiz.objects.get(id=id)
    serializer = SurveyQuizSerializer(quiz)  # Serialize multiple objects
    return Response(serializer.data, content_type='application/json; charset=utf-8')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값인 token을 받아온다.
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]