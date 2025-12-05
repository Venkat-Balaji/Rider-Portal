# users/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, EmergencyContact
from .serializers import MeSerializer, EmergencyContactSerializer
from audits.models import AuditLog
from django.utils import timezone

def calculate_profile_completion(user):
    fields = [
       ('full_name', 10), ('phone', 15), ('date_of_birth', 10), ('blood_group', 5),
       ('address', 10), ('profile_photo_url', 10),
       ('medical_conditions', 8), ('allergies', 7), ('insurance_provider', 5),
       ('personal_doctor_name', 5), ('emergency_contacts', 15)
    ]
    score = 0
    for field, weight in fields:
        if field == 'emergency_contacts':
            if EmergencyContact.objects.filter(user=user).exists():
                score += weight
        else:
            val = getattr(user, field, None)
            if val:
                if isinstance(val, (list, dict)):
                    if val:
                        score += weight
                else:
                    score += weight
    return min(100, score)

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        score = calculate_profile_completion(user)
        user.profile_completion_score = score
        user.profile_completed = (score >= 80)
        user.updated_at = timezone.now()
        user.save(update_fields=['profile_completion_score','profile_completed','updated_at'])
        AuditLog.objects.create(actor_user_id=user.id, action='profile_update', details={'score': score})

class RegenerateQRView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        import secrets
        from qr.models import QRCode
        token = secrets.token_urlsafe(12)
        qr, created = QRCode.objects.update_or_create(user=user, defaults={'token': token, 'is_active': True, 'rotated_at': timezone.now()})
        AuditLog.objects.create(actor_user_id=user.id, action='qr_regenerated', details={'token': token}, ip=self._get_ip(request))
        try:
            from notifications.models import Notification
            Notification.objects.create(user=user, title='QR regenerated', message='Your emergency QR code was regenerated.', metadata={'token': token})
        except Exception:
            pass
        return Response({'qr_token': qr.token}, status=status.HTTP_200_OK)

    def _get_ip(self, request):
        return request.META.get('REMOTE_ADDR')

class ContactListCreateView(generics.ListCreateAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='contact_created', details={'contact_id': str(obj.id)})

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)
    def perform_update(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='contact_updated', details={'contact_id': str(obj.id)})
    def perform_destroy(self, instance):
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='contact_deleted', details={'contact_id': str(instance.id)})
        instance.delete()
