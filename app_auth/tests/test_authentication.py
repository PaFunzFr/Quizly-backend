import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

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


def test_registration(auth_client):
    url = reverse('register')
    payload = {
        "username": "uniqueuser",
        "password": "Password123",
        "confirmed_password": "Password123",
        "email": "unique@example.com"
    }
    response = auth_client.post(
        url,
        payload,
        format="json"
    )

    # Registration success
    assert response.status_code == 201
    assert response.data["detail"] == "User created successfully!"

    # User created?
    user = User.objects.filter(username="uniqueuser").first()
    assert user is not None
    assert user.email == "unique@example.com"


def test_login(auth_client):
    url = reverse('login') 
    payload = {
        "username": "testuser",
        "password": "Password123"
    }
    response = auth_client.post(
        url,
        payload,
        format="json"
    )

    # Login successful?
    assert response.status_code == 200
    assert "detail" in response.data
    assert response.data["detail"] == "Login successfully!"

    # Cookies created?
    cookies = response.cookies
    assert "access_token" in cookies
    assert "refresh_token" in cookies

    # Token set?
    assert cookies["access_token"].value != ""
    assert cookies["refresh_token"].value != ""


def test_logout(auth_client):
    url = reverse('logout') 
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data["detail"] == "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
    
    # check if cookies were deleted
    cookies = response.cookies

    assert cookies["access_token"].value == ""
    assert cookies["refresh_token"].value == ""

    assert cookies["access_token"]["max-age"] == 0
    assert cookies["refresh_token"]["max-age"] == 0


def test_refresh_success(auth_client_with_refresh):
    response = auth_client_with_refresh.post("/api/token/refresh/")
    assert response.status_code == 200
    assert response.data["detail"] == "Token refreshed"
    assert "access" in response.data

    # is cookie set?
    assert "access_token" in response.cookies
    assert response.cookies["access_token"].value != ""


def test_refresh_no_cookie(api_client):
    response = api_client.post("/api/token/refresh/")
    assert response.status_code == 401
    assert response.data["detail"] == "Refresh Token not found."


def test_refresh_invalid_cookie(api_client):
    api_client.cookies["refresh_token"] = "FAKETOKEN123"
    response = api_client.post("/api/token/refresh/")
    assert response.status_code == 401
    assert response.data["detail"] == "Refresh Token invalid"