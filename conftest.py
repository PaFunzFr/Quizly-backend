import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def test_user(db):
    """
    Fixture to create a test user.

    Returns:
        User: A newly created user instance with predefined username, email, and password.
    """
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Password123"
    )
    return user


@pytest.fixture
def other_user_as_quiz_owner():
    """
    Fixture to create another user who can act as a quiz owner.

    Returns:
        User: A user instance different from the primary test user.
    """
    user = User.objects.create_user(
        username="other",
        email="other@example.com",
        password="Password123"
    )
    return user


@pytest.fixture
def api_client():
    """
    Fixture to provide an unauthenticated DRF APIClient instance.

    Returns:
        APIClient: DRF test client without authentication credentials.
    """
    return APIClient()


@pytest.fixture
def token_pair(test_user):
    """
    Fixture to generate JWT access and refresh tokens for a given user.

    Args:
        test_user (User): The user for whom tokens are generated.

    Returns:
        dict: Dictionary containing 'access' and 'refresh' tokens as strings.
    """
    refresh = RefreshToken.for_user(test_user)
    access = str(refresh.access_token)
    refresh = str(refresh)
    return {"access": access, "refresh": refresh}


@pytest.fixture
def auth_client(api_client, token_pair):
    """
    Fixture to provide an authenticated APIClient using JWT cookies.

    Args:
        api_client (APIClient): The DRF test client.
        token_pair (dict): Dictionary containing 'access' and 'refresh' JWT tokens.

    Returns:
        APIClient: APIClient with JWT cookies set for authentication.
    """
    api_client.cookies["access_token"] = token_pair["access"]
    api_client.cookies["refresh_token"] = token_pair["refresh"]
    return api_client


@pytest.fixture
def auth_client_with_refresh(test_user):
    """
    Fixture to provide an APIClient with only the refresh token set in cookies.

    Useful for testing token refresh endpoints.

    Args:
        test_user (User): The user for whom the refresh token is generated.

    Returns:
        APIClient: APIClient with 'refresh_token' cookie set.
    """
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.cookies["refresh_token"] = str(refresh)
    return client


@pytest.fixture
def quiz_dummy():
    """
    Fixture to provide a dummy quiz in JSON format.

    The dummy quiz includes:
    - A title and description.
    - A valid video URL.
    - Exactly 10 questions, each with 4 options and a correct answer.

    Returns:
        dict: JSON-like dictionary representing a quiz.
    """
    dummy_json = {
        "title": "Test Quiz",
        "description": "This is a dummy quiz for testing purposes.",
        "video_url": "https://www.youtube.com/watch?v=validId",
        "questions": [
            {
                "question_title": f"Test question {i+1}?",
                "question_options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "answer": "Option A"
            } for i in range(10)
        ]
    }
    return dummy_json