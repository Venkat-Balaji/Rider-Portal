from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import QRCode, QRScan
from .serializers import PublicQRSerializer
from audits.models import AuditLog
from django.shortcuts import get_object_or_404

class PublicQRView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        qr = get_object_or_404(QRCode, token=token, is_active=True)
        # optional cache layer should be inserted here
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
        lat = request.data.get('location', {}).get('lat')
        lon = request.data.get('location', {}).get('lon')
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
