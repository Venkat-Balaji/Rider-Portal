import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, supabase_user_id, email=None, password=None, **extra):
        if not supabase_user_id:
            raise ValueError('supabase_user_id required')
        user = self.model(supabase_user_id=supabase_user_id, email=email or '', **extra)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, supabase_user_id, email=None, password=None, **extra):
        user = self.create_user(supabase_user_id, email=email, **extra)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supabase_user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo_url = models.TextField(blank=True, null=True)
    allergies = models.JSONField(default=list, blank=True)
    medical_conditions = models.JSONField(default=list, blank=True)
    insurance_provider = models.CharField(max_length=255, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=255, blank=True, null=True)
    personal_doctor_name = models.CharField(max_length=255, blank=True, null=True)
    personal_doctor_phone = models.CharField(max_length=32, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    profile_completed = models.BooleanField(default=False)
    profile_completion_score = models.PositiveSmallIntegerField(default=0) 
    objects = UserManager()

    USERNAME_FIELD = 'supabase_user_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name or self.email or self.supabase_user_id
class EmergencyContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    relation = models.CharField(max_length=64, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(default=1)  # 1 (primary), 2 (secondary)
    created_at = models.DateTimeField(auto_now_add=True)