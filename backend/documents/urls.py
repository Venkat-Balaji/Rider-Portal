from django.urls import path
from .views import DocumentListCreateView, SignedUploadURLView, DocumentDetailView

urlpatterns = [
    path('', DocumentListCreateView.as_view(), name='documents'),
    path('signed-url', SignedUploadURLView.as_view(), name='documents-signed-url'),
    path('<uuid:id>/', DocumentDetailView.as_view(), name='document-detail'),
]
