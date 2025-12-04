from django.urls import path
from .views import PublicQRView, RecordScanView

urlpatterns = [
    path('<str:token>/', PublicQRView.as_view(), name='public-qr'),
    path('<str:token>/scan', RecordScanView.as_view(), name='qr-scan'),
]
