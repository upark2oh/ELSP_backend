from rest_framework import generics
from capstone.models import ResponseModel
from capstone.serializers import ResponseSerializer
from rest_framework.response import Response

class ResponseListCreateView(generics.ListCreateAPIView):
    queryset = ResponseModel.objects.all()
    serializer_class = ResponseSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class UserListView(generics.ListAPIView):
    serializer_class = ResponseSerializer

    def get_queryset(self):
        user = self.request.user  # 현재 요청을 보낸 사용자
        print(user)
        return ResponseModel.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data, content_type='application/json; charset=utf-8')