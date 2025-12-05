# documents/views.py
import time
import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentSerializer
from django.conf import settings
from audits.models import AuditLog

# Pillow optional import for dev thumbnailing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

import io
import base64

class SignedUploadURLView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        filename = request.data.get('filename')
        content_type = request.data.get('content_type', 'application/octet-stream')
        if not filename:
            return Response({'error': 'filename required'}, status=status.HTTP_400_BAD_REQUEST)

        svc_key = getattr(settings, 'SUPABASE_SERVICE_KEY', None)
        bucket = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'public')
        storage_path = f'{request.user.id}/{int(time.time())}-{filename}'

        if svc_key and getattr(settings, 'SUPABASE_ISS', None):
            sign_base = settings.SUPABASE_ISS.replace('https://', '').strip('/')
            url = f'https://{sign_base}/storage/v1/object/sign/{bucket}/{storage_path}'
            headers = {'Authorization': f'Bearer {svc_key}'}
            r = requests.post(url, headers=headers)
            if r.status_code == 200:
                data = r.json()
                upload_url = data.get('signedURL') or data.get('signed_url') or data.get('signedUrl') or data.get('url')
                return Response({'upload_url': upload_url, 'storage_path': f'{bucket}/{storage_path}'})
            else:
                return Response({'error': 'failed to get signed url', 'detail': r.text}, status=500)
        else:
            # dev fallback - frontend cannot actually PUT to this; only for testing metadata flow
            return Response({'upload_url': f'/local-upload/{storage_path}', 'storage_path': f'{bucket}/{storage_path}'})

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user, uploaded_by=self.request.user.supabase_user_id)
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='document_created', details={'doc_id': str(obj.id)})
        # Dev convenience: try to generate thumbnail synchronously if possible
        try:
            generate_thumbnail_sync(obj)
        except Exception:
            # do not fail request if thumbnailing breaks
            pass

class DocumentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='document_deleted', details={'doc_id': str(instance.id)})
        instance.status = 'deleted'
        instance.save(update_fields=['status'])

def generate_thumbnail_sync(document: Document):
    """
    Simple dev-time thumbnailer that downloads accessible URLs and saves base64 data URL into thumbnail_path.
    Replace with background task + real storage upload for production.
    """
    if not PIL_AVAILABLE:
        return
    sp = document.storage_path or ''
    if sp.startswith('http://') or sp.startswith('https://'):
        r = requests.get(sp, stream=True, timeout=10)
        r.raise_for_status()
        img = Image.open(r.raw).convert('RGB')
    else:
        # cannot access non-URL storage paths here
        return

    img.thumbnail((400, 400))
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=80)
    buf.seek(0)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    document.thumbnail_path = f'data:image/jpeg;base64,{b64}'
    document.thumbnail_converted = True
    document.save(update_fields=['thumbnail_path','thumbnail_converted'])
