import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Password123"
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def token_pair(test_user):
    refresh = RefreshToken.for_user(test_user)
    access = str(refresh.access_token)
    refresh = str(refresh)
    return {"access": access, "refresh": refresh}


@pytest.fixture
def auth_client(api_client, token_pair):
    api_client.cookies["access_token"] = token_pair["access"]
    api_client.cookies["refresh_token"] = token_pair["refresh"]
    return api_client


@pytest.fixture
def auth_client_with_refresh(test_user):
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.cookies["refresh_token"] = str(refresh)
    return client