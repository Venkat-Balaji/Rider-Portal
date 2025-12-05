# qr/serializers.py
from rest_framework import serializers
from .models import QRCode

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id','token','is_active','created_at','rotated_at']

class PublicQRSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return {
            'id': str(user.id),
            'full_name': user.full_name,
            'blood_group': user.blood_group,
            'medical_conditions': user.medical_conditions or [],
            'allergies': user.allergies or [],
            'personal_doctor': {
                'name': user.personal_doctor_name,
                'phone': user.personal_doctor_phone
            },
            'emergency_contacts': [
                {'name': c.name, 'phone': c.phone, 'relation': c.relation} for c in getattr(user, 'emergency_contacts', []).all()
            ] if hasattr(user, 'emergency_contacts') else [],
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
