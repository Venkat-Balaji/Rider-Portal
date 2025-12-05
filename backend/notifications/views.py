# notification/views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from audits.models import AuditLog

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        n = get_object_or_404(Notification, id=id, user=request.user)
        n.is_read = True
        n.seen_at = timezone.now()
        n.save(update_fields=['is_read', 'seen_at'])
        AuditLog.objects.create(actor_user_id=request.user.id, action='notification_read', details={'notification_id': str(n.id)})
        return Response({'ok': True}, status=status.HTTP_200_OK)
