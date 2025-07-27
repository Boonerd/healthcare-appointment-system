from .models import User, DoctorProfile, PatientProfile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "national_id",
            "phone_number",
            "role",
            "profile_pic",
            "is_active",
        ]
        read_only_fields = ["is_active", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "national_id",
            "phone_number",
            "password",
            "role",
        ]

    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        value_lower = value.lower()
        if value_lower not in valid_roles:
            raise serializers.ValidationError(
                f"Invalid role '{value}'. Must be one of: {valid_roles}"
            )
        return value_lower

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["user", "specialization", "license_number"]


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ["user", "age", "medical_history"]
