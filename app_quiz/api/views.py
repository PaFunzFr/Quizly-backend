from rest_framework import views, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsOwnerStaffOrAdmin
from .serializers import QuizSerializer, QuizDetailSerializer
from .utils import download_and_transcribe, generateQuiz
from app_quiz.models import Quiz, Question

from app_auth.api.views import CookieJWTAuthentication
# from threading import Thread

class QuizCreateView(views.APIView):
    serializer_class = QuizSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            transcript_text = download_and_transcribe(url)
            quiz_str = generateQuiz(transcript_text)

            import json
            try:
                quiz_json = json.loads(quiz_str)
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON returned from Gemini", "raw": quiz_str},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            quiz = Quiz.objects.create(
                owner=request.user,
                title=quiz_json.get("title", "No title set")[:80],
                description=quiz_json.get("description", "No Description set")[:200],
                video_url=url,
            )
            for q in quiz_json["questions"]:
                Question.objects.create(
                    quiz=quiz,
                    question_title=q["question_title"][:200],
                    question_options=q["question_options"],
                    answer=q["answer"][:200],
                )
            return Response(self.serializer_class(quiz).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         quiz = serializer.save()
    #         url = serializer.validated_data['video_url']
    #         t = Thread(target=download_and_transcribe, args=(url,))
    #         t.start()
    #         return Response({"status": "Task gestartet"}, status=status.HTTP_202_ACCEPTED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Quiz.objects.filter(owner = user)
        return queryset


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizDetailSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerStaffOrAdmin]
    queryset = Quiz.objects.all()