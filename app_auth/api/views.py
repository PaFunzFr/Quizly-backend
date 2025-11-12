from rest_framework import status
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema, OpenApiResponse

class CookieJWTAuthentication(JWTAuthentication):
    """Authenticate user via JWT stored in cookies."""
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None  # no Token => not authenticated
        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token")
        
@extend_schema(
    description="Register a new user.",
    request=RegistrationSerializer,
    responses={
        201: OpenApiResponse(description="User created successfully."),
        400: OpenApiResponse(description="Invalid registration data."),
    }
)
class RegistrationView(APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            """Create a new user account."""
            serializer.save() 
            return Response(
                {"detail": "User created successfully!"},
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        

@extend_schema(
    description="Login with username and password. Returns JWT tokens and user info.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="Login successful. Tokens set in cookies."),
        401: OpenApiResponse(description="Invalid credentials."),
    }
)
class LoginView(TokenObtainPairView):
    """User login endpoint using JWT."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Authenticate user and set JWT cookies."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get user information after validation
        user = serializer.user

        # get both tokens
        refresh = serializer.validated_data["refresh"] # get refresh token
        access = serializer.validated_data["access"] # get access token

        response = Response(
            {
            "detail":"Login successfully!",
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
            samesite = "None"
        )

        response.set_cookie(
            key = "refresh_token",
            value = str(refresh),
            httponly = True,
            secure = True,
            samesite = "None"
        )

        return response
    

@extend_schema(
    description="Refresh access token using refresh token stored in cookies.",
    responses={
        200: OpenApiResponse(description="Access token refreshed."),
        401: OpenApiResponse(description="Refresh token missing or invalid."),
    }
)
class CookieTokenRefreshView(TokenRefreshView):
    """Refresh JWT access token via cookie."""
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        """Refresh access token."""
        if refresh_token is None:
            return Response(
                {"detail":"Refresh Token not found."}, status=status.HTTP_401_UNAUTHORIZED,
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

        response = Response(
            {
                "detail":"Token refreshed",
                "access": access_token
            }
        )

        response.set_cookie(
            key = "access_token",
            value = access_token,
            httponly = True,
            secure = True,
            samesite = "None"
        )

        return response
    

@extend_schema(
    description="Logout user and delete JWT cookies.",
    responses={
        200: OpenApiResponse(description="User logged out successfully."),
    }
)
class LogoutView(APIView):
    """Logout endpoint, clears JWT cookies."""
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user and invalidate tokens."""
        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response