from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentSerializer
from django.conf import settings
from audits.models import AuditLog
from rest_framework.parsers import MultiPartParser, FormParser

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def perform_create(self, serializer):
        # For production, return signed upload url to frontend.
        # Here we accept metadata and create a placeholder record. For direct uploads use signed urls.
        serializer.save(user=self.request.user, uploaded_by=self.request.user.supabase_user_id)
        AuditLog.objects.create(actor_user_id=self.request.user.id, action='document_uploaded', details={'doc': str(serializer.instance.id)})

class SignedUploadURLView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        filename = request.data.get('filename')
        content_type = request.data.get('content_type', 'application/octet-stream')
        if not filename:
            return Response({'error': 'filename required'}, status=status.HTTP_400_BAD_REQUEST)
        # If SUPABASE_SERVICE_KEY is configured call Supabase Storage API to get signed URL.
        svc_key = getattr(settings, 'SUPABASE_SERVICE_KEY', None)
        bucket = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'public')
        if svc_key:
            # build signed url using Supabase REST API for storage (simple example)
            # NOTE: In a production system you should use Supabase client or generate a presigned URL server-side
            import requests, urllib.parse, time, hashlib, hmac
            # For brevity we produce a "fake" signed URL pointing to Supabase storage path; implement properly for your project.
            storage_path = f'{bucket}/{request.user.id}/{filename}'
            signed_url = f'https://{settings.SUPABASE_ISS.replace("https://","")}/storage/v1/object/sign/{urllib.parse.quote(storage_path)}'
            # This endpoint requires service key in headers; but for a short example we'll just return the sign endpoint for the frontend to call with service key (not recommended)
            return Response({'upload_url': signed_url, 'storage_path': storage_path})
        else:
            # fallback: provide local placeholder
            storage_path = f'local/{request.user.id}/{filename}'
            return Response({'upload_url': f'/local-upload/{storage_path}', 'storage_path': storage_path})
