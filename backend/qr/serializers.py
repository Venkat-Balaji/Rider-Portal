from rest_framework import serializers
from .models import QRCode, QRScan

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id','token','is_active','created_at','rotated_at']

class PublicQRSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    def get_user(self, obj):
        # Build public-safe user payload directly from obj.user to avoid circular imports
        user = obj.user
        return {
            'id': str(user.id),
            'full_name': user.full_name,
            'blood_group': user.blood_group,
            'age': None,  # compute if you want
            'medical_conditions': user.medical_conditions or [],
            'allergies': user.allergies or [],
            'personal_doctor': {
                'name': user.personal_doctor_name,
                'phone': user.personal_doctor_phone
            },
            'emergency_contacts': user.emergency_contact or [],
            'insurance': {
                'provider': user.insurance_provider,
                'policy': user.insurance_policy_number
            }
        }

    def get_meta(self, obj):
        user = obj.user
        updated = getattr(user, 'updated_at', None)
        return {
            'qr_token': obj.token,
            'last_updated': updated.isoformat() if updated else None
        }
