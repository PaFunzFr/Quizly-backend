from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
refresh_url = reverse("refresh")


def test_refresh_success(auth_client_with_refresh):
    """
    Test that a valid refresh token cookie successfully refreshes the access token.

    This test verifies that:
    - The response status code is 200 (OK).
    - The response contains a success message and a new access token.
    - The 'access_token' cookie is set and not empty.
    """
    
    response = auth_client_with_refresh.post(refresh_url)
    assert response.status_code == 200
    assert "Token refreshed" in str(response.data)
    assert "access" in response.data

    # is cookie set?
    assert "access_token" in response.cookies
    assert response.cookies["access_token"].value != ""


def test_refresh_no_cookie(api_client):
    """
    Test that a refresh attempt without a refresh token cookie fails.

    This test verifies that:
    - The response status code is 401 (Unauthorized).
    - The response contains an appropriate error message indicating the refresh token is missing.
    """

    response = api_client.post(refresh_url)
    assert response.status_code == 401
    assert "Refresh Token not found." in str(response.data)


def test_refresh_invalid_cookie(api_client):
    """
    Test that a refresh attempt with an invalid refresh token cookie fails.

    This test verifies that:
    - The response status code is 401 (Unauthorized).
    - The response contains an appropriate error message indicating the refresh token is invalid.
    """

    api_client.cookies["refresh_token"] = "FAKETOKEN123"
    response = api_client.post(refresh_url)
    assert response.status_code == 401
    assert "Refresh Token invalid" in str(response.data)