<<<<<<< Updated upstream
from rest_framework import serializers
from .models import User, DoctorProfile, PatientProfile, Appointment
=======
from .models import User, DoctorProfile, PatientProfile, Appointments
from rest_framework import serializers
from datetime import datetime
from django.utils import timezone


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["user", "specialization", "license_number"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["user", "age", "medical_history"]
>>>>>>> Stashed changes


class UserSerializer(serializers.ModelSerializer):
    doctor_profile = DoctorProfileSerializer(read_only=True)
    patient_profile = PatientProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
<<<<<<< Updated upstream
            "id", "email", "full_name", "national_id", "phone_number",
            "role", "profile_pic", "is_active"
=======
            "email",
            "full_name",
            "national_id",
            "phone_number",
            "role",
            "profile_pic",
            "doctor_profile",
            "patient_profile",
>>>>>>> Stashed changes
        ]
        read_only_fields = ["national_id", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "full_name", "national_id", "phone_number", "password", "role"
        ]

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value.lower() not in valid_roles:
            raise serializers.ValidationError(f"Invalid role. Must be one of: {valid_roles}")
        return value.lower()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = "__all__"
        read_only_fields = ["status", "patient", "created_at"]

    def validate(self, data):
        doctor = data["doctor"]
        appointment_date = data["appointment_date"]
        appointment_time = data["appointment_time"]

        if timezone.is_naive(appointment_time):
            appointment_time = timezone.make_aware(appointment_time)

        appointment_datetime = datetime.combine(appointment_date, appointment_time)  # type: ignore
        if appointment_datetime <= timezone.now():
            raise serializers.ValidationError("Appointment must be in the future.")

        if not doctor.availability:
            raise serializers.ValidationError("Doctor is not available.")
        return data

    def create(self, validated_data):
        patient = self.context["request"].user.patient_profile
        validated_data["patient"] = patient
        return super().create(validated_data)


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
<<<<<<< Updated upstream
        fields = ["user", "specialization", "license_number"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["user", "age", "medical_history"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
=======
        fields = ["availability"]
>>>>>>> Stashed changes
