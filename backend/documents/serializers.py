from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','user','name','type','storage_path','mime_type','size_bytes','uploaded_by','uploaded_at']
        read_only_fields = ['id','user','storage_path','uploaded_by','uploaded_at']
