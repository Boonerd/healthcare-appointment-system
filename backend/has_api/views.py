from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from datetime import datetime
import time
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from django.db import connection
from django.db.utils import OperationalError

from .serializers import UserSerializer, RegisterSerializer
from .utils.jwt import CustomTokenObtainPairSerializer
from .models import User


# Boiler plate for API response structure
class BaseAPIView(APIView):
    # to secure most endpoints
    permission_classes = [IsAuthenticated]

    def success_response(self, message="", data=None, status_code=200):
        return Response(
            {"success": True, "message": message, "data": data}, status=status_code
        )

    def error_response(self, message="", data=None, status_code=400):
        return Response(
            {"success": False, "message": message, "data": data}, status=status_code
        )


class TestAPI(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        current_time = datetime.now().isoformat()
        return self.success_response(message="API is okay", data={"time": current_time})


class DBAPI(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            start_time = time.perf_counter()

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            return self.success_response(
                message="Database is healthy", data={"query_time_ms": duration_ms}
            )

        except OperationalError as e:
            return self.error_response(
                message="Database connection failed",
                data={"error": str(e)},
                status_code=503,
            )


class UserRegisterView(BaseAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return self.success_response(
                data={"message": "User registered successfully"}, status_code=201
            )
        return self.error_response(data=serializer.errors, status_code=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return self.success_response(data=serializer.data)


class ActivateUserView(BaseAPIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, national_id):
        try:
            user = User.objects.get(national_id=national_id)
            user.is_active = True
            user.is_staff = True
            user.save()
            return self.success_response(message="User activated successfully.")
        except User.DoesNotExist:
            return self.error_response(message="User not found.", status_code=404)
