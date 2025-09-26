from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    """
    Model representing a Quiz created by a user.

    Attributes:
        owner (ForeignKey): The user who owns the quiz.
        title (CharField): The title of the quiz (max 80 characters).
        description (CharField): A brief description of the quiz (max 200 characters).
        created_at (DateTimeField): Timestamp when the quiz was created.
        updated_at (DateTimeField): Timestamp when the quiz was last updated.
        video_url (URLField): URL of the video associated with the quiz.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizes")
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=False, null=False)

class Question(models.Model):
    """
    Model representing a Question belonging to a Quiz.

    Attributes:
        quiz (ForeignKey): The quiz this question belongs to.
        question_title (CharField): The text of the question (max 200 characters).
        question_options (JSONField): A list of answer options.
        answer (CharField): The correct answer to the question.
        created_at (DateTimeField): Timestamp when the question was created.
        updated_at (DateTimeField): Timestamp when the question was last updated.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_title = models.CharField(blank=False, null=False, max_length=200)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
