from django.urls import reverse
from app_quiz.models import Quiz
import json

from unittest.mock import patch
from contextlib import ExitStack


def test_create_quiz_requires_authentication(api_client):
    url = reverse("create-quiz")
    payload = {"url": "https://www.youtube.com/watch?v=anyId"}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 401


def test_create_quiz_invalid_url(auth_client):
    url = reverse("create-quiz")
    payload = {"url": "https://example.com/video"}

    response = auth_client.post(
        url,
        payload,
        format="json"
    )

    assert response.status_code == 400
    assert "Invalid YouTube URL" in str(response.data)


def test_create_quiz_invalid_json(auth_client):
    url = reverse("create-quiz")
    payload = {"url": "https://www.youtube.com/watch?v=validId"}

    # Mock download_and_transcribe and generateQuiz 
    with ExitStack() as stack:
        stack.enter_context(patch("app_quiz.api.views.download_and_transcribe", return_value="FAKE TRANSCRIPT"))
        stack.enter_context(patch("app_quiz.api.views.generateQuiz", return_value="NOT_JSON"))
        response = auth_client.post(url, payload, format="json")

    assert response.status_code == 500
    assert "Invalid JSON returned from Gemini" in str(response.data)
    assert response.data["raw"] == "NOT_JSON"



def test_create_quiz_valid_url(auth_client, test_user, quiz_dummy):
    url = reverse("create-quiz")
    payload = {"url": "https://www.youtube.com/watch?v=validId"}
    quiz_dummy_str = json.dumps(quiz_dummy)

    with ExitStack() as stack:
        stack.enter_context(patch("app_quiz.api.views.download_and_transcribe", return_value="FAKE TRANSCRIPT"))
        stack.enter_context(patch("app_quiz.api.views.generateQuiz", return_value=quiz_dummy_str))
        response = auth_client.post(url, payload, format="json")

    # print(response.data)
    assert response.status_code == 201

    # Quiz created?
    quiz = Quiz.objects.filter(owner=test_user).first()
    assert quiz is not None

    # Quiz Information set?
    assert quiz.title is not None
    assert quiz.description is not None

    # Quiz has (exactly 10) Questions?
    assert quiz.questions.count() == 10
