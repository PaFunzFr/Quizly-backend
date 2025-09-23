from rest_framework import views
from rest_framework.response import Response

from .serializers import QuizCreateSerializer

class QuizCreateView(views.APIView):
    serializer_class = QuizCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)