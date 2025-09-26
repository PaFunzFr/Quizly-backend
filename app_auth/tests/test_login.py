from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_login(auth_client):
    """
    Test the user login endpoint for successful authentication and cookie creation.

    This test verifies that:
    - The response status code is 200 (OK).
    - The response contains a success message indicating login was successful.
    - Both 'access_token' and 'refresh_token' cookies are created.
    - The cookies contain non-empty JWT tokens.
    """

    url = reverse('login') 
    payload = {
        "username": "testuser",
        "password": "Password123"
    }
    response = auth_client.post(url, payload, format="json")

    # Login successful?
    assert response.status_code == 200
    assert "detail" in response.data
    assert "Login successfully!" in str(response.data)

    # Cookies created?
    cookies = response.cookies
    assert "access_token" in cookies
    assert "refresh_token" in cookies

    # Token set?
    assert cookies["access_token"].value != ""
    assert cookies["refresh_token"].value != ""


def test_logout(auth_client):
    """
    Test the user logout endpoint for successful token invalidation and cookie deletion.

    This test verifies that:
    - The response status code is 200 (OK).
    - The response contains a success message indicating logout.
    - Both 'access_token' and 'refresh_token' cookies are deleted.
    - The cookies' values are empty and their max-age is set to 0.
    """

    url = reverse('logout') 
    response = auth_client.post(url)
    
    assert response.status_code == 200
    assert "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid." in str(response.data)
    
    # check if cookies were deleted
    cookies = response.cookies

    assert cookies["access_token"].value == ""
    assert cookies["refresh_token"].value == ""

    assert cookies["access_token"]["max-age"] == 0
    assert cookies["refresh_token"]["max-age"] == 0
