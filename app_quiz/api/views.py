from rest_framework import views, status
from rest_framework.response import Response

from .serializers import QuizCreateSerializer
from .tasks import download_and_transcribe, createQuiz

# from threading import Thread

class QuizCreateView(views.APIView):
    serializer_class = QuizCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['video_url']
            transcript_text = download_and_transcribe(url)
            quiz_str = createQuiz(transcript_text)

            import json
            try:
                quiz_json = json.loads(quiz_str)
            except json.JSONDecodeError as e:
                return Response(
                    {"error": "Invalid JSON returned from Gemini", "raw": quiz_str},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(quiz_json, status=status.HTTP_200_OK)
        
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


