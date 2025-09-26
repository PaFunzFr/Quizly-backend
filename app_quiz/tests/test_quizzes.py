from django.urls import reverse
from app_quiz.models import Quiz
from django.contrib.auth import get_user_model

User = get_user_model()


def test_get_quizzes_valid(auth_client):
    """
    Test retrieving the list of quizzes for an authenticated user.

    Verifies that:
    - The response status code is 200 (OK).
    - The user receives a list of their quizzes.
    """
    url = reverse('quiz-list')
    response = auth_client.get(url)

    assert response.status_code == 200


def test_get_quizzes_requires_authentication(api_client):
    """
    Test that listing quizzes requires authentication.

    Verifies that:
    - The response status code is 401 (Unauthorized) if no credentials are provided.
    """
    url = reverse('quiz-list')
    response = api_client.get(url)

    assert response.status_code == 401


def test_get_quiz_invalid_pk(auth_client):
    """
    Test retrieving a quiz with an invalid primary key.

    Verifies that:
    - The response status code is 404 (Not Found).
    - The response contains an error message indicating that the quiz does not exist.
    """
    invalid_pk = 9999
    url = reverse('quiz-detail', kwargs={'pk': invalid_pk})
    response = auth_client.get(url)

    assert response.status_code == 404
    assert "No Quiz matches the given query." in str(response.data)


def test_quiz_detail_forbidden(auth_client, test_user, db, other_user_as_quiz_owner):
    """
    Test that a user cannot access a quiz they do not own.

    Verifies that:
    - Attempting to retrieve another user's quiz returns a 403 (Forbidden) status.
    - The response contains an appropriate permission error message.
    """
    quiz = Quiz.objects.create(
        owner=other_user_as_quiz_owner,
        title="Other User Quiz",
        description="This quiz is not owned by auth_client",
        video_url="dummyUrl",
    )

    # Trying to access the quiz as authenticated (auth_client) user (username=testuser)
    url = reverse("quiz-detail", kwargs={"pk": quiz.pk})
    response = auth_client.get(url)

    assert response.status_code == 403
    assert "You do not have permission to perform this action." in str(response.data)