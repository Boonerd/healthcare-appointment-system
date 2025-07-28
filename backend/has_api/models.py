from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


class CustomUserManager(BaseUserManager):
<<<<<<< Updated upstream
    def create_user(self, email, national_id, password, role="patient", **extra_fields):
        if not email and not national_id:
            raise ValueError("Users must have a national ID or email")

=======
    def create_user(
        self,
        email: str,
        national_id: str,
        password: str,
        full_name: str,
        role: str = "patient",
        **extra_fields,
    ):
        if not email and not national_id and not full_name:
            raise ValueError("Users must have a national ID, full name and email")
>>>>>>> Stashed changes
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            email=email,
            national_id=national_id,
            role=role,
            full_name=full_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, national_id, password, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, national_id, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    )
<<<<<<< HEAD
    national_id = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=50, unique=True)
=======
    national_id = models.CharField(
        max_length=12, null=False, unique=True, db_index=True
    )
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    full_name = models.CharField(max_length=50, null=False, unique=True)
>>>>>>> 0929b5e (Change token expiry to 1hr)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")
    profile_pic = models.URLField(default="https://shorturl.at/cA9tj", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "national_id"
    REQUIRED_FIELDS = ["email", "full_name", "phone_number"]

    objects = CustomUserManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.strip().title()
        super().save(*args, **kwargs)


class User(AbstractUser):
    objects = CustomUserManager()


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=20, null=False)
    license_number = models.CharField(max_length=20, null=False)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Doctor: {self.user.full_name}"


class PatientProfile(models.Model):
<<<<<<< Updated upstream
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
=======
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=6, null=False, default="M|F")
>>>>>>> Stashed changes
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.full_name}"


<<<<<<< Updated upstream
=======
class Appointments(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="scheduled"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        appointment_datetime = datetime.combine(
            self.appointment_date, self.appointment_time
        )
        if appointment_datetime <= timezone.now():
            raise ValidationError(
                "Appointment must be scheduled for a future date and time."
            )
        if not self.doctor.availability:
            raise ValidationError("Doctor is not available for appointments.")

    def __str__(self):
        return f"{self.patient.user.full_name} with Dr. {self.doctor.user.full_name} on {self.appointment_date} at {self.appointment_time}"


# only 1 admin per clinic, admin is activated by super user, then the admin goes on to activate doctors and patients
>>>>>>> Stashed changes
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.CharField(max_length=20)

    def clean(self):
        if not self.pk and AdminProfile.objects.count() >= 2:
            raise ValidationError("Only 2 admins are allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.user.full_name} @ {self.center}"


class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name='appointments_as_patient', on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('cancelled', 'Cancelled')], default='scheduled')

    def __str__(self):
        return f"{self.patient.full_name} → {self.doctor.full_name} at {self.appointment_time}"
