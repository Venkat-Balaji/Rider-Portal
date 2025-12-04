from django.urls import path
from .views import MeView, RegenerateQRView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('me/qr/regenerate', RegenerateQRView.as_view(), name='regenerate-qr'),
]
