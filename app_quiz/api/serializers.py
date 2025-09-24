from rest_framework import serializers
from urllib.parse import urlparse, parse_qs

from app_quiz.models import Quiz, Question

class QuestionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'question_title',
            'question_options',
            'answer',
            'created_at',
            'updated_at'
        ]

class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions'
        ]
        read_only_fields = ["id", "title", "description", "created_at", "updated_at", "questions"]

    def validate_video_url(self, value):

        if not value:
            raise serializers.ValidationError("Video URL cannot be empty.")

        video_id = None
        parsed_url = urlparse(value)

        if parsed_url.netloc in ('www.youtube.com', 'youtube.com'):
        
            if parsed_url.path == '/watch':
                query_params = parse_qs(parsed_url.query)
                # get video id from v parameter
                video_id = query_params.get('v', [None])[0]

        elif parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path.lstrip('/')

        if not video_id:
            raise serializers.ValidationError(
                "Invalid YouTube URL. Please use a 'www.youtube.com/watch?v=...' or 'youtu.be/...' link."
            )

        # return normalized youtube url
        return f"https://www.youtube.com/watch?v={video_id}"