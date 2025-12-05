from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','title','message','metadata','is_read','created_at','seen_at']
        read_only_fields = ['id','created_at','seen_at']
