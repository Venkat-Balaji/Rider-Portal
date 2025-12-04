from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','supabase_user_id','email','username','full_name','phone','date_of_birth',
            'blood_group','address','profile_photo_url','allergies','medical_conditions',
            'insurance_provider','insurance_policy_number','personal_doctor_name','personal_doctor_phone',
            'emergency_contact','is_active','created_at','updated_at',
        ]
        read_only_fields = ['id','supabase_user_id','created_at','updated_at','is_active']

class MeSerializer(UserSerializer):
    qr = serializers.SerializerMethodField()

    def get_qr(self, obj):
        # import here to avoid circular import at module level
        try:
            from qr.serializers import QRCodeSerializer
            qr = getattr(obj, 'qr', None)
            if qr:
                return QRCodeSerializer(qr).data
            return None
        except Exception:
            return None
