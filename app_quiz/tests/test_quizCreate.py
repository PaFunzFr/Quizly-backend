from django.urls import reverse
from app_quiz.models import Quiz
import json

from unittest.mock import patch
from contextlib import ExitStack


def test_create_quiz_requires_authentication(api_client):
    """
    Test that creating a quiz without authentication is forbidden.

    Verifies that:
    - The response status code is 401 (Unauthorized) when no credentials are provided.
    """
    url = reverse("create-quiz")
    payload = {"url": "https://www.youtube.com/watch?v=anyId"}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 401


def test_create_quiz_invalid_url(auth_client):
    """
    Test that creating a quiz with an invalid video URL returns an error.

    Verifies that:
    - The response status code is 400 (Bad Request).
    - The response contains an appropriate error message about invalid YouTube URL.
    """
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
    """
    Test handling of invalid JSON returned by the quiz generation AI.

    Mocks:
    - `download_and_transcribe` to return a fake transcript.
    - `generateQuiz` to return a non-JSON string.

    Verifies that:
    - The response status code is 500 (Internal Server Error).
    - The response contains an error message indicating invalid JSON.
    - The raw invalid output is included in the response.
    """
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
    """
    Test successful creation of a quiz from a valid YouTube URL.

    Mocks:
    - `download_and_transcribe` to return a fake transcript.
    - `generateQuiz` to return a valid quiz JSON string.

    Verifies that:
    - The response status code is 201 (Created).
    - A new quiz instance is created in the database for the authenticated user.
    - The quiz has a title, description, and exactly 10 associated questions.
    """
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
