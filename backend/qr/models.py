import uuid
from django.db import models
from django.conf import settings

class QRCode(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='qr')
    token = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated_at = models.DateTimeField(null=True, blank=True)
    image_path = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'QR({self.token}) for {self.user_id}'

class QRScan(models.Model):
    id = models.BigAutoField(primary_key=True)
    qr_token = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
