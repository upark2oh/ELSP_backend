from rest_framework import generics
from capstone.models import ResponseModel, UserFeedbackModel
from capstone.serializers import ResponseSerializer, UserFeedbackSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
        #print(user)
        return ResponseModel.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        #print(serializer.data)
        return Response(serializer.data, content_type='application/json; charset=utf-8')

class DeleteItemView(APIView):
    def post(self, request, format=None):
        # 클라이언트에서 전송한 선택된 토픽
        selected_item_date = request.data.get('current_date', None)

        # 현재 사용자의 모든 토픽 가져오기
        all_user_items = ResponseModel.objects.filter(user=request.user, current_date=selected_item_date)
        
        # 선택된 토픽 삭제
        deleted = False  # 토픽이 삭제되었는지 여부를 나타내는 플래그

        for item in all_user_items:
            # 선택된 토픽과 일치하는 경우 삭제
            item.delete()
            deleted = True

        if deleted:
            # 토픽이 삭제된 경우 성공적인 응답
            return Response(status=status.HTTP_200_OK)
        else:
            # 선택된 토픽이 없는 경우 에러 응답
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserFeedbackView(generics.ListCreateAPIView):
    queryset= UserFeedbackModel.objects.all()
    serializer_class = UserFeedbackSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


