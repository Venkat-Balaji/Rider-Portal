# users/serializers.py
from rest_framework import serializers
from .models import User
# import EmergencyContact from models_extra to avoid circular issues if placed separately
try:
    from .models_extra import EmergencyContact
except Exception:
    # if EmergencyContact is in models.py, import it from there
    try:
        from .models import EmergencyContact
    except Exception:
        EmergencyContact = None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','supabase_user_id','email','username','full_name','phone','date_of_birth',
            'blood_group','address','profile_photo_url','allergies','medical_conditions',
            'insurance_provider','insurance_policy_number','personal_doctor_name','personal_doctor_phone',
            'profile_completed','profile_completion_score','is_active','created_at','updated_at',
        ]
        read_only_fields = ['id','supabase_user_id','created_at','updated_at','is_active','profile_completion_score','profile_completed']

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id','name','phone','relation','priority','created_at']
        read_only_fields = ['id','created_at']

class MeSerializer(UserSerializer):
    qr = serializers.SerializerMethodField()
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)

    def get_qr(self, obj):
        # import here to avoid circular import issues
        try:
            from qr.serializers import QRCodeSerializer
            qr = getattr(obj, 'qr', None)
            if qr:
                return QRCodeSerializer(qr).data
            return None
        except Exception:
            return None
