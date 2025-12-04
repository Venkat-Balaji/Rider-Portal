import uuid
from django.db import models
from django.conf import settings

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    storage_path = models.TextField()
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField(null=True, blank=True)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.user_id})'
