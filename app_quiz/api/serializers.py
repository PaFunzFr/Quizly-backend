from rest_framework import serializers
from urllib.parse import urlparse, parse_qs

from app_quiz.models import Quiz, Question

class QuestionNestedSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz questions used as a nested representation within a quiz.

    Includes question title, possible options, correct answer, and timestamps.
    """
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

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing quizzes.

    Supports nested questions read-only and accepts a video URL to generate the quiz.
    Validates YouTube URLs and normalizes them to standard format.
    """
    questions = QuestionNestedSerializer(many=True, read_only=True)
    url = serializers.URLField(write_only=True)
    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions',
            'url'
        ]
        read_only_fields = ["id", "title", "video_url", "description", "created_at", "updated_at", "questions"]

    def validate_url(self, value):
        """
        Validate the provided YouTube video URL.

        Ensures the URL is either a standard YouTube link or a shortened youtu.be link.
        Extracts the video ID and returns a normalized YouTube URL.

        Raises:
            serializers.ValidationError: If the URL is empty or invalid.
        """
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
    
class QuizDetailSerializer(QuizSerializer):
    """
    Serializer for detailed view and update of a quiz.

    Provides read-only nested questions and prevents modification of video URL, question list, and ID.
    """
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
        read_only_fields = ["id", "created_at", "updated_at", "questions", "video_url"]

    def validate(self, attrs):
        """
        Validate that forbidden fields are not updated.

        Forbidden fields: 'video_url', 'questions', 'id'.

        Raises:
            serializers.ValidationError: If any forbidden field is present in the input data.
        """
        forbidden_fields = ["video_url", "questions", "id"]
        for field in forbidden_fields:
            if field in self.initial_data:
                raise serializers.ValidationError(
                    {field: "This field cannot be updated."}
                )
        return super().validate(attrs)