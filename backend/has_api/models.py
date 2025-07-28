from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, national_id, password, role="patient", **extra_fields):
        if not email and not national_id:
            raise ValueError("Users must have a national ID or email")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            email=email,
            national_id=national_id,
            role=role,
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
    national_id = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")
    profile_pic = models.URLField(default="https://shorturl.at/cA9tj", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "national_id"
    REQUIRED_FIELDS = ["email", "full_name"]

    objects = CustomUserManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.strip().title()
        super().save(*args, **kwargs)


class User(AbstractUser):
    objects = CustomUserManager()


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Doctor: {self.user.full_name}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.full_name}"


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
