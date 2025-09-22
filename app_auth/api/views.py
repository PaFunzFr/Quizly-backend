from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save() 
            return Response(
                {"detail": "User created successfully!"},
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        

class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get user information after validation
        user = serializer.user

        # get both tokens
        refresh = serializer.validated_data["refresh"] # get refresh token
        access = serializer.validated_data["access"] # get access token

        response = Response(
            {
            "detail":"Login successful",
            "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email
                }
            }
        )

        response.set_cookie(
            key = "access_token",
            value = str(access),
            httponly = True,
            secure = True,
            samesite = "Lax"
        )

        response.set_cookie(
            key = "refresh_token",
            value = str(refresh),
            httponly = True,
            secure = True,
            samesite = "Lax"
        )

        return response
    
    
class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail":"Refresh Token not found."}, status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data = {"refresh": refresh_token}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {"detail":"Refresh Token invalid"}, status=status.HTTP_401_UNAUTHORIZED,
            )
        
        access_token = serializer.validated_data.get("access")

        response = Response({"message":"Token refreshed"})

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            secure = True,
            samesite = "Lax"
        )

        return response
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        
        # delete cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response