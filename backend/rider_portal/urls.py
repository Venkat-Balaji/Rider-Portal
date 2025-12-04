from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', TemplateView.as_view(template_name='index.html'), name='dev-index'),
    path('dev/qr/', TemplateView.as_view(template_name='qr_check.html'), name='dev-qr'),
    path('dev/api-test/', TemplateView.as_view(template_name='api_test.html'), name='dev-api-test'),
    path('api/v1/', include([
        path('users/', include('users.urls')),
        path('qr/', include('qr.urls')),
        path('documents/', include('documents.urls')),
    ])),
]
