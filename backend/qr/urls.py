# existing qr/urls.py
from django.urls import path
from .views import PublicQRView, RecordScanView, QRImageView

urlpatterns = [
    path('<str:token>/', PublicQRView.as_view(), name='public-qr'),
    path('<str:token>/scan', RecordScanView.as_view(), name='qr-scan'),
    # Authenticated user's QR image:
    path('me/image', QRImageView.as_view(), name='qr-image'),
]
