import re #regex
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
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
            # 'username' : {read_only: True}
        }

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirmed_password"):
            raise serializers.ValidationError({"confirmed_password": "Passwords do not match"})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already used')
        return value


    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # def save(self):
    #     pw = self.validated_data['password']
    #     self.validated_data.pop("confirmed_password")
    #     email = self.validated_data['email']
    #     username = self.validated_data['username']

        # user specific part of email and clean it up
        # if not username:
        #     local_part = email.split('@')[0]
        #     clean_part = re.sub(r'[^a-zA-Z0-9]', '', local_part)
        #     if not clean_part:
        #         clean_part = "user"
        #     count = User.objects.count() + 1

            # generated username extracted from email
            # username = f"{clean_part}{count}"

        # return User.objects.create_user(
        #     username=username,
        #     email=email,
        #     password=pw
        # )
    



class LoginSerializer(TokenObtainPairSerializer):
    #email = serializers.EmailField() # Login with email and password
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) # change with email

    # needed for email login
    # """ make username unrequired """
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     if "username"in self.fields:
    #         self.fields.pop("username")


    def validate(self, attrs):
        #email = attrs.get("email") # login with email and password
        username = attrs.get("username")
        password = attrs.get("password") # change with email

        try:
            # user = User.objects.get(email=email) # login with email and password
            user = User.objects.get(username=username) # change with email
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User or Password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid User or Password")
        
        data = super().validate({"username": user.username, "password": password})
        return data