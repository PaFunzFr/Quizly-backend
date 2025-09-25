from django.urls import reverse
from app_quiz.models import Quiz
from django.contrib.auth import get_user_model
User = get_user_model()


def test_get_quizzes_valid(auth_client):
    url = reverse('quiz-list')
    response = auth_client.get(url)

    assert response.status_code == 200


def test_get_quizzes_requires_authentication(api_client):
    url = reverse('quiz-list')
    response = api_client.get(url)

    assert response.status_code == 401


def test_get_quiz_invalid_pk(auth_client):
    invalid_pk = 9999
    url = reverse('quiz-detail', kwargs={'pk': invalid_pk})
    response = auth_client.get(url)

    assert response.status_code == 404
    assert "No Quiz matches the given query." in str(response.data)


def test_quiz_detail_forbidden(auth_client, test_user, db, other_user_as_quiz_owner):

    quiz = Quiz.objects.create(
        owner=other_user_as_quiz_owner,
        title="Other User Quiz",
        description="This quiz is not owned by auth_client",
        video_url="dummyUrl",
    )

    # Try to access the quiz as authenticated user (username=testuser)
    url = reverse("quiz-detail", kwargs={"pk": quiz.pk})
    response = auth_client.get(url)

    assert response.status_code == 403
    assert "You do not have permission to perform this action." in str(response.data)