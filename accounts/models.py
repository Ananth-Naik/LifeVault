from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
        ("ADMIN", "Admin"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("BLOCKED", "Blocked"),
    ]


    VERIFICATION_CHOICES = [
    ("PENDING", "Pending"),
    ("VERIFIED", "Verified"),
    ("REJECTED", "Rejected"),
    ]

    verification_status = models.CharField(
    max_length=10,
    choices=VERIFICATION_CHOICES,
    default="PENDING"
    )

    user_id = models.AutoField(primary_key=True)

    lifevault_id = models.CharField(
        max_length=15,
        unique=True,
        blank=True
    )
    qr_code = models.ImageField(
    upload_to="qr_codes/",
    null=True,
    blank=True
)

    full_name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    account_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):

        if not self.lifevault_id:

            prefix = "P" if self.role == "PATIENT" else "D"

            last_user = User.objects.filter(
                role=self.role
            ).order_by("-user_id").first()

            if last_user:
                number = int(last_user.lifevault_id[-4:]) + 1
            else:
                number = 1

            self.lifevault_id = f"LV26{prefix}{number:04d}"

        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.lifevault_id} - {self.full_name}"
class PatientProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    blood_pressure = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    emergency_phone = models.CharField(
        max_length=15,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "patient_profiles"

    def __str__(self):
        return f"{self.user.lifevault_id} - Patient Profile"
class EmergencyContact(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="emergency_contact"
    )

    name = models.CharField(max_length=100)

    relationship = models.CharField(max_length=50)

    phone = models.CharField(max_length=15)

    address = models.TextField(blank=True)

    class Meta:
        db_table = "emergency_contacts"

    def __str__(self):
        return f"{self.user.lifevault_id} - {self.name}"