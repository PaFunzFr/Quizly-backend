from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
refresh_url = reverse("refresh")


def test_refresh_success(auth_client_with_refresh):
    response = auth_client_with_refresh.post(refresh_url)
    assert response.status_code == 200
    assert response.data["detail"] == "Token refreshed"
    assert "access" in response.data

    # is cookie set?
    assert "access_token" in response.cookies
    assert response.cookies["access_token"].value != ""


def test_refresh_no_cookie(api_client):
    response = api_client.post(refresh_url)
    assert response.status_code == 401
    assert response.data["detail"] == "Refresh Token not found."


def test_refresh_invalid_cookie(api_client):
    api_client.cookies["refresh_token"] = "FAKETOKEN123"
    response = api_client.post(refresh_url)
    assert response.status_code == 401
    assert response.data["detail"] == "Refresh Token invalid"