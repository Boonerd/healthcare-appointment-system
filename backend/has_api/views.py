import time
from datetime import datetime

from django.db import connection
from django.db.utils import OperationalError

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Appointment
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    AppointmentSerializer,
)
from .utils.jwt import CustomTokenObtainPairSerializer


class BaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def success_response(self, message="", data=None, status_code=200):
        return Response(
            {"success": True, "message": message, "data": data},
            status=status_code,
        )

    def error_response(self, message="", data=None, status_code=400):
        return Response(
            {"success": False, "message": message, "data": data},
            status=status_code,
        )


class TestAPI(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return self.success_response(message="API is okay", data={"time": datetime.now().isoformat()})


class DBAPI(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            start = time.perf_counter()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            duration = round((time.perf_counter() - start) * 1000, 2)
            return self.success_response("Database is healthy", {"query_time_ms": duration})
        except OperationalError as e:
            return self.error_response("DB connection failed", {"error": str(e)}, 503)


class UserRegisterView(BaseAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response("User registered successfully", status_code=201)
        return self.error_response(data=serializer.errors, status_code=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(BaseAPIView):
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
            return self.success_response("User activated successfully.")
        except User.DoesNotExist:
            return self.error_response("User not found.", status_code=404)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        doctor = request.data.get("doctor")
        appointment_time = request.data.get("appointment_time")

        if Appointment.objects.filter(doctor=doctor, appointment_time=appointment_time, status="scheduled").exists():
            return Response(
                {"error": "Doctor is not available at this time"},
                status=status.HTTP_409_CONFLICT,
            )

        return super().create(request, *args, **kwargs)
