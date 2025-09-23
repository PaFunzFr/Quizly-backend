import re #regex
from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_repeated_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already used')
        return value

    def save(self):
        pw = self.validated_data['password']
        email = self.validated_data['email']

        # user specific part of email and clean it up
        local_part = email.split('@')[0]
        clean_part = re.sub(r'[^a-zA-Z0-9]', '', local_part)

        count = User.objects.count() + 1
        # generated username extracted from email
        gen_username = f"{clean_part}{count}"
        account = User(
            email=email,
            username=gen_username
        )
        account.set_password(pw)
        account.save()
        return account
    

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    """ make username unrequired """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "username"in self.fields:
            self.fields.pop("username")


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User or Password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid User or Password")
        
        data = super().validate({"username": user.username, "password": password})
        return data