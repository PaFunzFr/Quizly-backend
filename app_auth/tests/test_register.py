from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_registration(auth_client):
    """
    Test the user registration endpoint for successful account creation.

    This test verifies that:
    - The response status code is 201 (Created).
    - The response contains a success message indicating the user was created.
    - A new user is actually created in the database with the expected username and email.
    """

    url = reverse('register')
    payload = {
        "username": "uniqueuser",
        "password": "Password123",
        "confirmed_password": "Password123",
        "email": "unique@example.com"
    }
    response = auth_client.post(url, payload, format="json")

    # Registration success
    assert response.status_code == 201
    assert "User created successfully!" in str(response.data)

    # User created?
    user = User.objects.filter(username="uniqueuser").first()
    assert user is not None
    assert user.email == "unique@example.com"

