from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from datetime import datetime
import time
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from django.db import connection
from django.db.utils import OperationalError

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    AppointmentSerializer,
    DoctorAvailabilitySerializer,
)
from .utils.jwt import CustomTokenObtainPairSerializer
from .models import User, DoctorProfile, PatientProfile, Appointments


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
        role = request.data.get("role")

        if role == "doctor":
            specialization = request.data.get("specialization")
            license_number = request.data.get("license_number")

            if not specialization and not license_number:
                return Response(
                    {"error": "Doctor must have specialization and license number."},
                    status=400,
                )
        if role == "patient" or role == "" or not role:
            age = request.data.get("age")
            gender = request.data.get("gender")

            if not age and not gender:
                return Response(
                    {"error": "Patient must have age and gender"},
                    status=400,
                )
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == "doctor":  # type: ignore
                DoctorProfile.objects.create(
                    user=user,
                    specialization=request.data.get("specialization"),
                    license_number=request.data.get("license_number"),
                )
            if user.role == "patient":  # type: ignore
                PatientProfile.objects.create(
                    user=user,
                    age=request.data.get("age"),
                    gender=request.data.get("gender"),
                )
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


class DoctorListView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = User.objects.filter(role="doctor").select_related("doctor_profile")
        serializer = UserSerializer(doctors, many=True)
        return self.success_response(data=serializer.data)


class PatientListView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = User.objects.filter(role="patient").select_related("patient_profile")
        serializer = UserSerializer(patients, many=True)
        return self.success_response(data=serializer.data)


class ActivateUserView(BaseAPIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, national_id):
        try:
            user = User.objects.get(national_id=national_id)
            if user.is_active:
                return self.error_response(message="User is already active")
            user.is_active = True
            if user.role == "admin":
                user.is_staff = True
            user.is_staff = False
            user.save()
            return self.success_response(
                message=f"User with ID {user.national_id} activated successfully."
            )
        except User.DoesNotExist:
            return self.error_response(message="User not found.", status_code=404)


class CreateAppointmentView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # allow admins and doctors to create appointments for doctors not able to login
        # if user.role != "patient":
        serializer = AppointmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data, status_code=201)
        return self.error_response(data=serializer.errors)


class MyAppointmentsView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, "patient_profile"):
            appointments = Appointments.objects.filter(patient=user.patient_profile)
        elif hasattr(user, "doctor_profile"):
            appointments = Appointments.objects.filter(doctor=user.doctor_profile)
        else:
            appointments = Appointments.objects.none()

        serializer = AppointmentSerializer(appointments, many=True)
        return self.success_response(data=serializer.data)


class CancelAppointmentView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, appointment_id):
        user = request.user
        appointment = get_object_or_404(Appointments, pk=appointment_id)
        if appointment.status != "scheduled":
            return self.error_response(
                data={"error": "Only scheduled appointments can be cancelled."}
            )
        appointment.status = "cancelled"
        appointment.save()
        return self.success_response(
            data={"message": "Appointment cancelled successfully."}
        )


class DoctorAvailabilityView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "doctor":
            return self.error_response(
                data=f"Forbidden role: {request.user.role}", status_code=403
            )
        doctor = request.user.doctor_profile
        serializer = DoctorAvailabilitySerializer(doctor)
        return self.success_response(data=serializer.data)

    def patch(self, request):
        doctor = request.user.doctor_profile
        serializer = DoctorAvailabilitySerializer(
            doctor, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                data={"message": "Availability updated successfully."}
            )
        return self.error_response(data=serializer.errors)
