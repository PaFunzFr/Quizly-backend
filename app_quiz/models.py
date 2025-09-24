from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizes")
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=False, null=False)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_title = models.CharField(blank=False, null=False, max_length=200)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
