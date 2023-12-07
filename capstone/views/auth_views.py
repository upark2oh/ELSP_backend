from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from capstone.serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import logout
from rest_framework import generics

# 회원가입을 처리하는 뷰
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # 모든 사용자가 회원가입 요청을 할 수 있도록 허용
    permission_classes = (permissions.AllowAny,)

# 사용자 프로필을 조회하는 뷰
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    # 인증된 사용자만 접근 가능하도록 설정
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # 현재 요청을 보낸 사용자의 정보 반환
        return self.request.user

# 로그아웃을 처리하는 뷰
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        # 성공적으로 로그아웃되었음을 응답
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

# 회원탈퇴를 처리하는 뷰
class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)