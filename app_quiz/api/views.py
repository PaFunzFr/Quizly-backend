from rest_framework import views, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsOwnerStaffOrAdmin
from .serializers import QuizSerializer, QuizDetailSerializer
from .utils import download_and_transcribe, generateQuiz

from app_quiz.models import Quiz, Question
from app_auth.api.views import CookieJWTAuthentication

from drf_spectacular.utils import extend_schema, OpenApiResponse



@extend_schema(
    description="Create a new quiz by providing a video URL. The system downloads, transcribes, and generates quiz questions.",
    request=QuizSerializer,
    responses={
        201: OpenApiResponse(description="Quiz created successfully."),
        400: OpenApiResponse(description="Invalid input data."),
        500: OpenApiResponse(description="Failed to generate quiz from transcript."),
    }
)
class QuizCreateView(views.APIView):
    """Endpoint to create a new quiz based on a video URL."""
    serializer_class = QuizSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a quiz by downloading video transcript and generating questions."""
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


@extend_schema(
    description="Retrieve a list of quizzes created by the authenticated user.",
    responses={
        200: OpenApiResponse(description="List of user's quizzes."),
        401: OpenApiResponse(description="Authentication credentials were not provided."),
    }
)
class QuizListView(generics.ListAPIView):
    """Endpoint to list all quizzes owned by the authenticated user."""
    serializer_class = QuizSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return quizzes owned by the authenticated user."""
        user = self.request.user
        queryset = Quiz.objects.filter(owner = user)
        return queryset


@extend_schema(
    description="Retrieve, update, or delete a specific quiz. Only the owner or authorized staff/admin can modify.",
    responses={
        200: OpenApiResponse(description="Quiz retrieved successfully."),
        401: OpenApiResponse(description="Authentication required."),
        403: OpenApiResponse(description="Permission denied."),
        404: OpenApiResponse(description="Quiz not found."),
    }
)
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Endpoint to retrieve, update, or delete a specific quiz."""
    serializer_class = QuizDetailSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerStaffOrAdmin]
    queryset = Quiz.objects.all()