from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

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

