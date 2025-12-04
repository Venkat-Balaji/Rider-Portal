from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import MeSerializer
from qr.models import QRCode
from audits.models import AuditLog
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        AuditLog.objects.create(actor_user_id=user.id, action='profile_update', details={'user': str(user.id)})

class RegenerateQRView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        # generate token
        import secrets, string
        token = secrets.token_urlsafe(12)
        qr, created = QRCode.objects.update_or_create(user=user, defaults={'token': token, 'is_active': True, 'rotated_at': timezone.now()})
        AuditLog.objects.create(actor_user_id=user.id, action='qr_regenerated', details={'token': token}, ip=self._get_ip(request))
        return Response({'qr_token': qr.token}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        return request.META.get('REMOTE_ADDR')

