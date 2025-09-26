import re #regex
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Handles user creation with password confirmation, validates that the passwords match,
    and ensures the email is unique. Passwords are write-only to prevent exposure.
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirmed_password'
            ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """
        Ensure that 'password' and 'confirmed_password' fields match.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        if attrs.get("password") != attrs.get("confirmed_password"):
            raise serializers.ValidationError({"confirmed_password": "Passwords do not match"})
        return attrs

    def validate_email(self, value):
        """
        Ensure the provided email address is unique.

        Raises:
            serializers.ValidationError: If the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already used')
        return value


    def create(self, validated_data):
        """
        Create and return a new user instance.

        Sets the user's password securely using Django's set_password method.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login.

    Validates user credentials and returns JWT tokens (access and refresh).
    Ensures that the username exists and the password is correct.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 


    def validate(self, attrs):
        """
        Validate the provided username and password.

        Raises:
            serializers.ValidationError: If the user does not exist or the password is incorrect.

        Returns:
            dict: JWT token data (access and refresh tokens) after successful validation.
        """
        username = attrs.get("username")
        password = attrs.get("password") 

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User or Password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid User or Password")
        
        data = super().validate({"username": user.username, "password": password})
        return data