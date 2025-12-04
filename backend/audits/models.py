from django.db import models
import uuid

class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    actor_user_id = models.UUIDField(null=True, blank=True)
    actor_role = models.CharField(max_length=128, blank=True, null=True)
    action = models.CharField(max_length=255)
    details = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action} by {self.actor_user_id} at {self.created_at}'
