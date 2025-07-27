from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        national_id: str,
        password: str,
        role: str = "patient",
        **extra_fields,
    ):
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

    def create_superuser(
        self,
        email: str,
        national_id: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            national_id=national_id,
            password=password,
            **extra_fields,
        )


"""
National ID can be used as unique key hence required
Email also required for OTP and reminders
When a new user is created in the system, their default status is inactive, hence admin must activate them or doc when creating thme
"""


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES: tuple = (
        ("admin", "Admin"),
        (
            "doctor",
            "Doctor",
        ),
        ("patient", "Patient"),
    )
    national_id = models.CharField(max_length=12, null=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    full_name = models.CharField(max_length=50, null=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")
    profile_pic = models.URLField(
        default="https://shorturl.at/cA9tj",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
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
    objects: CustomUserManager = CustomUserManager()


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Doctor: {self.user.full_name}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=False)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.full_name}"


# only 1 admin per clinic, admin is activated by super user, then the admin goes on to activate doctors and patients
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.CharField(max_length=20)

    def clean(self):
        if not self.pk:
            admin_count = AdminProfile.objects.count()
            if admin_count >= 2:
                raise ValidationError("Only 2 admins are allowed in the system.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.user.full_name} @ {self.center}"
