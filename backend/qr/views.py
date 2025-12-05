# qr/views.py
import io
import qrcode
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import QRCode, QRScan
from .serializers import PublicQRSerializer
from audits.models import AuditLog
from django.http import HttpResponse

class PublicQRView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        qr = get_object_or_404(QRCode, token=token, is_active=True)
        data = PublicQRSerializer(qr).data
        AuditLog.objects.create(actor_user_id=qr.user_id, action='qr_view_public', details={'token': token}, ip=self._get_ip(request))
        return Response({'data': data})

    def _get_ip(self, request):
        return request.META.get('REMOTE_ADDR')

class RecordScanView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, token):
        qr = QRCode.objects.filter(token=token, is_active=True).first()
        user = qr.user if qr else None
        lat = None
        lon = None
        loc = request.data.get('location') or {}
        if isinstance(loc, dict):
            lat = loc.get('lat')
            lon = loc.get('lon')
        scan = QRScan.objects.create(
            qr_token=token,
            user=user,
            ip=self._get_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            location_lat=lat,
            location_lon=lon
        )
        AuditLog.objects.create(actor_user_id=user.id if user else None, action='qr_scan_recorded', details={'token': token, 'scan_id': scan.id}, ip=self._get_ip(request))
        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    def _get_ip(self, request):
        return request.META.get('REMOTE_ADDR')

# Authenticated endpoint: return PNG image for user's QR
class QRImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'qr') or not user.qr or not user.qr.is_active:
            return Response({'detail': 'QR not found'}, status=status.HTTP_404_NOT_FOUND)
        token = user.qr.token
        qr_url = f'{request.scheme}://{request.get_host()}/api/v1/qr/{token}/'
        img = qrcode.make(qr_url)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return HttpResponse(buf.getvalue(), content_type='image/png')
