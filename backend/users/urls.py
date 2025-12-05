# users/urls.py
from django.urls import path
from .views import MeView, RegenerateQRView
from .views import ContactListCreateView, ContactDetailView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('me/qr/regenerate', RegenerateQRView.as_view(), name='regenerate-qr'),
]

# append contacts endpoints if available
if ContactListCreateView:
    urlpatterns += [
        path('me/contacts/', ContactListCreateView.as_view(), name='contacts'),
        path('me/contacts/<uuid:id>/', ContactDetailView.as_view(), name='contact-detail'),
    ]
